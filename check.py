import sqlite3
from urllib import request
import requests
import datetime
import urllib
import json
import time
import random

def get_all_users():
    with sqlite3.connect('data_vk') as con:
        cur = con.cursor()
        return cur.execute(f'SELECT * FROM users').fetchall()
    if con:
        con.commit()
        con.close()

def get_users_data(user_id):
    with sqlite3.connect('data_vk') as con:
        cur = con.cursor()
        try:
            return cur.execute(f'SELECT * FROM users WHERE user_id="{user_id}"').fetchall()[0]
        except:
            return False
    if con:
        con.commit()
        con.close()

def startStatus(token):
    try:
        try:
            getCountry = requests.get("https://api.vk.com/method/account.getProfileInfo?v=5.95&access_token={0}".format(token))
            getCountry = getCountry.json()
            getCountry = getCountry["response"]
            getCountry = getCountry["city"]
            city = getCountry["title"]
        except:
            getCountry = requests.get("https://api.vk.com/method/account.getProfileInfo?v=5.95&access_token={0}".format(token))
            getCountry = getCountry.json()
            getCountry = getCountry["response"]
            city = getCountry['home_town']     

        url = "http://api.openweathermap.org/data/2.5/weather"
        parameters = {
        'q': city,
        'appid': "3ca96ba2df742f49a5e220299ae0a2ef",
        'units':'metric',
        'lang' : 'ru'}
        res = requests.get(url, params = parameters)
        data = res.json()

        getLikes = requests.get("https://api.vk.com/method/photos.get?album_id=profile&rev=1&extended=1&count=1&v=5.95&access_token={0}".format(token))
        getLikes = getLikes.json()
        getLikes = getLikes["response"]
        getLikes = getLikes["items"]
        getLikes = getLikes[0]
        getLikes = getLikes["likes"]
        getLikes = getLikes["count"]

        getValuts = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
        getEuro = getValuts.text.split('<Valute ID="R01239">')[1].split('</Valute>')[0].split('<Value>')[1].split('</Value>')[0].split(',')[0]
        getDollar = getValuts.text.split('<Valute ID="R01235">')[1].split('</Valute>')[0].split('<Value>')[1].split('</Value>')[0].split(',')[0]

        today = datetime.datetime.today()
        nowTime = today.strftime("%H:%M")
        nowDate = today.strftime("%d.%m.%Y")

        statusSave = ("🕰 Время: {0} | 📅 Дата: {1} | ☁ Погода в городе: '{2}' составляет: {3}℃ | 💟 Лайков на аве: {4} | 💵 Доллар: {5}р | 💶 Евро: {6}р | 😘 @freestatusvk_bot".format(nowTime, nowDate,
            data["name"], str(data["main"]["temp"]), getLikes, getDollar, getEuro))
        requests.get("https://api.vk.com/method/status.set?text=" + statusSave + "&v=5.95&access_token={0}".format(token))
        return True
    except:
        return False

while True:
    users = get_all_users()
    for user in users:
        if get_users_data(user[0])[1] == 1 or str(get_users_data(user[0])[1]) == '1' or get_users_data(user[0])[1] == '1':
            token = str(get_users_data(user[0])[2])
            if startStatus(token) is True:
                print(f'set status user_id: {user[0]}')
            else:
                continue
        else:
            continue 
    time.sleep(random.randint(60, 120))
