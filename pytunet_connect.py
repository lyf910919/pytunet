import time
import urllib.request, hashlib
import codecs

login_url  = 'http://net.tsinghua.edu.cn/do_login.php'
logout_url = 'http://net.tsinghua.edu.cn/do_login.php'
check_url  = 'http://net.tsinghua.edu.cn/do_login.php'
query_url  = 'https://usereg.tsinghua.edu.cn/login.php'

times_cnt = {1: 'FIRST', 2: 'SECOND', 3: 'THIRD', 4: 'FORTH', 5: 'FIFTH'}
ret_type  = {'Logoutissuccessful'       : 'LOGOUT SUCCESS',
            'not_online' : 'NOT ONLINE',
            'ip_exist_error'   : 'IP ALREADY EXISTS',
            'user_tab_error'   : 'THE CERTIFICATION PROGRAM WAS NOT STARTED',
            'username_error'   : 'WRONG USERNAME',
            'user_group_error' : 'ACCOUNT INFOMATION INCORRECT',
            'password_error'   : 'WRONG PASSWORD',
            'status_error'     : 'ACCOUNT OVERDUE, PLEASE RECHARGE',
            'available_error'  : 'ACCOUNT HAS BEEN SUSPENDED',
            'delete_error'     : 'ACCOUNT HAS BEEN DELETED',
            'usernum_error'    : 'USERS NUMBER LIMITED',
            'online_num_error' : 'USERS NUMBER LIMITED',
            'mode_error'       : 'DISABLE WEB REGISTRY',
            'time_policy_error': 'CURRENT TIME IS NOT ALLOWED TO CONNECT',
            'flux_error'       : 'FLUX OVER',
            'ip_error'         : 'IP NOT VALID',
            'mac_error'        : 'MAC NOT VALID',
            'sync_error'       : 'YOUR INFOMATION HAS BEEN MODIFIED, PLEASE TRY AGAIN AFTER 2 MINUTES',
            'ip_alloc'         : 'THE IP HAS BEEN ASSIGNED TO OTHER USER'
            }

version  = '1.2'
sleep_time = 8

#########################################################
#                Main Login/Logout Modules                #
#########################################################

def trans_content(response):
    content = response.read().decode()
    ret = ''
    for ch in content:
        if ch.isalpha() or ch == '_':
            ret += ch
    return ret

def tunet_login(username, password):
    hashcd_md5 = hashlib.md5()
    hashcd_md5.update(password.encode())
    tr_password = hashcd_md5.hexdigest()
    print(tr_password)
    login_data = 'action=login' + '&username=' + username + '&password={MD5_HEX}' + tr_password + '&ac_id=1'
    login_data = login_data.encode()
    request_url = urllib.request.Request(login_url, login_data)
    response_url = urllib.request.urlopen(request_url)
    ret = trans_content(response_url)
    print (ret_type.get(ret, 'CONNECTED'))
    return ret

def tunet_logout():
    logout_data = 'action=logout'
    logout_data = logout_data.encode()
    request_url = urllib.request.Request(logout_url, logout_data)
    response_url = urllib.request.urlopen(request_url)
    ret = trans_content(response_url)
    print (ret)
    print (ret_type.get(ret, 'CONNECTED'))
    return ret

def tunet_check():
    check_data = 'action=check_online'
    check_data = check_data.encode()
    request_url = urllib.request.Request(check_url, check_data)
    response_url = urllib.request.urlopen(request_url)
    ret = trans_content(response_url)
    if ret == 'not_online':
        print ('NOT ONLINE')
    else:
        print (ret_type.get(ret, 'CONNECTED'))
    return ret

#########################################################
#                    Help&Version Modules                #
#########################################################

def tunet_help():
    print ('-h, --help   : show all options of Tsinghua University Internet Connector')
    print ('-v, --version: show version of Tsinghua University Internet Connector')
    print ('-u           : input your username after \'-u\'')
    print ('-p           : input your password after \'-p\'')
    print ('-a           : enter username and password later, you can login other campus network account')
    print ('-i, --login  : login operation')
    print ('-o, --logout : logout operation')
    print ('-c, --check  : check the internet')
    print ('-q, --query  : query basic infomation, online state and flux usage details')

def tunet_version():
    print ('Tsinghua University Internet Connector ', version)

def tunet_others():
    print ('UNKNOWN OPTIONS')
    print ('WHICH OPTION DO YOU WANT?')
    tunet_help()
    print ('IF ANY ERROR, PLEASE CONTACT im@huhaoyu.com.')

#########################################################
#                        Main Part                        #
#########################################################

def tunet_connect(username, password):
    ret = 'ip_exist_error'
    for count in range(5):
        print ('%s attempts to connect...' % times_cnt.get(count + 1))
        if ret != tunet_login(username, password):
            break
        if count == 4:
            print ('please try to reconnect after 1 minute')
            break
        print ('try to reconnect after %s seconds' %sleep_time)
        time.sleep(sleep_time)
        print ()