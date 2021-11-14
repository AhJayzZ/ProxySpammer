import requests, json
import os,time
from bs4 import BeautifulSoup

# File path setting
dir_path = os.path.dirname(__file__)
file_name = 'proxy.txt'                             # Default file name
proxy_file_path = os.path.join(dir_path,file_name)

# Max connection retries
requests.adapters.DEFAULT_RETRIES = 5


# Close request log
requests.packages.urllib3.disable_warnings()



# Url configuration
ip_test_url = "https://www.whatismyip.com.tw/"

proxy_api = "https://www.proxyscan.io/api/proxy?type=https"
course_home_url = "https://gpa.ntustexam.com/"
course_dislike_url = "https://gpa.ntustexam.com/dislike"
course_like_url = "https://gpa.ntustexam.com/like"



def get_proxy():
    proxy_data = requests.get(proxy_api).json()[0]
    proxy_ip = str(proxy_data['Ip'])
    proxy_port = str(proxy_data['Port'])
    proxy_server = proxy_ip + ":" + proxy_port

    # Need only HTTPS protocal 
    if len(proxy_data['Type']) > 1 :
        proxy_type = str(proxy_data['Type'][1])
    else :
        proxy_type = str(proxy_data['Type'][0])
        
    print('Proxy server:',proxy_server,proxy_type)
    return proxy_server,proxy_type
      
def url_request(proxy_server,proxy_type):

    myheader = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
    myproxy = {
        'https': proxy_server,
        # 'http':  'http://' + proxy_server,
        # 'SOCKS4' : 'SOCKS4://' + proxy_server,
        # 'SOCKS5' : 'SOCKS5://' + proxy_server,
    }

    # request session configuration
    mysession = requests.session()
    mysession.cookies.clear()
    mysession.proxies = myproxy
    mysession.headers = myheader
    mysession.timeout = 10
    mysession.verify = False
    mysession.keep_alive = False

    # Check proxy existence
    exist = proxy_record(proxy_server)
    try :
        if not exist :
            # Proxy haven't been used

            # Step 1. Get token
            res = mysession.get(course_home_url)
            soup = BeautifulSoup(res.text,'html.parser')
            form = soup.find('form',{'id':'queryForm'})
            token = form.find('input',{'name':'_token'})['value']
            print('token:',token)

            # Step 2.Dislike
            form_data={
                '_token' : token,
                'id' : 2347,        # 2347 is the ID of course
            }
            result = mysession.post(course_dislike_url,data = form_data)
            print(result.text)
            print('Status Code:',result.status_code ,'\n')

            # Proxy server validation checking
            # res = mysession.get(ip_test_url,headers=myheader,verify=False,proxies=myproxy)
            # soup = BeautifulSoup(res.text,'html.parser')
            # ip = soup.find('span').text
            # print('My IP:',ip)

        else :
            # Proxy have been used,pass 
            print('Proxy data exist!','\n')
            pass
    except :
        print('Abandon (Bad proxy server)','\n')
        pass


def proxy_record(proxy_server) :
    # File not exist
    if not os.path.exists(proxy_file_path):
        # Create a new txt file
        try :
            f = open(file_name,'w')
            f.close()
        except :
            print('File creation error , please check again file name!')
            exit(0)

    f = open(proxy_file_path,'a+')
    ip_data = f.readlines()
    for ip in ip_data :
        print (ip)
        if proxy_server == ip :
            # Proxy data already exist
            return True
        
    # Proxy not exist
    f.write(proxy_server + '\n')
    f.close()
    return False


    
if __name__ == '__main__' :
    while True :
    
        time.sleep(2)

        # Get proxy server data
        proxy_server,proxy_type = get_proxy()

        # Requesting the url
        url_request(proxy_server,proxy_type)
            