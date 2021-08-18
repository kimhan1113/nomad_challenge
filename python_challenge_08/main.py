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
    #     flag_new = 1
    return temp_list

@app.route("/")
@app.route("/?order_by=popular")
def home():
    order = request.args.get("order_by")
    global flag_popular

    print('home in')
    print(order)
    
    if (flag_popular):
        data = get_stories(popular)

    else:
        data = db["popular"]

    
    if ((order == 'popular') or (order == None)):
        return render_template("index.html", data=data, order="popular")

    else:
        try:
            data_new = db['new']
        except:
            data_new = get_stories(new)
        return render_template("index.html", data=data_new, order="new",)

    
    # return render_template("index.html")


# @app.route("/?order_by=new")
# def new_url():
#     order = request.args.get("order_by")

#     global flag_new

#     print('new in')

#     if (flag_new):
#         data = get_stories(new)

#     else:
#         data = db["new"]

#     if ((order == 'popular') or (order == None)):
#         # 어차피 첫페이지는 popular라서 무조건 db에 들어가니깐 다시 불러올때는 db에서 불러올수있다.       
#         data = db["popular"]
#         return render_template("index.html", data=data, order='popular')
#     else:
#         return render_template("index.html", data=data, order="new",)


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