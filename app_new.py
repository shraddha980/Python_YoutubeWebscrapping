import re
import urllib.request
from urllib.request import urlopen as uReq
from urllib import request, response
from cleantext import clean
import pandas as pd
import scrapetube
from youtube_comment_scraper_python import *
from bs4 import BeautifulSoup
import requests.models
from flask import Flask
from flask import render_template
from flask_cors import cross_origin
# import mysql.connector
from sqlalchemy import create_engine, sql
import pymysql
import pickle
import sqlite3
from pandas.io import sql
import pymysql
import pymongo
import eventlet
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

app = Flask(__name__)


@app.route("/", methods=('GET', 'POST'))
@cross_origin()
def homepage():
    return render_template("index.html")


@app.route("/review", methods=['GET', 'POST'])
@cross_origin()
def results():

    chrome_path = r"/app/.chromedriver/bin/chromedriver"
    driver = webdriver.Chrome(chrome_path)
    driver.get("https://www.youtube.com/c/CampusX-official/videos")
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    video_lists = []
    for i in user_data:
        video_lists.append(i.get_attribute('href'))
    print(video_lists)

# print(len(links))

# def remove_emoji(string):
# emoji_pattern = re.compile("["
# u"U0001F600-U0001F64F"  # emoticons
# u"U0001F300-U0001F5FF"  # symbols & pictographs
# u"U0001F680-U0001F6FF"  # transport & map symbols
# u"U0001F1E0-U0001F1FF"  # flags (iOS)
# u"U00002702-U000027B0"
# u"U000024C2-U0001F251"
# "]+", flags=re.UNICODE)
# return emoji_pattern.sub(r'', string)
    all_data = []
    for video in video_lists:

        r = requests.get(video)
        s = BeautifulSoup(r.text, "html.parser")
        try:
            title = s.find("meta", itemprop="name")['content']
            # new_title = remove_emoji(title)
            # new_title1 = clean(new_title, no_emoji=True)
            # new_title2 = re.sub(r'[^\w\s]', '', new_title1)
            # new_title2 = new_title2.replace("//", "")
        except TypeError as e:
            print(e)
            print("handled successfully")
        try:
            views = s.find("meta", itemprop="interactionCount")['content']
        except TypeError as e:
            print(e)
            print("handled successfully")
        try:
            date_published = s.find("meta", itemprop="datePublished")['content']
        except TypeError as e:
            print(e)
            print("handled successfully")
        try:
            description = s.find("meta", itemprop="description")['content'].replace('"', '')
        except TypeError as e:
            print(e)
            print("handled successfully")
    # new_description = remove_emoji(description)
    # new_description1 = clean(new_description, no_emoji=True)
    # new_description2 = re.sub(r'[^\w\s]', '', new_description1)
    # new_description2 = new_description2.replace("//", "")
        #try:
            #duration = s.find("span", {"class": "ytp-time-duration"})
        #except TypeError as e:
            #print(e)
            #print("handled successfully")
        try:
            tag = ', '.join([meta.attrs.get("content") for meta in s.find_all("meta", {"property": "og:video:tag"})])
            # tag1 = tag.strip('"')
        except TypeError as e:
            print(e)
            print("handled successfully")

        try:
            comment_div = s.select("#content #content-text")
            comment_list = [x.text for x in comment_div]
        except TypeError as e:
            print(e)
            print("handled successfully")

        mydict = {"Title": title, "Views": views, "Date_published": date_published, "Description": description,"Tag": tag}
        all_data.append(mydict)
    print(all_data)
    df = pd.DataFrame(all_data)
    df.to_csv('text1.csv')
    print(df)
    return render_template('results.html', all_data=all_data)


# client = pymongo.MongoClient(
# "mongodb+srv://shraddha_111:make_Way12@cluster0.ek5ysl8.mongodb.net/?retryWrites=true&w=majority")
# db = client.test
# print(db)
# db1 = client['MongoDB']
# coll = db1['Youtube_data']
# coll.insert_many(all_data)


# else:
# return render_template('index.html')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8012, debug=True)

