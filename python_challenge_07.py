import os
import csv
import requests
from bs4 import BeautifulSoup as bfs
import bs4
import re
import pandas as pd
from tqdm import tqdm

os.system("clear")
alba_url = "http://www.alba.co.kr"

company_list = []


def get_url_name(url):

    link_list = []

    indeed_result = requests.get(url)
 
    indeed_soup = bfs(indeed_result.text, 'html.parser')

    # only search for superbrands
    result = indeed_soup.find_all(id = 'MainSuperBrand')

    for res in result:

        # do not sort both list cuz they were appended different list

        # get urls
        href_result = res.find('ul', class_ = 'goodsBox').find_all("a", class_ = 'goodsBox-info', href=True)

        for href in href_result:
            link_list.append(href['href'])


        # get company names
        company_result = res.find('ul', class_ = 'goodsBox').find_all("a", class_ = 'goodsBox-info')

        # clean company name and put them in list
        for com in company_result:
            com_name = str(com.find_all('span', class_='company'))
            com_name=re.sub('<.+?>', '', com_name, 0).strip()[1:-1]
            company_list.append(com_name)

    return link_list   


def crawling_data(url):


    indeed_result = requests.get(url)

    indeed_soup = bfs(indeed_result.text, 'html.parser')

    tables = indeed_soup.find_all("table")

    for table in tables:
        for table_row in table.find_all('tr'):

            # columns = list(table_row.find_all('td',class_='local first'))

            locale = table_row.find('td',class_='local first')
            company = table_row.find('td',class_='title')
            work_time = table_row.find('td',class_='data')
            salary = table_row.find('td',class_='pay')
            regtime = table_row.find('td',class_='regDate last')

            try:
                # locale = re.sub("\?"," ", locale)
                com = company.find('span', class_='company')
                link_total.append([locale.text, com.text, work_time.text, salary.text, regtime.text])
                
            except:
                continue

#NormalInfo > script:nth-child(6)
def get_total_page(url):

    indeed_result = requests.get(url)
    indeed_soup = bfs(indeed_result.text, 'html.parser')

    pages = indeed_soup.find_all(class_ = 'jobCount')
    # numbers = re.sub(r'[^0-9]', '', pages[0])
    number_list = re.findall("\d", pages[0].text)
    number = "".join(number_list)
    
    total_page = int(number) / 50
    if(type(total_page) == float):
        total_page = int(total_page) + 1

    return total_page


if __name__ == "__main__":

    links = get_url_name(alba_url)

    

    for j, link in enumerate(tqdm(links)):

        total_page = get_total_page(link)

        try:

            link_total = []        
            for i in range(total_page+1):           
                crawling_data(link + f'job/brand/?page={i+1}&pagesize=50')
                
            df = pd.DataFrame(link_total)
            df.columns=["place", "title", "time", "pay", "date"]
            
            # remove specific chars
            file_name = re.sub("\&amp;","", company_list[j])
            df.to_csv(file_name+'.csv', index=False)
            
        except:
            continue
