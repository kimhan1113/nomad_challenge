import os
import requests
from bs4 import BeautifulSoup as bf
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

# print(format_currency(5000, "GBP", locale="ko_KR"))


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

def get_exchange(from_country, to_country):
    url = f'https://wise.com/gb/currency-converter/{from_country.lower()}-to-{to_country.lower()}-rate?'
    indeed_result = requests.get(url)
    # print(indeed_result)
    indeed_soup = bf(indeed_result.text, 'html.parser')

    # 태그명, 클래스명으로 찾음!
    result = indeed_soup.find('span','text-success').text

    # 바로 int형으로 변환이 안된다 float형의 string이면 먼저 float로 바꾸고
    # int로 바꿀수 있다.

    result = float(result)
    # result = result
    return result

if __name__ == "__main__":
    
    country_data_list = get_tr_data(url)

    # print(country_data_list[0][2])
    # assert 1==0

    print('Welcome to CurrencyConvert PRO 2000')
    print()


    for i, data in enumerate(country_data_list):
        print("#" + str(i) + ' ' + data[0])
    # int(ans) > len(country_data_list) - 1
    print()
    print('Where are you from? Choose a country by number.\n')

    from_country = 0
    to_country = 0

    while True:
        print('#:', end=" ")
        from_country = input()

        try:
            from_country = int(from_country)
        except:
            print('That wasn\'t a number')
            continue
            
        if (type(from_country) != int) or (int(from_country) > len(country_data_list) - 1):
            
            print('Choose a number from the list.')
            continue
        else:
            print(f'{country_data_list[from_country][0]}\n')
            break

    print('Now choose another country.')
    print()
    while True:
        
        print('#:', end=" ")
        to_country = input()

        try:
            to_country = int(to_country)
        except:
            print('That wasn\'t a number\n')
            continue

        if (type(to_country) != int) or (int(to_country) > len(country_data_list) - 1):
            
            print('Choose a number from the list.')
            continue
        else:
            print(f'{country_data_list[to_country][0]}\n')
            break

    while True:

        print(f'How many {country_data_list[from_country][1]} do you want to convert to {country_data_list[to_country][1]}?')
        
        ans = input()

        try:
            ans = int(ans)
        except:
            print('That wasn\'t a number\n')
            continue

        else:

            from_code = country_data_list[from_country][1].lower()
            to_code = country_data_list[to_country][1].lower()
    
            exchange = get_exchange(from_code, to_code)
            exchange = ans * exchange

            print(f'{country_data_list[from_country][1]} {ans:,} is {format_currency(exchange, to_code.upper(), locale="ko_KR")}')
            break
