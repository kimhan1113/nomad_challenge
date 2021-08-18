import requests
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(ids):
  return f"{base_url}/items/{ids}"


db = {}
app = Flask("DayNine")


flag_new = True
flag_popular = True

def get_stories(arg):
    data = requests.get(arg).json()
    temp_list = []
    for i in data["hits"]:
        tmp = {}
        tmp["title"] = i['title']
        tmp["url"] = i['url']
        tmp["points"] = i['points']
        tmp["author"] = i['author']
        tmp["num_comments"] = i['num_comments']
        tmp["id"] = i['objectID']
        temp_list.append(tmp)

    if arg == popular:
        db["popular"] = temp_list
        global flag_popular
        flag_popular = False
    else:
        db['new'] = temp_list
        global flag_new
        flag_new = False

    return temp_list

@app.route("/")
@app.route("/?order_by=popular")
def home():
    order = request.args.get("order_by")
    global flag_popular
    global flag_new
    
    # 처음 서버실행하면 데이터를 긁어온다 
    if (flag_popular):
        data = get_stories(popular)
        # false로 해줘서 또 요청할 시 db에서 데이터를 가져오도록 한다.
        flag_popular = False
    else:
        data = db["popular"]
    
    # html 템플릿에서 order로 보여지는 화면 판단 할 수있도록 한다.
    if ((order == 'popular') or (order == None)):
        return render_template("index.html", data=data, order="popular")

    # popular가 아니면 
    else:

        # popular와 동일한 방식으로 flag로 구분해서 처음들어오면 데이터를 긁어오고
        # flag를 false해준다. 즉 다음에 들어올 때는 db에 있는 데이터를 가지고 온다.
        if(flag_new):
            data_new = get_stories(new)
            flag_new = False
            
        else:
            data_new = db['new']       

        return render_template("index.html", data=data_new, order="new",)

    
    # return render_template("index.html")


def get_id_data(id_):

    json_url = make_detail_url(id_)

    comment = requests.get(json_url).json()

    temp_list = []

    temp = {}
    temp["title"] = comment['title']
    temp["url"] = comment['url']
    temp["points"] = comment['points']

    temp["title_author"] = comment['author']

    temp_list.append(temp)

    for i in comment["children"]:
        tmp = {}
        if(i['author'] == None):
            continue
        tmp["author"] = i['author']
        tmp["text"] = i['text']
        temp_list.append(tmp)

    return temp_list

@app.route("/<idnum>")
def get_id(idnum):
    data = get_id_data(idnum)
    colon = ":"
    return render_template("detail.html", data=data, idnum=idnum, colon=colon)

# print(get_stories('https://hn.algolia.com/api/v1/search_by_date?tags=story'))
app.run(host="0.0.0.0")
