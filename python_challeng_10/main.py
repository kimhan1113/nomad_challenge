import requests
from flask import Flask, render_template, request, send_file, redirect, url_for
from get_data import *
from flask_cors import CORS



os.system('clear')


"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

# extend를 써서 data를 하나로 합치자!!

db = {}

app = Flask("DayTwelve")

# CORS(app, expose_headers=["x-suggested-filename"])

@app.route("/" , methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/read")
def read():

    total_data= []
    lang = request.args["lang"]
 
    jobs = db.get(lang)

    if jobs:
        
        print('fake db로옴!') 
        return render_template("read.html", lang=lang, data=jobs)
             

    else:
        remoteok_data = remoteok(lang)
        stackoverflow_data = stackoverflow(lang)
        weworkremotely_data = weworkremotely(lang)

        total_data.extend(remoteok_data)
        total_data.extend(stackoverflow_data)
        total_data.extend(weworkremotely_data)

        db[lang] = total_data
        print("db없어서 새로 만듬!")
        return render_template("read.html", lang=lang, data=total_data)


@app.route('/export')
def export():
    try:
        word = request.args.get('lang')

        if not word:
            raise Exception()
        
        jobs = db.get(word)
        if not jobs:
            raise Exception()

        save_to_file(jobs, word)
        # 'application/x-csv',
        # 웨일에서는 작동안됨 뭔짓을해도,,
        result = send_file( word + '.csv',
                     mimetype='text/csv',
                     attachment_filename = word + '.csv',
                     as_attachment=True)

        return result
    except:                 
        return redirect('/read')
 
app.run(host="0.0.0.0")




