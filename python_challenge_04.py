import requests
import os
import sys


# print(urls)
stop = False
def check_continuous():
    
    while True:
        print('Do you wanna start over? (y/n)')
        ans = str(input()).lower()
        if(ans == 'y'):
            os.system('clear')
            break
        elif(ans ==  'n'):
            print('k. bye!')
            stop = True
            return stop
        else:
            print(f'{ans} is not valid word')
            continue


while True:
    print('Welcome to IsItDown.py')
    print('please write a URL or URLs you want to check. (seperated by comma)')

    urls = list(map(str, input().split(',')))

    for url in urls:
        clean_url = url.strip()
        # print(clean_url)

        if('http://' in clean_url):
            pass
        else:
            clean_url = 'http://' + clean_url

        if('.com' not in clean_url):
            print(f'{clean_url} is not a valid URL')
            continue
            
        else:
            pass

        try:
            r = requests.get(clean_url)
            (r.status_code == 200)
            print(f'{clean_url} is Up!')
            
        except:
            print(f'{clean_url} is down')
        
    stop = check_continuous()
    if(stop):
        break    
            


