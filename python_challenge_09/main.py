import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bfs
import os


os.system('clear')


"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""


subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")

@app.route("/" , methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/read")
def read():

    # ischecked = "on", else = "None"
    data_list = []
    language_list = []
    for lang in subreddits:

        check = request.args.get(lang)
        url = f'https://www.reddit.com/r/{lang}/top/?t=month'

        # 표시가 되었다면 on이 들어감으로 true가된다.
        if(check):
            
            language_list.append(lang)
            indeed_result = requests.get(url, headers=headers)
            indeed_soup = bfs(indeed_result.text, 'html.parser')

            # 제목 가져오기
            title_list = indeed_soup.find("div", class_="_1OVBBWLtHoSPfGCRaPzpTf _3nSp9cdBpqL13CqjdMr2L_ _2OVNlZuUd8L9v0yVECZ2iA").find_all("a", class_=lambda value: value and value.startswith("SQnoC3ObvgnGjWt90zD9Z"))

            # 투표수 가져오기
            vote_list = indeed_soup.find("div", class_="_1OVBBWLtHoSPfGCRaPzpTf _3nSp9cdBpqL13CqjdMr2L_ _2OVNlZuUd8L9v0yVECZ2iA").find_all("div", class_ = lambda value: value and value.startswith('_23h0-EcaBUorIHC-JZyh6J'))

            # 연결할 url 가져오기
            url_list = indeed_soup.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")

            # vote에 광고는 vote로 표시되서 제거해야함, k는 * 1000로 바꿈
            clean_vote = []
            for vote in vote_list:

                # 데이터 타입이 bs4라서 못찾았던 거임!!  
                # string 변환한 후 광고에 들어가는 string으로
                # vote를 필터한다.  
                check_vote = str(vote)

                if 'vote-arrows-t3_z' in check_vote:
                    continue

                try:
                    vote_text = vote.text.strip()
                    if vote_text.endswith('k'):
                        vote_int = int(float(vote_text[:-1]) * 1000)
                        clean_vote.append(vote_int)
                    elif vote_text.startswith('Vote'):
                        continue
                    else:
                        vote_int = int(vote_text)
                        clean_vote.append(vote_int)
                except:
                    continue
            
            for i in range(len(clean_vote)):
                
                title = title_list[i].text.strip()
                vote = clean_vote[i]
                url = url_list[i]['href']
                language = 'r/' + lang
                data_list.append([title, vote, url, language])
                
        else:
            continue

    print(len(title_list))
    print(len(clean_vote))
    print(len(url_list))
        
    # data_list vote 순으로 정렬해야함.
    data_list.sort(key=lambda x:x[1], reverse=True)

    
    # temp = request.args.get('javascript')
    # temp2 = request.args.get('reactjs')
    # print(temp, temp2)

    # check에 걸리는 language들은 data에 담아서 read.html로 보내자!
    return render_template("read.html", data = data_list, language_list =  language_list)

app.run(host="0.0.0.0")