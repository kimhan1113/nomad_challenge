import os
import requests
from bs4 import BeautifulSoup as bf

os.system("clear")
url = "https://www.iban.com/currency-codes"
# print(indeed_soup.find_all('tr').text)


def get_tr_data(url):

    data_list = list()
    indeed_result = requests.get(url)
    # print(indeed_result)
    indeed_soup = bf(indeed_result.text, 'html.parser')
    for i, tr in enumerate(indeed_soup.find_all('tr')):
        if i == 0:
            continue
        else:
            data = tr.get_text().strip().split('\n')

            if data[1] == 'No universal currency':
                continue
            else:            
                temp = [data[0].capitalize(), data[2], data[3]]
                # temp.append([])
                data_list.append(temp)
    
    return data_list

country_data_list = get_tr_data(url)

# print(country_data_list[0][2])
# assert 1==0

print('Hello! Please choose select a country by number:')


for i, data in enumerate(country_data_list):
    print("#" +' ' + str(i) + ' ' + data[0])
# int(ans) > len(country_data_list) - 1

while True:
    print('#:', end=" ")
    ans = input()

    try:
        ans = int(ans)
    except:
        pass

    if type(ans) == str:
        print('That wasn\'t a number')
        continue
    elif (type(ans) != int) or (int(ans) > len(country_data_list) - 1):
        
        print('Choose a number from the list.')
        continue
    else:
        print(f'You chose {country_data_list[ans][0]}')
        print(f'The currency Code is {country_data_list[ans][1]}')
        break