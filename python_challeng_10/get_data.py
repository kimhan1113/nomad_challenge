from bs4 import BeautifulSoup as bfs
import os
import requests
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

os.system('clear')
# https://stackoverflow.com/jobs?r=true&q=python
# https://weworkremotely.com/remote-jobs/search?term=python
# https://remoteok.io/remote-dev+python-jobs

def stackoverflow(name):

    data_list = []

    url = f'https://stackoverflow.com/jobs?r=true&q={name}'
    indeed_result = requests.get(url, headers=headers)
    indeed_soup = bfs(indeed_result.text, 'html.parser')

    author_list = indeed_soup.find_all("h3", class_="fc-black-700 fs-body1 mb4")
    title_list = indeed_soup.find_all("h2", class_="mb4 fc-black-800 fs-body3")
    link_list = indeed_soup.find_all("a", class_="s-link stretched-link")
    

    for i in range(len(author_list)):

        author = author_list[i].text.split('\n')[1].strip()
        title = title_list[i].text.strip()
        link = 'https://stackoverflow.com' + str(link_list[i]['href']).strip()

        data_list.append([title,author,link])
    
    return data_list

    

def weworkremotely(name):

    data_list = []
    
    url = f'https://weworkremotely.com/remote-jobs/search?term={name}'
    indeed_result = requests.get(url, headers=headers)
    indeed_soup = bfs(indeed_result.text, 'html.parser')

    author_list = indeed_soup.find_all("span", class_="company")
    title_list = indeed_soup.find_all("span", class_="title")
    link_list = indeed_soup.find("div", class_="jobs-container").find_all("a")


    clean_author_list = []
    for i in range(0,len(author_list),3):
        clean_author_list.append(author_list[i].text)

    clean_link_list = []
    for link in link_list:
        try:
            str_link = link['href']
            str_link = str(str_link)
            if((str_link.startswith('/remote-jobs')) or (str_link.startswith('/listings'))):
                # print(str_link)
                clean_link_list.append(link)
        except:
            continue


    for i in range(len(clean_author_list)):

        author = clean_author_list[i].strip()
        title = title_list[i].text.strip()
        link = 'https://weworkremotely.com' + str(clean_link_list[i]['href']).strip()
  
        data_list.append([title,author,link])


    
    return data_list
    


def remoteok(name):
    # https://remoteok.io/remote-dev+python-jobs

    url = f'https://remoteok.io/remote-dev+{name}-jobs'

    data_list = []

    indeed_result = requests.get(url, headers=headers)
    indeed_soup = bfs(indeed_result.text, 'html.parser')

    title_list = indeed_soup.find_all("h2" , itemprop="title")
    author_list = indeed_soup.find_all("h3" , itemprop="name")
    # title_list = indeed_soup.find_all("a", class_="preventLink").find("h2")
    link_list = indeed_soup.find_all("a", itemprop="url")

    for i in range(len(title_list)):

        author = author_list[i].text.strip()
        title = title_list[i].text.strip()
        link = 'https://remoteok.io' + str(link_list[i]['href']).strip()
  
        data_list.append([title,author,link])

    return data_list
    

def save_to_file(jobs, word):
    f = open(f"{word}.csv", "w")
    w = csv.writer(f)
    w.writerow(["Title", "Company", "Link"])

    for job in jobs:
        w.writerow(job)
    f.close
    return
