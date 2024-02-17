import requests
import os
import random
from selenium import webdriver

def general_request(url, file_path, headers, proxy):
    
    if(proxy): #if proxy is not null in the config
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            r = requests.get(url, headers=headers, proxies=proxies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")  
    else:
        try:
            r = requests.get(url, headers=headers)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")  

def cookie_request(url, cookie_url, file_path, headers, proxy): #symilar to the previous but collects cookies in case the request needs them
    if(proxy):
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            response = requests.get(cookie_url)
            if response.status_code == 200:
                cookies = response.cookies
            r = requests.get(url, headers=headers, proxies=proxies, cookies=cookies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")   
    else:
        try:
            response = requests.get(cookie_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.get(url, headers=headers, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")  

def general_post_request(url, file_path, headers, data, proxy): #This is a symilar function but with a post instead of a get
    
    if(proxy):
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            r = requests.post(url, headers=headers, proxies=proxies, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")  
    else:
        try:
            r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")  

def cookie_post_request(url, cookie_url, file_path, headers, data, proxy):
    if(proxy):
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            response = requests.get(cookie_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            else:
                print("Failed to retrieve cookies, trying the request without them (reponse might be useless)")
                r = requests.post(url, headers=headers, data=data, proxies=proxies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")   
    else:
        try:
            response = requests.get(cookie_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, cookies=cookies)
            else:
                print("Failed to retrieve cookies, trying the request without them (reponse might be useless)")
                r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")


#
#v.2
#

def get_request(url, file_path, headers=None, data=None, cookies_url=None, crazy_cookies=False, cookies_headers=None, proxy=None):  #a generalisation of the previous that allows self selection of the releant function depending on the data available in the config file
    #Ordinary get request with url and file path
    if (cookies_url==None or cookies_url == '') and (cookies_headers==None or cookies_headers == '') and (proxy==None or proxy == '') and crazy_cookies==False:
        try:
            r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Proxy get request, same as before but using a proxy
    elif (cookies_url==None or cookies_url == '') and (cookies_headers==None or cookies_headers == '') and crazy_cookies==False and proxy:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            r = requests.get(url, headers=headers, data=data, proxies=proxies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Get request with simple cookies (cookie request doesn't require headers)
    elif (cookies_headers==None or cookies_headers == '') and (proxy==None or proxy == '') and crazy_cookies==False and cookies_url:
        try:
            response = requests.get(cookies_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.get(url, headers=headers, data=data, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Get request for simple cookies + proxy
    elif (cookies_headers==None or cookies_headers == '') and crazy_cookies==False and proxy and cookies_url:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            response = requests.get(cookies_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.get(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Get request for complex cookies (cookies retrieval requires headers)
    elif (proxy==None or proxy == '') and crazy_cookies==False and cookies_url and cookies_headers:
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.get(url, headers=headers, data=data, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
    #Get request for complex cookies + proxy
    elif proxy and cookies_url and cookies_headers and crazy_cookies==False:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}    
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.get(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
    #If carazy_cookies==True we'll use selenium to open a browser, connect to the site and get all mysterious cookies that are sent to us without being explicitly shown in the dev tools
    elif cookies_url and crazy_cookies==True and (proxy==None or proxy == ''):
        try:
            driver = webdriver.Chrome()
            driver.get(cookies_url)
            cookies = driver.get_cookies()
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
        try:
            r = requests.get(url, headers=headers, data=data, cookies=cookies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving content {str(e)}")
    #Same but with proxy
    elif cookies_url and crazy_cookies==True and proxy:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket} 
        try:
            driver = webdriver.Chrome()
            driver.get(cookies_url)
            cookies = driver.get_cookies()
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
        try:
            r = requests.get(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving content {str(e)}")
    #We will use both a cookies headea and crazy cookies when the site provides half of them with each method and discard the duplicates
    elif cookies_url and cookies_headers and crazy_cookies and (proxy==None or proxy == ''):
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                unique_cookies = set()
                for cookie in cookies:
                    unique_cookies.add((cookie.name, cookie.value))
                print (len(cookies))
                driver = webdriver.Chrome()
                driver.get(cookies_url)
                cookies2 = driver.get_cookies()
                for cookie in cookies2:
                    unique_cookies.add((cookie['name'], cookie['value']))
                #cookies2 = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                #cookies = set(cookies+cookies2)
                unique_cookies_dict = dict(unique_cookies)
                print (len(unique_cookies_dict))
                r = requests.get(url, headers=headers, data=data, cookies=unique_cookies_dict)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}") 
    #Same as before but with proxy
    elif proxy and cookies_url and cookies_headers and crazy_cookies:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}    
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                unique_cookies = set()
                for cookie in cookies:
                    unique_cookies.add((cookie.name, cookie.value))
                driver = webdriver.Chrome() 
                driver.get(cookies_url)
                cookies2 = driver.get_cookies()
                for cookie in cookies2:
                    unique_cookies.add((cookie['name'], cookie['value']))
                #cookies2 = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                #cookies = set(cookies+cookies2)
                unique_cookies_dict = dict(unique_cookies)
                print (len(unique_cookies_dict))
                r = requests.get(url, headers=headers, data=data, cookies=unique_cookies_dict, proxy=proxy)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.get(url, headers=headers, data=data, proxy=proxy)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}") 
    return r.status_code

def post_request(url, file_path, headers=None, data=None, cookies_url=None, crazy_cookies=False, cookies_headers=None, proxy=None):
    #Ordinary post request with url and file path
    if (cookies_url==None or cookies_url == '') and (cookies_headers==None or cookies_headers == '') and (proxy==None or proxy == '') and crazy_cookies==False:
        try:
            r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Proxy post request, same as before but using a proxy
    elif (cookies_url==None or cookies_url == '') and (cookies_headers==None or cookies_headers == '') and crazy_cookies==False and proxy:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            r = requests.post(url, headers=headers, data=data, proxies=proxies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Post request with simple cookies (cookie request doesn't require headers), cookies retrieval use get
    elif (cookies_headers==None or cookies_headers == '') and (proxy==None or proxy == '') and crazy_cookies==False and cookies_url:
        try:
            response = requests.get(cookies_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Post request for simple cookies + proxy
    elif (cookies_headers==None or cookies_headers == '') and crazy_cookies==False and proxy and cookies_url:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}
        try:
            response = requests.get(cookies_url)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error: {str(e)}")
    #Post request for complex cookies (cookies retrieval requires headers)
    elif (proxy==None or proxy == '') and crazy_cookies==False and cookies_url and cookies_headers:
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
    #Post request for complex cookies + proxy
    elif proxy and cookies_url and cookies_headers and crazy_cookies==False:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}    
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                r = requests.post(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data, proxies=proxies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")      
    #If carazy_cookies==True we'll use selenium to open a browser, connect to the site and get all mysterious cookies that are sent to us without being showed in the dev tools
    elif cookies_url and crazy_cookies==True and (cookies_headers==None or cookies_headers == '') and (proxy==None or proxy == ''):
        try:
            driver = webdriver.Chrome()
            driver.get(cookies_url)
            #cookies = driver.get_cookies()
            cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
            print (len(cookies))
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
        try:
            r = requests.post(url, headers=headers, data=data, cookies=cookies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving content {str(e)}")
    #Same but with proxy
    elif cookies_url and crazy_cookies==True and proxy:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket} 
        try:
            driver = webdriver.Chrome()
            driver.get(cookies_url)
            cookies = driver.get_cookies()
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}")
        try:
            r = requests.post(url, headers=headers, data=data, proxies=proxies, cookies=cookies)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving content {str(e)}")
    #We will use both a cookies header and crazy cookies when the site provides half of them with each method and discard the duplicates
    elif cookies_url and cookies_headers and crazy_cookies and (proxy==None or proxy == ''):
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                unique_cookies = set()
                for cookie in cookies:
                    unique_cookies.add((cookie.name, cookie.value))
                driver = webdriver.Chrome()
                driver.get(cookies_url)
                cookies2 = driver.get_cookies()
                for cookie in cookies2:
                    unique_cookies.add((cookie['name'], cookie['value']))
                #cookies2 = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                #cookies = set(cookies+cookies2)
                unique_cookies_dict = dict(unique_cookies)
                r = requests.post(url, headers=headers, data=data, cookies=unique_cookies_dict)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}") 
    #Same as before but with proxy
    elif proxy and cookies_url and cookies_headers and crazy_cookies:
        proxy_socket = proxy
        proxies=proxies = {"http": proxy_socket, "https": proxy_socket}    
        try:
            response = requests.get(cookies_url, headers=cookies_headers)
            if response.status_code == 200:
                cookies = response.cookies
                unique_cookies = set()
                for cookie in cookies:
                    unique_cookies.add((cookie.name, cookie.value))
                driver = webdriver.Chrome()
                driver.get(cookies_url)
                cookies2 = driver.get_cookies()
                for cookie in cookies2:
                    unique_cookies.add((cookie['name'], cookie['value']))
                #cookies2 = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}
                #cookies = set(cookies+cookies2)
                unique_cookies_dict = dict(unique_cookies)
                r = requests.post(url, headers=headers, data=data, cookies=unique_cookies_dict, proxy=proxy)
            else:
                print("Cookies could not be retrieved, trying a request without them")
                r = requests.post(url, headers=headers, data=data, proxy=proxy)
            with open(os.path.abspath(file_path), 'wb') as f:
                if(len(r.content)>0):
                    f.write(r.content)
        except Exception as e:
            print(f"Error retrieving cookies {str(e)}") 
    return r.status_code

def random_proxy_download(url, file_path, proxies, request_type, headers=None, data=None, cookies_url=None, crazy_cookies=False, cookies_headers=None): #if the config has several proxies it will choose one randomly and discard it if it fails to try another one
    proxy=proxies[random.randrange(len(proxies))]
    if request_type == "GET":
        if(get_request(url, file_path, proxy=proxy, headers=headers, data=data, cookies_url=cookies_url, crazy_cookies=crazy_cookies, cookies_headers=cookies_headers) != 200):
            proxies.remove(proxy)
            random_proxy_download(url, file_path, proxy, request_type, headers=headers, data=data, cookies_url=cookies_url, crazy_cookies=crazy_cookies, cookies_headers=cookies_headers)
    elif request_type == "POST":
        if(post_request(url, file_path, proxy=proxy, headers=headers, data=data, cookies_url=cookies_url, crazy_cookies=crazy_cookies, cookies_headers=cookies_headers)!= 200):
            proxies.remove(proxy)
            random_proxy_download(url, file_path, proxy, request_type, headers=headers, data=data, cookies_url=cookies_url, crazy_cookies=crazy_cookies, cookies_headers=cookies_headers)
