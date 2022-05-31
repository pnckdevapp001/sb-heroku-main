# -*- coding: utf-8-*-
from linepy import (LINE, Channel, OEPoll, OpType)
import json
import os
import traceback
import sys
import ast
import requests
import re
import random
import pytz
import string
from googletrans import Translator
from akad import *
from linepy.style import *
from linepy.login import *
from justgood import imjustgood
from time import sleep
from gtts import gTTS
from datetime import datetime
from bs4 import BeautifulSoup
import schedule
import time
from Liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread
import threading
import http.client
from pornhub_api import PornhubApi
api = PornhubApi()
api.stars.all()
 
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ru-4569f-default-rtdb.asia-southeast1.firebasedatabase.app'
})

#Lotto_ref = db.reference('LOTTODATA/')

login = json.loads(open('Data/token.json', 'r').read())
setting = json.loads(open('Data/settings.json', 'r').read())
cctv = json.loads(open('Data/cctv.json', 'r').read())
loger = Login()


if login["email"] == "":
    if login["token"] == "":
        data = loger.logqr(cert=None)  # You can put your Crt token here
        client = LINE(idOrAuthToken=data)
        login["token"] = data
        with open('Data/token.json', 'w') as fp:
            json.dump(login, fp, sort_keys=True, indent=4)
    else:
        try:
            client = LINE(idOrAuthToken=login["token"])
        except:
            print("TOKEN EXPIRED")
            sys.exit()
else:
    client = LINE(login["email"], login["password"])

ops = OEPoll(client)
clPoll = OEPoll(client)
starting = time.time()
mid = client.profile.mid
whitelist = [client.profile.mid, client, ]
oburl = client.server.LINE_OBJECT_URL
host = "https://{}".format(setting["main"])
protectMax = setting["proMax"]
protectStaff = setting["proStaff"]
read = {
    "addwhitelist": False,
    "delwhitelist": False,
    "addblacklist": False,
    "delblacklist": False,
    "dual": False,
    "dual2": False,
    "pp": False,
    "gpict": {},
    "cctv": {},
    "imgurl": {},
    "wmessage": {},
    "lmessage": ""
}



Gid = ["ca42c3b4b95237b04b34c2d70b87dbf88","c28b23fb070c90a0d42d8f444e61d47b2"]
Lotto_ref = db.reference('LOTTODATA/')
clipThai_ref = db.reference('GO'+str(random.randint(1,7)))

def saveDataLotto(label, textData):
    Lotto_ref.child(label+'/').set({
    label: {
        'text': textData
    }
})


def getDataLotto(label):
    snapshot = Lotto_ref.child(label+'/'+label).get()
    return snapshot["text"]


def getDataClipThai(Nlabel):
    snapshot = clipThai_ref.child(Nlabel).get()
    paylodeXclip = {
      "link": snapshot["link"],
      "splash": snapshot["splash"],
      "splashtext": snapshot["splashtext"],
      "src": snapshot["src"],
    }
    return paylodeXclip


def remove(string):
    pattern = re.compile(r'\s+')
    # pattern = re.compile(r'รอบที่ บน-ล่าง รายละเอียด')
    return re.sub(pattern, ',', string)

def trans(texttr):
    translator = Translator()
    translations = translator.translate(texttr,src='auto',dest='th')
    #print(translations.text)
    return translations.text

def url_match(urlX):
    try:
        videopath = urlX.split("$")[1]
        print(videopath)
        return videopath
    except:
        return urlX

def Lottovip():
    url = "https://www.ballsod55.com/tmp/bailek/lottoshuay.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all('table', {"class": "table table-striped"})
    label = "lottovip"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        regexT = r'\d{3}'
        roundNowLotto = "ผลหวยยี่กี จาก ʟᴏᴛᴛᴏᴠɪᴘ\n"+textdata[28]+"ที่ "+textdata[29]+"\n❸ ตัวบน "+textdata[31] + \
            "\n❷ ตัวล่าง " + textdata[32]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[37]+" "+textdata[38] + " 🔸 3บน : " + textdata[40] + " | 2ล่าง : " + textdata[41] +\
            "\n"+textdata[46]+" "+textdata[47] + " 🔸 3บน : " + textdata[49] + " | 2ล่าง : " + textdata[50] +\
            "\n"+textdata[55]+" "+textdata[56] + " 🔸 3บน : " + textdata[58] + " | 2ล่าง : " + textdata[59] +\
            "\n"+textdata[64]+" "+textdata[65] + " 🔸 3บน : " + textdata[67] + " | 2ล่าง : " + textdata[68] +\
            "\n"+textdata[73]+" "+textdata[74] + " 🔸 3บน : " + textdata[76] + " | 2ล่าง : " + textdata[77] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"    
        dataget = getDataLotto(label)
    #print(dataget)  
        toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if re.match(regexT, textdata[31]):
        if roundNowLotto != dataget:
            SaveLottoData = saveDataLotto(label,roundNowLotto)
            client.center(toGroup, label, roundNowLotto)
            print("OK_"+label.upper())
        else:
          print("DUB_"+label.upper())
      else:
        print("RUN_"+label.upper())
    except Exception as error:
        print(error)
    return "LOTTOVIP"
    


def LottoRuay():
    url = "https://www.ballsod55.com/tmp/bailek/ruayshuay.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all('table', {"class": "table table-striped"})
    label = "ruay"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        regexT = r'\d{3}'
        roundNowLotto = "ผลหวยยี่กี จาก 𝐑𝐮𝐚𝐲𝐬𝐇𝐮𝐚𝐲\n"+textdata[28]+"ที่ "+textdata[29]+"\n❸ ตัวบน "+textdata[31] + \
            "\n❷ ตัวล่าง " + textdata[32]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[37]+" "+textdata[38] + " 🔸 3บน : " + textdata[40] + " | 2ล่าง : " + textdata[41] +\
            "\n"+textdata[46]+" "+textdata[47] + " 🔸 3บน : " + textdata[49] + " | 2ล่าง : " + textdata[50] +\
            "\n"+textdata[55]+" "+textdata[56] + " 🔸 3บน : " + textdata[58] + " | 2ล่าง : " + textdata[59] +\
            "\n"+textdata[64]+" "+textdata[65] + " 🔸 3บน : " + textdata[67] + " | 2ล่าง : " + textdata[68] +\
            "\n"+textdata[73]+" "+textdata[74] + " 🔸 3บน : " + textdata[76] + " | 2ล่าง : " + textdata[77] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
        #print(roundNowLotto)        
    dataget = getDataLotto(label)
    toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if re.match(regexT, textdata[31]):
        if roundNowLotto != dataget:
            SaveLottoData = saveDataLotto(label,roundNowLotto)
            client.center(toGroup, label, roundNowLotto)
            print("OK_"+label.upper())
        else:
          print("DUB_"+label.upper())
      else:
        print("RUN_"+label.upper())
    except Exception as error:
        print(error)
    return "LottoRuay"

def LottoHuay():
    url = "https://formula.aapsite.com/stock1huayresult.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all(
        'table', {"class": "table responsive table-bordered table-sm"})
    label = "huay"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        # print(textdata)
        roundNowLotto = "ผลหวยยี่กี จาก HUAY\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
            "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
            "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
            "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
            "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
            "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
        # print(roundNowLotto)
    dataget = getDataLotto(label)
    toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if roundNowLotto != dataget:
         SaveLottoData = saveDataLotto(label, roundNowLotto)
         client.center(toGroup, label, roundNowLotto)
         print("OK_"+label.upper())
    except Exception as error:
        print(error)
    return "LottoHuay"

def LottoJet():
    url = "https://formula.aapsite.com/stock1jetsadabetresult.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all(
        'table', {"class": "table responsive table-bordered table-sm"})
    label = "jetsadabet"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        # print(textdata)
        roundNowLotto = "ผลหวยยี่กี จาก JETSADABET\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
            "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
            "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
            "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
            "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
            "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
        # print(roundNowLotto)
    dataget = getDataLotto(label)
    toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if roundNowLotto != dataget:
         SaveLottoData = saveDataLotto(label, roundNowLotto)
         client.center(toGroup, label, roundNowLotto)
         print("OK_"+label.upper())
    except Exception as error:
        print(error)
    return "LottoJet"

def Lotto2lottovip():
    url = "https://formula.aapsite.com/stock1lottovipresult.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all(
        'table', {"class": "table responsive table-bordered table-sm"})
    label = "2lottovip"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        # print(textdata)
        roundNowLotto = "ผลหวยยี่กี จาก LOTTOVIP\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
            "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
            "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
            "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
            "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
            "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
        # print(roundNowLotto)
    dataget = getDataLotto(label)
    toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if roundNowLotto != dataget:
         SaveLottoData = saveDataLotto(label, roundNowLotto)
         client.center(toGroup, label, roundNowLotto)
         print("OK_"+label.upper())
    except Exception as error:
        print(error)
    

def Lotto2ruay():
    url = "https://formula.aapsite.com/stock1ruayresult.php"
    content = requests.get(url)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, 'html.parser')
    tags = soup.find_all(
        'table', {"class": "table responsive table-bordered table-sm"})
    label = "2ruay"
    for tag in tags:
        textdata = remove(tag.get_text()).split(',')
        #print(textdata)
        roundNowLotto = "ผลหวยยี่กี จาก RUAY\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
            "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
            "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
            "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
            "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
            "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
            "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
            "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
        #print(roundNowLotto)
    dataget = getDataLotto(label)
    toGroup = 'ca42c3b4b95237b04b34c2d70b87dbf88'
    try:
      if roundNowLotto != dataget:
         SaveLottoData = saveDataLotto(label, roundNowLotto)
         client.center(toGroup, label, roundNowLotto)
         print("OK_"+label.upper())
    except Exception as error:
        print(error)

        
    

def LINE_OP_TYPE(op):
    print('++ Operation : ( %i ) %s' %(op.type, OpType._VALUES_TO_NAMES[op.type].replace('_', ' ')))
    if op.type in [19, 133]:
        if op.param3 not in mid:
            if op.param1 in protectStaff:
                th = Thread(target=prostaff(op,))
                th.start()
                th.join()
            elif op.param1 in protectMax:
                th = Thread(target=promax(op,))
                th.start()
                th.join()
        else:
            kekick(op)
              
    if op.type in [13, 124]:
        if op.param1 in protectMax:
            th = Thread(target=proinvite(op,))
            th.start()
            th.join()

    if op.type == 55:
        try:
            target = [ax.mid for ax in client.getGroup(op.param1).members]
            if op.param1 in read["cctv"]:
                if op.param2 in target:
                    if op.param2 not in read["cctv"][op.param1]:
                        user = ["คุณ", "เฮ้ เซเปียน","สบายดีไหม "," พี่สาวคนสวยของคุณเป็นอย่างไรบ้าง?"]
                        data = random.choice(user)
                        text = "• @!  {}".format(data)
                        client.sendMention(op.param1, text, [op.param2])
                        read["cctv"][op.param1][op.param2] = True
            if op.param1 in cctv['readPoint']:
                timezone = pytz.timezone("Asia/Jakarta")
                timing = datetime.now(tz=timezone)
                timer = timing.strftime('%H.%M')
                if op.param2 in cctv['readPoint'][op.param1]:
                    pass
                else:
                    cctv['readPoint'][op.param1][op.param2] = True
                    cctv['readMember'][op.param1][op.param2] = "Time: {}".format(
                        timer)
                    with open('Data/cctv.json', 'w') as fp:
                        json.dump(cctv, fp, sort_keys=True, indent=4)
        except:
            pass

    if op.type in [17, 130]:
        if op.param1 in setting["welcome"]:
            if op.param2 not in setting["blacklist"]:
                jangan = client.getGroup(op.param1)
                if op.param1 in read["wmessage"]:
                    text = "สวัสดี @! \nยินดีต้อนรับ " + jangan.name + \
                        "\n" + read["wmessage"][op.param1]
                    client.sendMention(op.param1, text, [op.param2])
                    client.sendPage(op.param1)
                else:
                    text = "สวัสดี @! \nยินดีต้อนรับ " + jangan.name
                    client.sendMention(op.param1, text, [op.param2])
                    client.sendPage(op.param1)

    if op.type in [15, 128]:
        if setting["leave"] == True:
            if op.param2 not in setting["blacklist"]:
                jangan = client.getGroup(op.param1)
                if read["lmessage"] != "":
                    mess = read["lmessage"] + " @! "
                    client.sendMention(op.param1, mess, [op.param2])
                else:
                    mess = "ลาก่อน @! "
                    client.sendMention(op.param1, mess, [op.param2])

    if op.type == 5:
        if setting["adders"] == True:
            if op.param1 not in setting["blacklist"]:
                if setting["addmsg"] == "":
                    client.sendMention(
                        op.param1, "สวัสดี @! \nขอบคุณ ที่แอดเพื่อน :)", [op.param1])
                else:
                    text = "สวัสดี @! \n" + setting["addmsg"]
                    client.sendMention(op.param1, text, [op.param1])

    if op.type in [13, 17, 55, 124, 130]:
        if op.param2 in setting["blacklist"]:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except:
                pass

    if op.type in [32, 126]:
        if op.param1 in protectMax:
            if op.param2 not in setting["whitelist"]:
                setting["blacklist"].append(op.param2)
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
                try:
                    client.kickoutFromGroup(op.param1, [op.param2])
                    client.findAndAddContactsByMid(op.param3)
                    client.inviteIntoGroup(op.param1, [op.param3])
                except:
                    pass

    if op.type in [11, 122]:
        if op.param1 in protectMax and op.param3 == "4":
            if op.param2 not in setting["whitelist"]:
                setting["blacklist"].append(op.param2)
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
                hoax = client.getGroup(op.param1)
                if hoax.preventedJoinByTicket == False:
                    abc = client.getGroup(op.param1)
                    abc.preventedJoinByTicket = True
                    client.updateGroup(abc)
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        pass
            else:
                hoax = client.getGroup(op.param1)
                if hoax.preventedJoinByTicket == False:
                    abc = client.getGroup(op.param1)
                    abc.preventedJoinByTicket = True
                    client.updateGroup(abc)

    if op.type == 11:
        if op.param1 in protectMax and op.param3 == "1":
            if op.param2 not in setting["whitelist"]:
                setting["blacklist"].append(op.param2)
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
                hoax = client.getGroup(op.param1).name
                if hoax not in setting["gname"][op.param1]:
                    abc = client.getGroup(op.param1)
                    abc.name = setting["gname"][op.param1]
                    client.updateGroup(abc)
                    try:
                        client.kickoutFromGroup(op.param1, [op.param2])
                    except:
                        pass
            else:
                abc = client.getGroup(op.param1).name
                setting["gname"][op.param1] = abc
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)

    if op.type == 25 or op.type == 26:
        try:
            msg = op.message
            txt = msg.text
            if msg.toType in [0, 2]:
                to = msg.to
                ids = msg.id
                msg.to = msg.to
                if msg.contentType == 0:
                    if None == txt:
                        return False
                    cmd = txt.lower()
                    rname = setting["rname"].lower() + " "
                    link = txt[txt.find(":")+2:]
                    #search = txt[txt.find(":")+2:].lower()
                    #print( msg )
                    if re.search(r'help', cmd):
                        menu = open('help/help.txt', 'r',encoding='utf-8' ).read()
                        client.help(msg.to,'คำสั่ง', menu)
                    
                    if re.search(r'avc', cmd):
                        #label = "JAV"
                        APIAV = ["https://mgzyz1.com/api.php/provide/vod/?ac=detail","https://apilj.com/api.php/provide/vod/at/json/?ac=detail"]
                        url = requests.get(random.choice(APIAV))
                        text = url.text
                        data = json.loads(text)
                        avdata = data['list'][random.randint(1,19)]
                        # x_vod_id = str(avdata['vod_id'])
                        # x_vod_pic = avdata['vod_pic']
                        # x_vod_name_Th = trans(avdata['vod_name'])
                        # x_vod_name = avdata['vod_name']
                        # x_vod_time = avdata['vod_time']
                        # x_type_name_Th = trans(avdata['type_name'])
                        # x_vod_score = str(avdata['vod_score'])
                        vpath = url_match(avdata['vod_play_url'])
                        #flexJav={"type": "bubble", "size": "kilo", "body":{"type": "box", "layout": "vertical", "contents": [{"type": "video", "url": vpath, "previewUrl": vpath, "altContent":{"type": "image", "size": "full", "aspectRatio": "1:1", "aspectMode": "cover", "url": x_vod_pic}},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "AVFREEX24.COM", "size": "xxs", "color": "#ff0000"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ff0000", "paddingStart": "5px", "paddingEnd": "5px", "paddingTop": "1px", "paddingBottom": "1px", "cornerRadius": "5px", "offsetTop": "5px", "offsetStart": "5px", "backgroundColor": "#00000011"},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": x_vod_name_Th , "weight": "bold", "wrap": True, "color": "#ffffffcc"},{"type": "text", "text": x_type_name_Th, "wrap": True, "size": "xxs", "margin": "sm", "color": "#ffffffcc"}], "paddingTop": "5px", "paddingEnd": "10px", "paddingStart": "10px"}], "paddingAll": "0px", "paddingBottom": "13px", "backgroundColor": "#000000"}}
                        #print(flexJav)
                        client.sendFlexVideo(msg.to,vpath)

                    if re.search(r'clt', cmd):
                        #label = "JAV"
                        #APIAV = ["https://mgzyz1.com/api.php/provide/vod/?ac=detail","https://apilj.com/api.php/provide/vod/at/json/?ac=detail"]
                        url = requests.get(f"https://ru-4569f-default-rtdb.asia-southeast1.firebasedatabase.app/GO"+str(random.randint(1,7))+"/"+str(random.randint(1,120))+".json")
                        text = url.text
                        data = json.loads(text)
                        #x_vod_id = str(data['vod_id'])
                        #x_vod_pic = data['splash']
                        x_vod_src = data['src']
                        #x_vod_name_Th = trans(avdata['vod_name'])
                        #x_vod_name = avdata['vod_name']
                        #x_vod_time = avdata['vod_time']
                        #x_type_name_Th = trans(avdata['type_name'])
                        #x_vod_score = str(avdata['vod_score'])
                        #vpath = url_match(avdata['vod_play_url'])
                        #flexJav={"type": "bubble", "size": "kilo", "body":{"type": "box", "layout": "vertical", "contents": [{"type": "video", "url": vpath, "previewUrl": vpath, "altContent":{"type": "image", "size": "full", "aspectRatio": "1:1", "aspectMode": "cover", "url": x_vod_pic}},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "AVFREEX24.COM", "size": "xxs", "color": "#ff0000"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ff0000", "paddingStart": "5px", "paddingEnd": "5px", "paddingTop": "1px", "paddingBottom": "1px", "cornerRadius": "5px", "offsetTop": "5px", "offsetStart": "5px", "backgroundColor": "#00000011"},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": x_vod_name_Th , "weight": "bold", "wrap": True, "color": "#ffffffcc"},{"type": "text", "text": x_type_name_Th, "wrap": True, "size": "xxs", "margin": "sm", "color": "#ffffffcc"}], "paddingTop": "5px", "paddingEnd": "10px", "paddingStart": "10px"}], "paddingAll": "0px", "paddingBottom": "13px", "backgroundColor": "#000000"}}
                        #print(flexJav)
                        client.sendFlexVideoTh(msg.to,x_vod_src)

                    if re.search(r'avn', cmd):
                        #label = "JAV"
                        #APIAV = ["https://mgzyz1.com/api.php/provide/vod/?ac=detail","https://apilj.com/api.php/provide/vod/at/json/?ac=detail"]
                        url = requests.get(f"https://ru-4569f-default-rtdb.asia-southeast1.firebasedatabase.app/GO"+str(random.randint(1,7))+"/"+str(random.randint(1,120))+".json")
                        text = url.text
                        data = json.loads(text)
                        #x_vod_id = str(data['vod_id'])
                        #x_vod_pic = data['splash']
                        x_vod_src = data['src']
                        #x_vod_name_Th = trans(avdata['vod_name'])
                        #x_vod_name = avdata['vod_name']
                        #x_vod_time = avdata['vod_time']
                        #x_type_name_Th = trans(avdata['type_name'])
                        #x_vod_score = str(avdata['vod_score'])
                        #vpath = url_match(avdata['vod_play_url'])
                        #flexJav={"type": "bubble", "size": "kilo", "body":{"type": "box", "layout": "vertical", "contents": [{"type": "video", "url": vpath, "previewUrl": vpath, "altContent":{"type": "image", "size": "full", "aspectRatio": "1:1", "aspectMode": "cover", "url": x_vod_pic}},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "AVFREEX24.COM", "size": "xxs", "color": "#ff0000"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ff0000", "paddingStart": "5px", "paddingEnd": "5px", "paddingTop": "1px", "paddingBottom": "1px", "cornerRadius": "5px", "offsetTop": "5px", "offsetStart": "5px", "backgroundColor": "#00000011"},{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": x_vod_name_Th , "weight": "bold", "wrap": True, "color": "#ffffffcc"},{"type": "text", "text": x_type_name_Th, "wrap": True, "size": "xxs", "margin": "sm", "color": "#ffffffcc"}], "paddingTop": "5px", "paddingEnd": "10px", "paddingStart": "10px"}], "paddingAll": "0px", "paddingBottom": "13px", "backgroundColor": "#000000"}}
                        #print(flexJav)
                        client.sendFlexVideoTh(msg.to,x_vod_src)
                    
                    if cmd.startswith('lox='):
                        msgTU = cmd.split('lox=')[1]
                        if msgTU == "":
                            return
                        DOWNLOAD_HEADERS = {'user-agent': 'TelegramBot (like TwitterBot)'}
                        conn = http.client.HTTPSConnection("api.tiktokv.com")
                        payload = ''
                        headers = {}
                        conn.request("GET", "/aweme/v1/multi/aweme/detail/?aweme_ids=%5B" + msgTU + "%5D", payload, headers)
                        res = conn.getresponse()
                        data = res.read()
                        obj = json.loads(data.decode("utf-8"))
                        download_url =  obj["aweme_details"][0]["video"]["play_addr"]["url_list"][0];
                        client.sendFlexVideoTh(msg.to,download_url)
                        

                    if cmd.startswith('ph='):
                        msgTU = cmd.split('ph=')[1]
                        if msgTU == "":
                            return
                        data = api.search.search(msgTU, period="weekly")
                        pornlist = []
                        for vid in data.videos:
                            pornlist.append(vid.video_id)
                        url = requests.get("https://playx.cleverapps.io/api/?site_id=pornhub&video_id="+random.choice(pornlist))
                        text = url.text
                        datapX = json.loads(text)
                        thumb = datapX['thumb']
                        try:
                            fullHD = datapX['mp4']['1080p']
                        except:
                            fullHD = datapX['mp4']['720p']
                        phone = datapX['mp4']['480p']
                        if fullHD != "":
                            print(fullHD,thumb)
                            client.sendFlexVideoTh(msg.to,fullHD)
                        elif phone != "":
                            print(phone,thumb)
                            client.sendFlexVideoTh(msg.to,phone)
                        else:
                            print("NOVID")
                            client.sendMessage(msg.to,"กรุณาลองใหม่อีกครั้ง")

                    # if cmd == ".ruay" or cmd == "ruay":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     datalotto = getDataLotto(label)
                    #     client.center(msg.to, label, datalotto)
                    
                    # if cmd == ".jet" or cmd == "jet":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     datalotto = getDataLotto(label)
                    #     client.center(msg.to, label, datalotto)

                    # if cmd == ".mawin" or cmd == "mawin":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     datalotto = getDataLotto(label)
                    #     client.center(msg.to, label, datalotto)
                    
                    if cmd == ".settings" or cmd == rname + ".settings":
                        if cmd.startswith('.'):
                            label = cmd.replace('.', '')
                        else:
                            label = cmd.replace(rname, "")
                        justgood = "https://www.img.in.th/images/8d8a98f486d4e22cf0cf0d80340bfc7d.png"
                        data = ""
                        if msg.to not in protectMax and msg.to not in protectStaff:
                            data += "\n\n📴 ALL PROTECTION"
                        else:
                            if msg.to in protectMax:
                                data += "\n\n🆗 PROTECT MAX"
                            elif msg.to in protectStaff:
                                data += "\n\n🆗 PROTECT STAFF"
                        if setting["ticket"]:
                            data += "\n🆗 JOIN TICKET"
                        else:
                            data += "\n📴 JOIN TICKET"
                        if msg.to in setting["welcome"]:
                            data += "\n🆗 WELCOME MESSAGE"
                        else:
                            data += "\n📴 WELCOME MESSAGE"
                        if setting["leave"]:
                            data += "\n🆗 LEAVE MESSAGE"
                        else:
                            data += "\n📴 LEAVE MESSAGE"
                        if setting["adders"]:
                            data += "\n🆗 ADD MESSAGE"
                        else:
                            data += "\n📴 ADD MESSAGE"
                        datax = {"type": "bubble", "size": "kilo", "body": {"type": "box", "layout": "vertical", "backgroundColor": "#000000", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "SETTINGS", "color": "#FFC300", "weight": "bold", "size": "xxs"}], "position": "absolute", "offsetTop": "15px", "offsetStart": "15px", "borderWidth": "1px", "borderColor": "#FFC300", "cornerRadius": "50px", "paddingStart": "7px", "paddingEnd": "7px", "paddingTop": "2px", "paddingBottom": "2px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "image", "url": justgood, "aspectRatio": "1:1", "aspectMode": "cover", "action": {
                            "type": "uri", "uri": justgood}}], "cornerRadius": "100px"}], "alignItems": "center", "paddingTop": "20px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": label.upper(), "weight": "bold", "size": "md", "color": "#FFC300"}, {"type": "text", "text": "Im Just Good", "color": "#FFC300cc", "size": "xxs"}], "alignItems": "center", "paddingTop": "10px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": data, "color": "#FFC300", "size": "xs", "wrap": True}], "paddingTop": "15px", "paddingBottom": "5px"}], "paddingAll": "10px", "paddingStart": "15px", "paddingEnd": "15px", "paddingBottom": "10px"}}
                        client.sendFlex(msg.to, datax)
                    
                    if cmd == ".me" or cmd == "me":
                        client.me(to)

                    if cmd in [".speed", "sp", "speed", ".sp"] or cmd == "speed":
                        rend = time.time()
                        client.getProfile()
                        yosh = time.time() - rend
                        client.sendMention(
                            msg.to, "「   @!   」\nTime: %.4f" % (yosh), [mid])

                    if cmd in ["rname", ".rname", "mykey", ".mykey"] or cmd == "rname":
                        client.sendMessage(msg.to, setting["rname"].title())

                    # if cmd == ".kickall" or cmd == "kickall" or cmd == setting["keykick"].lower():
                    #     if msg.toType == 2:
                    #         hoax = client.getGroup(msg.to)
                    #         client.sendMessage(msg.to, "Goodbye Bitch ~")
                    #         for ax in hoax.members:
                    #             if ax.mid not in setting["whitelist"]:
                    #                 client.kickoutFromGroup(msg.to, [ax.mid])
                    #         client.sendMessage(
                    #             msg.to, "Rubish has been cleared")

                    if cmd == "🎖️" or cmd == "@@@":
                        group = client.getGroup(msg.to)
                        midMembers = [contact.mid for contact in group.members]
                        midSelect = len(midMembers)//20
                        for mentionMembers in range(midSelect+1):
                            ret_ = "ᴘɴᴄᴋ ᴅᴀᴠ ᴀᴘᴘ\n"
                            no = 0
                            dataMid = []
                            for dataMention in group.members[mentionMembers*20: (mentionMembers+1)*20]:
                                dataMid.append(dataMention.mid)
                                ret_ += "\n{}. @!\n".format(str(no)
                                                            ).replace("/0️⃣/gi", "apples")
                                no = (no+1)
                            ret_ += "\n\n「 🔛 สมาชิกทั้งหมด {} ท่าน 」".format(str(
                                len(dataMid))) + "\n\n• (っ◔◡◔)っ 🐯 ขออภัยหากรบกวน 🐝\n• 🐳 ꜱᴏʀʀʏ ᴛᴏ ʙᴏᴛʜᴇʀ ʏᴏᴜ 🐳\n"
                            client.sendMention(msg.to, ret_, dataMid)

                    
                    #https://liff.line.me/1657175016-y3oO8Okv
                    # if cmd == ".reboot":
                    #     client.sendMessage(msg.to, "restarting..")
                    #     restart()
                    if re.search(r'dob', cmd):
                        try:
                            liff()
                            client.sendFlexText(msg.to, "https://liff.line.me/1657175016-y3oO8Okv")
                        except:
                            client.sendReplyMessage(ids, to, "เพื่อเปิดใช้งาน ดูบอลกรุณา Allow ด้วยคับ \nhttps://liff.line.me/1657175016-y3oO8Okv")
                    
                    if cmd == ".allowliff":
                        try:
                            liff()
                            client.sendFlexText(msg.to, "Flex enabled.")
                        except:
                            client.sendReplyMessage(ids, to, "Click and allow url to enable flex\nline://app/1602876096-e9QWgjyo")


                    if cmd == ".ginfo" or cmd == "ginfo":
                        group = client.getGroup(msg.to)
                        try:
                            gCreator = group.creator.displayName
                        except:
                            gCreator = "Not Found"
                        if group.invitee is None:
                            gPending = "0"
                        else:
                            gPending = str(len(group.invitee))
                        if group.pictureStatus is None:
                            gpict = "https://www.img.in.th/images/8d8a98f486d4e22cf0cf0d80340bfc7d.png"
                        else:
                            gpict = oburl + group.pictureStatus
                        menu = "\nTotal Members : {}".format(
                            str(len(group.members)))
                        menu += "\nTotal Pending : {}".format(gPending)
                        if group.preventedJoinByTicket == True:
                            menu += "\nGroup QR : Clossed"
                        else:
                            menu += "\nGroup QR: Open"
                        data = {"type": "bubble", "size": "kilo", "body": {"type": "box", "layout": "vertical", "backgroundColor": "#000000", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "GROUP INFO", "color": "#FFC300", "weight": "bold", "size": "xxs"}], "position": "absolute", "offsetTop": "15px", "offsetStart": "15px", "borderWidth": "1px", "borderColor": "#FFC300", "cornerRadius": "50px", "paddingStart": "7px", "paddingEnd": "7px", "paddingTop": "2px", "paddingBottom": "2px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "image", "url": gpict, "aspectRatio": "1:1", "aspectMode": "cover", "action": {
                            "type": "uri", "uri": gpict}}], "cornerRadius": "100px"}], "alignItems": "center", "paddingTop": "20px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": group.name, "weight": "bold", "size": "md", "color": "#FFC300"}, {"type": "text", "text": "Created By: {}".format(gCreator), "color": "#FFC300cc", "size": "xxs"}], "alignItems": "center", "paddingTop": "10px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": menu, "color": "#FFC300", "size": "xs", "wrap": True}], "paddingTop": "15px", "paddingBottom": "5px"}], "paddingAll": "10px", "paddingStart": "15px", "paddingEnd": "15px", "paddingBottom": "10px"}}
                        client.sendFlex(msg.to, data)
                        try:
                            client.sendContact(msg.to, group.creator.mid)
                        except:
                            pass
                        if group.preventedJoinByTicket == False:
                            gqropen = "GROUP URL:\nhttps://line.me/R/ti/g/{}".format(
                                str(client.reissueGroupTicket(group.id)))
                            try:
                                client.sendMessage(msg.to, gqropen)
                            except:
                                pass

                    if cmd == ".gbirth" or cmd == "gbirth":
                        client.gbirth(msg.id, msg.to)

                    if cmd == ".groups" or cmd == "groups":
                        if cmd.startswith('.'):
                            label = cmd.replace('.', '')
                        else:
                            label = cmd.replace(rname, "")
                        gruplist = client.getGroupIdsJoined()
                        kontak = client.getGroups(gruplist)
                        num = 0
                        menu = "Grouplist:\n"
                        for ids in kontak:
                            menu += "\n%i . %s" % (num, ids.name) + \
                                " (" + str(len(ids.members)) + ")"
                            num = (num+1)
                        menu += "\n\nTotal : %i Groups." % len(kontak)
                        client.help(msg.to, label, menu)

                    if cmd == ".groupid" or cmd == "🥇":
                        client.sendMessage(msg.to, "{}".format(
                            client.getGroup(msg.to).id))

                    if cmd == ".friendlist" or cmd == "friendlist":
                        if cmd.startswith('.'):
                            label = cmd.replace('.', '')
                        else:
                            label = cmd.replace(rname, "")
                        contactlist = client.getAllContactIds()
                        contacts = client.getContacts(contactlist)
                        num = 1
                        menu = "Friendlist:\n"
                        for ids in contacts:
                            menu += "\n%i. %s" % (num, ids.displayName)
                            num = (num+1)
                        menu += "\n\nTotal: %i Friends" % len(contacts)
                        client.help(msg.to, label, menu)

                    if cmd == ".pendinglist" or cmd == "pendinglist":
                        if cmd.startswith('.'):
                            label = cmd.replace('.', '')
                        else:
                            label = cmd.replace(rname, "")
                        pending = client.getGroup(msg.to)
                        if pending.invitee is None:
                            client.sendMessage(msg.to, "Pendinglist empty.")
                        else:
                            pendinglist = [a.mid for a in pending.invitee]
                            num = 1
                            menu = "Pendinglist:\n"
                            for xx in pendinglist:
                                menu += "\n%i. %s" % (num,
                                                      client.getContact(xx).displayName)
                                num = (num+1)
                            menu += "\n\nTotal: %i pendings." % len(
                                pendinglist)
                            client.help(msg.to, label, menu)

                    if cmd == ".memberlist" or cmd == "pendinglist":
                        if cmd.startswith('.'):
                            label = cmd.replace('.', '')
                        else:
                            label = cmd.replace(rname, "")
                        member = client.getGroup(msg.to)
                        members = [a.mid for a in member.members]
                        num = 1
                        menu = "Memberlist:\n"
                        for xx in members:
                            menu += "\n%i. %s" % (num,
                                                  client.getContact(xx).displayName)
                            num = (num+1)
                        menu += "\n\nTotal: %i members." % len(members)
                        client.help(msg.to, label, menu)

                    if cmd.startswith(".clear") or cmd.startswith("clear"):
                        clearing = cmd.split("clear")[1]
                        if clearing == "blacklist":
                            if setting["blacklist"] == []:
                                client.sendMessage(msg.to, "Blacklist empty!")
                            else:
                                setting["blacklist"] = []
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendReplyMessage(
                                    msg.id, msg.to, "blacklist cleared.")
                        elif clearing == "whitelist":
                            if setting["whitelist"] == []:
                                client.sendMessage(msg.to, "Whitelist empty!")
                            else:
                                setting["whitelist"] = []
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendReplyMessage(
                                    msg.id, msg.to, "Whitelist cleared.")

                    if cmd == ".whitelist" or cmd == "whitelist":
                        listing = setting["whitelist"]
                        no = 1
                        data = "• Imjustgood\n• Whitelist:\n\n"
                        for x in listing:
                            data += " {}. @! it, \n".format(no)
                            no += 1
                        data += "\nTotal: {}".format(len(listing))
                        if listing == []:
                            client.sendMessage(msg.to, "Whitelist empty!")
                        else:
                            client.sendReplyMention(
                                msg.id, msg.to, data, "", listing)

                    if cmd == ".blacklist" or cmd == "blackist":
                        listing = setting["blacklist"]
                        no = 1
                        data = "• Imjustgood\n• Blacklist:\n\n"
                        for x in listing:
                            data += " {}. @! it, \n".format(no)
                            no += 1
                        data += "\nTotal: {}".format(len(listing))
                        if listing == []:
                            client.sendMessage(msg.to, "Blacklist empty!")
                        else:
                            client.sendReplyMention(
                                msg.id, msg.to, data, "", listing)

                    if cmd == ".findblacklist" or cmd == "findblacklist":
                        if setting["blacklist"] == []:
                            client.sendReplyMessage(
                                msg.id, msg.to, "Blacklist empty!")
                        else:
                            find = client.getGroup(msg.to)
                            finded = []
                            for x in find.members:
                                if x.mid in setting["blacklist"]:
                                    finded.append(x.mid)
                            if finded == []:
                                client.sendReplyMessage(
                                    ids, to, "No blacklist found\nin '{}'".format(find.name))
                            else:
                                data = [o for o in finded]
                                finding = len(data)//20
                                for gx in range(finding + 1):
                                    result = "• ImJustGood\n• Find Blacklist:\n"
                                    listed = []
                                    no = 1
                                    for ax in data[gx*20:(gx+1)*20]:
                                        result += "\n  {}. @! it,\n".format(no)
                                        no = (no+1)
                                        listed.append(ax)
                                    result += "\nBe alert!「 {} 」here.\nGroup: {}".format(
                                        len(listed), find.name)
                                    client.sendReplyMention(
                                        ids, to, result, '', listed)

                    '''    **   GROUPSET   **   '''

                    if cmd.startswith(".kick ") or cmd.startswith("kick "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            Mmbers = [
                                a.mid for a in client.getGroup(msg.to).members]
                            hole = []
                            for mention in mentionees:
                                if mention["M"] not in hole:
                                    if mention['M'] not in Mmbers:
                                        hole.append(mention["M"])
                            for mmq in hole:
                                try:
                                    client.kickoutFromGroup(msg.to, [mmq])
                                except:
                                    client.sendMessage(msg.to, "Gagal son.")

                    if cmd.startswith(".invite ") or cmd.startswith("invite "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            Mmbers = [
                                a.mid for a in client.getGroup(msg.to).members]
                            hole = []
                            for mention in mentionees:
                                if mention["M"] not in hole:
                                    if mention['M'] not in Mmbers:
                                        hole.append(mention["M"])
                            for mmq in hole:
                                try:
                                    client.findAndAddContactsByMid(mmq)
                                    client.inviteIntoGroup(msg.to, [mmq])
                                except:
                                    client.sendMessage(msg.to, "Gagal son.")

                    if cmd.startswith(".sleed ") or cmd.startswith("sleed "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                try:
                                    client.kickoutFromGroup(
                                        msg.to, [mention['M']])
                                    client.findAndAddContactsByMid(
                                        mention['M'])
                                    client.inviteIntoGroup(
                                        msg.to, [mention['M']])
                                    client.cancelGroupInvitation(
                                        msg.to, [mention['M']])
                                except:
                                    client.sendMessage(msg.to, "Gagal son.")

                    if cmd.startswith(".joinurl ") or cmd.startswith("joinurl "):
                        mmq = msg.text.split(".joinurl ")[1]
                        if mmq.startswith("http"):
                            asw = mmq.split("/ti/g/")[1]
                            mmk = client.findGroupByTicket(asw)
                            if mmk.id not in client.getGroupIdsJoined():
                                try:
                                    client.acceptGroupInvitationByTicket(
                                        mmk.id, asw)
                                    client.sendMessage(
                                        msg.to, "Success join to {}".format(mmk.name))
                                except:
                                    pass

                    if '/ti/g/' in cmd and setting["ticket"] == True:
                        data = msg.text.split('/ti/g/')[1]
                        if " " in data:
                            link = data.split(" ")[0]
                        elif "\n" in data:
                            link = data.split("\n")[0]
                        else:
                            link = data
                        mmk = client.findGroupByTicket(link)
                        if mmk.id not in client.getGroupIdsJoined():
                            try:
                                client.acceptGroupInvitationByTicket(
                                    mmk.id, link)
                            except:
                                pass

                    if cmd.startswith(".sider ") or cmd.startswith("sider "):
                        data = cmd.split("sider ")[1]
                        if data == "on":
                            if msg.to in read["cctv"]:
                                read["cctv"][msg.to] = {}
                                client.sendMessage(msg.to, "sider restarting.")
                            else:
                                read["cctv"][msg.to] = {}
                                client.sendMessage(msg.to, "sider enabled.")
                        if data == "off":
                            if msg.to in read["cctv"]:
                                del read["cctv"][msg.to]
                                client.sendMessage(msg.to, "sider disabled.")
                            else:
                                client.sendMessage(msg.to, "already disabled.")

                    if cmd.startswith(".read") or cmd.startswith("read"):
                        data = cmd.split("read")[1]
                        if data == " on":
                            timezone = pytz.timezone("Asia/Jakarta")
                            timeNow = datetime.now(tz=timezone)
                            readTime = "Starting read point\nTime: " + \
                                timeNow.strftime('%H:%M:%S')
                            if msg.to in cctv['readPoint']:
                                cctv['readPoint'][msg.to] = {}
                                cctv['readMember'][msg.to] = {}
                                with open('Data/cctv.json', 'w') as fp:
                                    json.dump(
                                        cctv, fp, sort_keys=True, indent=4)
                                client.sendReplyMessage(
                                    msg.id, msg.to, "Read point restarting.")
                            else:
                                cctv['readPoint'][msg.to] = {}
                                cctv['readMember'][msg.to] = {}
                                with open('Data/cctv.json', 'w') as fp:
                                    json.dump(
                                        cctv, fp, sort_keys=True, indent=4)
                                client.sendReplyMessage(
                                    msg.id, msg.to, readTime)
                        if data == " off":
                            if msg.to not in cctv["readPoint"]:
                                client.sendReplyMessage(
                                    msg.id, msg.to, "already disabled.")
                            else:
                                del cctv['readPoint'][msg.to]
                                del cctv['readMember'][msg.to]
                                with open('Data/cctv.json', 'w') as fp:
                                    json.dump(
                                        cctv, fp, sort_keys=True, indent=4)
                                client.sendReplyMessage(
                                    msg.id, msg.to, "read member disabled.")
                        if data == "ing":
                            if msg.to in cctv['readPoint']:
                                if cctv["readMember"][msg.to].items() == []:
                                    client.sendReplyMessage(
                                        msg.id, msg.to, "Reader None")
                                else:
                                    yos = ""
                                    ren = []
                                    ang = '• JustGood\n• Group reader:\n\n'
                                for com in cctv["readMember"][msg.to]:
                                    heading = "@Goperation\n"
                                    just = str(len(yos)+len(ang))
                                    good = str(
                                        len(yos)+len(heading)+len(ang)-1)
                                    im = {'S': just, 'E': good, 'M': com}
                                    ren.append(im)
                                    yos += heading + \
                                        " {}\n".format(
                                            cctv["readMember"][msg.to][com])
                                text = ang + yos + "\nGroup: " + \
                                    client.getGroup(msg.to).name
                                try:
                                    client.sendReplyMessage(msg.id, msg.to, text, contentMetadata={'MENTION': str(
                                        '{"MENTIONEES":'+json.dumps(ren).replace(' ', '')+'}')}, contentType=0)
                                except Exception as e:
                                    print(e)

                    if cmd.startswith(".join ") or cmd.startswith("join "):
                        data = cmd.split("join ")[1]
                        if data == "on":
                            if setting["join"]:
                                client.sendMessage(msg.to, "already enabled.")
                            else:
                                setting["join"] = True
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to, "join enabled.")
                        if data == "off":
                            if setting["join"] == False:
                                client.sendMessage(msg.to, "already disabled.")
                            else:
                                setting["join"] = False
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to, "already disabled.")

                    if cmd.startswith(".ticket ") or cmd.startswith("ticket "):
                        data = cmd.split("ticket ")[1]
                        if data == "on":
                            if setting["ticket"]:
                                client.sendMessage(msg.to, "already enabled.")
                            else:
                                setting["ticket"] = True
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "Join ticket enabled.")
                        if data == "off":
                            if setting["ticket"] == False:
                                client.sendMessage(
                                    msg.to, "Join ticket disabled.")
                            else:
                                setting["ticket"] = False
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to, "already disabled.")

                    if cmd.startswith(".addmsg ") or cmd.startswith("addmsg "):
                        data = cmd.split("addmsg ")[1]
                        if data == "on":
                            if setting["adders"]:
                                client.sendMessage(msg.to, "already enabled.")
                            else:
                                setting["adders"] = True
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(msg.to, "Add msg enabled.")
                        if data == "off":
                            if setting["adders"] == False:
                                client.sendMessage(msg.to, "Already disabled.")
                            else:
                                setting["adders"] = False
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "add message disabled.")

                    if cmd.startswith(".leave ") or cmd.startswith("leave "):
                        data = cmd.split("leave ")[1]
                        if data == "on":
                            if setting["leave"]:
                                client.sendMessage(msg.to, "already enabled.")
                            else:
                                setting["leave"] = True
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "Leave msg enabled.")
                        if data == "off":
                            if setting["leave"] == False:
                                client.sendMessage(msg.to, "already disabled.")
                            else:
                                setting["leave"] = False
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "leave message disabled.")

                    if cmd.startswith(".welcome ") or cmd.startswith("welcome "):
                        data = cmd.split("welcome ")[1]
                        if data == "on":
                            if msg.to in setting["welcome"]:
                                client.sendMessage(msg.to, "already enabled.")
                            else:
                                setting["welcome"][msg.to] = True
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "Welcome msg enabled.")
                        if data == "off":
                            if msg.to not in setting["welcome"]:
                                client.sendMessage(
                                    msg.to, "welcome message disabled.")
                            else:
                                del setting["welcome"][msg.to]
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMessage(
                                    msg.to, "welcome message disabled.")

                    ''' ** STEALING ** '''

                    if cmd == ".geturl" or cmd == "geturl":
                        group = client.getGroup(msg.to)
                        if group.preventedJoinByTicket == True:
                            group.preventedJoinByTicket = False
                            client.updateGroup(group)
                            set = client.reissueGroupTicket(msg.to)
                            client.sendFlexText(
                                msg.to, "Group Ticket : \nhttps://line.me/R/ti/g/{}".format(str(set)))
                        else:
                            client.updateGroup()
                            set = client.reissueGroupTicket(msg.to)
                            client.sendFlexText(
                                msg.to, "Group Ticket : \nhttps://line.me/R/ti/g/{}".format(str(set)))

                    if cmd == ".gpict" or cmd == ".gpict":
                        group = client.getGroup(msg.to)
                        data = "{}{}".format(oburl, group.pictureStatus)
                        client.sendFlexImage(msg.to, data)

                    if cmd.startswith(".getpict ") or cmd.startswith("getpict "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                if mention["M"] not in setting["maker"]:
                                    data = "{}{}".format(oburl, client.getContact(
                                        mention["M"]).pictureStatus)
                                    client.sendFlexImage(msg.to, data)
                                else:
                                    client.sendMessage(
                                        msg.to, "Permission denied.")

                    if cmd.startswith(".getcover ") or cmd.startswith("getcover "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                if mention["M"] not in setting["maker"]:
                                    data = client.getProfileCoverURL(
                                        mention['M'])
                                    client.sendFlexImage(msg.to, data)
                                else:
                                    client.sendMessage(
                                        msg.to, "Permission denied.")

                    if cmd.startswith(".getmid ") or cmd.startswith("getmid "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                if mention["M"] not in setting["maker"]:
                                    data = client.getContact(mention['M']).mid
                                    client.sendMessage(msg.to, data)
                                else:
                                    client.sendMessage(
                                        msg.to, "Permission denied.")

                    if cmd.startswith(".getname ") or cmd.startswith("getname "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                if mention["M"] not in setting["maker"]:
                                    data = client.getContact(
                                        mention['M']).displayName
                                    client.sendMessage(
                                        msg.to, "「   Name   」\n{}".format(data))
                                else:
                                    client.sendMessage(
                                        msg.to, "Permission denied.")

                    if cmd.startswith(".getbio ") or cmd.startswith("getbio "):
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            for mention in mentionees:
                                if mention["M"] not in setting["maker"]:
                                    data = client.getContact(
                                        mention['M']).statusMessage
                                    client.sendMessage(
                                        msg.to, "「   Bio   」\n{}".format(data))
                                else:
                                    client.sendMessage(
                                        msg.to, "Permission denied.")

                    if cmd.startswith(".locate") or cmd.startswith("locate"):
                        cmdx = cmd.split(' @')[0]
                        if cmd.startswith('.'):
                            label = cmdx.replace('.', '')
                        else:
                            label = cmdx.replace(rname, "")
                        gruplist = client.getGroupIdsJoined()
                        kontak = client.getGroups(gruplist)
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            no = 1
                            detect = []
                            menu = "Groups Joined:\n\n"
                            for mention in mentionees:
                                profile = client.getContact(mention['M'])
                                for xx in range(len(kontak)):
                                    located = [
                                        x.mid for x in kontak[xx].members]
                                    if mention['M'] in located:
                                        detect.append(kontak[xx].id)
                                        menu += " {}. {} ({})\n".format(no,
                                                                        kontak[xx].name, len(located))
                                        no = (no+1)
                            if detect == []:
                                client.sendMessage(msg.to, "Nothing found.")
                            else:
                                menu += "\n\nTotal: {} Groups.".format(
                                    len(detect))
                                data = {"type": "bubble", "size": "kilo", "body": {"type": "box", "layout": "vertical", "backgroundColor": "#000000", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "image", "url": "{}{}".format(oburl, profile.pictureStatus), "aspectRatio": "1:1", "aspectMode": "cover"}], "cornerRadius": "100px"}], "alignItems": "center", "paddingTop": "50px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "{}".format(profile.displayName), "color": "#FFC300", "weight": "bold", "align": "center"}, {"type": "text", "text": "Tetaplah mesum", "color": "#FFC300cc", "align": "center", "size": "xxs"}], "paddingAll": "10px"}, {
                                    "type": "box", "layout": "vertical", "contents": [{"type": "text", "text": label.upper(), "color": "#FFC300", "weight": "bold", "size": "xxs"}], "position": "absolute", "borderWidth": "1px", "borderColor": "#ffffffcc", "paddingStart": "8px", "paddingEnd": "8px", "paddingTop": "5px", "paddingBottom": "5px", "offsetTop": "10px", "offsetStart": "10px", "cornerRadius": "20px"}, {"type": "box", "layout": "vertical", "contents": [{"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": menu, "color": "#FFC300", "size": "xs", "wrap": True}], "paddingAll": "20px", "backgroundColor": "#111111"}], "paddingAll": "20px", "paddingTop": "5px"}], "paddingAll": "0px"}, "styles": {"body": {"backgroundColor": "#161e2b"}}}
                                client.sendFlex(msg.to, data)

                    ''' ** PROTECTION ** '''

                    if cmd.startswith(".addwl ") or cmd.startswith(rname + "addwl "):
                        promote = cmd.split("addwl ")[1]
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            hole = []
                            white = setting["whitelist"]
                            no = 0
                            data = "Whitelist added:\n"
                            for mention in mentionees:
                                if mention["M"] not in setting["whitelist"] and mention['M'] not in setting["blacklist"]:
                                    hole.append(mention["M"])
                                    white.append(mention["M"])
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    data += "\n {}. @! it,".format(no)
                                    no = (no+1)
                                else:
                                    client.sendMention(
                                        msg.to, "@!  already in whitelist or blacklist.", [mention["M"]])
                            datax = data + \
                                "\n\nTotal: {} user.".format(len(hole))
                            try:
                                client.sendReplyMention(
                                    msg.id, msg.to, datax, "", hole)
                            except:
                                pass
                        if promote == "on":
                            client.sendMessage(msg.to, "send an contact.")
                            read["addwhitelist"] = True

                    if cmd.startswith(".delwl ") or cmd.startswith(rname + "delwl "):
                        demote = cmd.split("delwl ")[1]
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            hole = []
                            white = setting["whitelist"]
                            no = 1
                            data = "Whitelist removed:\n"
                            for mention in mentionees:
                                if mention["M"] in setting["whitelist"]:
                                    hole.append(mention["M"])
                                    white.remove(mention["M"])
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    data += "\n{}. @! it,".format(no)
                                    no += 1
                                else:
                                    client.sendMention(
                                        msg.to, "@!  not in whitelist.", [mention["M"]])
                            data += "\n\nTotal: {} user.".format(len(hole))
                            try:
                                client.sendReplyMention(
                                    msg.id, msg.to, data, "", hole)
                            except:
                                pass
                        if demote == "on":
                            client.sendMessage(msg.to, "send an contact.")
                            read["delwhitelist"] = True

                    if cmd.startswith(".addbl ") or cmd.startswith(rname + "addbl "):
                        promote = cmd.split("addbl ")[1]
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            hole = []
                            white = setting["blacklist"]
                            no = 1
                            data = "Blacklist added:\n"
                            for mention in mentionees:
                                if mention["M"] not in setting["blacklist"] and mention['M'] not in setting["whitelist"]:
                                    hole.append(mention["M"])
                                    white.append(mention["M"])
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    data += "\n {}. @! it,".format(no)
                                    no = (no+1)
                                else:
                                    client.sendMention(
                                        msg.to, "@!  already in whitelist or blacklist.", [mention["M"]])
                            datax = data + \
                                "\n\nTotal: {} user.".format(len(hole))
                            try:
                                client.sendReplyMention(
                                    msg.id, msg.to, datax, "", hole)
                            except:
                                pass
                        if promote == "on":
                            client.sendMessage(msg.to, "send an contact.")
                            read["addblacklist"] = True

                    if cmd.startswith(".delbl ") or cmd.startswith(rname + "delbl "):
                        demote = cmd.split("delbl ")[1]
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', cmd)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            hole = []
                            white = setting["blacklist"]
                            no = 1
                            data = "Blacklist removed:\n"
                            for mention in mentionees:
                                if mention["M"] in setting["blacklist"]:
                                    hole.append(mention["M"])
                                    white.remove(mention["M"])
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    data += " {}. @! it,\n".format(no)
                                    no += 1
                                else:
                                    client.sendMention(
                                        msg.to, "@!  not in blacklist.", [mention["M"]])
                            data += "\n\nTotal: {} user.".format(len(hole))
                            try:
                                client.sendReplyMention(
                                    msg.id, msg.to, data, "", hole)
                            except:
                                pass
                        if demote == "on":
                            client.sendMessage(msg.to, "send an contact.")
                            read["delblacklist"] = True

                    if cmd.startswith(".protect ") or cmd.startswith(rname + "protect "):
                        protection = cmd.split("protect ")[1]
                        if protection == "max":
                            if msg.to in protectMax:
                                client.sendMessage(
                                    msg.to, "Max protection already enabled.")
                            else:
                                if msg.to in protectStaff:
                                    del setting["proStaff"][msg.to]
                                    setting["proMax"][msg.to] = True
                                    jap = client.getGroup(msg.to)
                                    setting["gname"][msg.to] = jap.name
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    if client.getGroup(msg.to).preventedJoinByTicket == False:
                                        hoax = client.getGroup(msg.to)
                                        hoax.preventedJoinByTicket = True
                                        client.updateGroup(hoax)
                                        client.sendMessage(
                                            msg.to, "Protect max enabled.")
                                    else:
                                        client.sendMessage(
                                            msg.to, "Protect max enabled.")
                                else:
                                    if msg.to not in protectStaff and msg.to not in protectMax:
                                        setting["proMax"][msg.to] = True
                                        jap = client.getGroup(msg.to)
                                        setting["gname"][msg.to] = jap.name
                                        if client.getGroup(msg.to).preventedJoinByTicket == False:
                                            hoax = client.getGroup(msg.to)
                                            hoax.preventedJoinByTicket = True
                                            client.updateGroup(hoax)
                                            client.sendMessage(
                                                msg.to, "Protect max enabled.")
                                        else:
                                            client.sendMessage(
                                                msg.to, "Protect max enabled.")
                        elif protection == "staff":
                            if msg.to in protectStaff:
                                client.sendMessage(
                                    msg.to, "Protect staff already enabled.")
                            elif msg.to in protectMax:
                                del setting["proMax"][msg.to]
                                setting["proStaff"][msg.to] = True
                                jap = client.getGroup(msg.to)
                                setting["gname"][msg.to] = jap.name
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                if client.getGroup(msg.to).preventedJoinByTicket == False:
                                    hoax = client.getGroup(msg.to)
                                    hoax.preventedJoinByTicket = True
                                    client.updateGroup(hoax)
                                    client.sendMessage(
                                        msg.to, "Protect staff enabled.")
                                else:
                                    client.sendMessage(
                                        msg.to, "Protect staff enabled.")
                            else:
                                setting["proStaff"][msg.to] = True
                                jap = client.getGroup(msg.to)
                                setting["gname"][msg.to] = jap.name
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                if client.getGroup(msg.to).preventedJoinByTicket == False:
                                    hoax = client.getGroup(msg.to)
                                    hoax.preventedJoinByTicket = True
                                    client.updateGroup(hoax)
                                    client.sendMessage(
                                        msg.to, "Protect staff enabled.")
                                else:
                                    client.sendMessage(
                                        msg.to, "Protect staff enabled.")
                        elif protection == "none":
                            if msg.to not in protectStaff and msg.to not in protectMax:
                                client.sendMessage(
                                    msg.to, "Protection already disabled.")
                            else:
                                if msg.to in protectMax:
                                    del setting["proMax"][msg.to]
                                    with open('Data/settings.json', 'w') as fp:
                                        json.dump(
                                            setting, fp, sort_keys=True, indent=4)
                                    client.sendMessage(
                                        msg.to, "Protection disabled.")
                                else:
                                    if msg.to in protectStaff:
                                        del setting["proStaff"][msg.to]
                                        jap = client.getGroup(msg.to)
                                        setting["gname"][msg.to] = jap.name
                                        with open('Data/settings.json', 'w') as fp:
                                            json.dump(
                                                setting, fp, sort_keys=True, indent=4)
                                        client.sendMessage(
                                            msg.to, "Protection disabled.")


                    if cmd.startswith(".upbio: ") or cmd.startswith("upbio: "):
                        biograp = cmd.split("bio: ")[1]
                        if len(biograp) <= 100:
                            profile = client.getProfile()
                            profile.statusMessage = biograp
                            client.updateProfile(profile)
                            client.sendReplyMessage(
                                msg.id, msg.to, "Status bio updated to:\n{}".format(biograp))
                        else:
                            client.sendReplyMessage(
                                msg.id, msg.to, "Maximum 100 character.")

                    if cmd.startswith(".upname: ") or cmd.startswith("upname: "):
                        dname = cmd.split("upname: ")[1]
                        if len(dname) <= 100:
                            profile = client.getProfile()
                            profile.displayName = dname.title()
                            client.updateProfile(profile)
                            client.sendReplyMessage(
                                msg.id, msg.to, "Profile name updated to:\n{}".format(dname.title()))
                        else:
                            client.sendReplyMessage(
                                msg.id, msg.to, "Maximum 20 character.")

                    if cmd.startswith(".rname: ") or cmd.startswith("rname: "):
                        rnamed = cmd.split("name: ")[1]
                        setting["rname"] = rnamed
                        with open('Data/settings.json', 'w') as fp:
                            json.dump(setting, fp, sort_keys=True, indent=4)
                        client.sendReplyMessage(
                            msg.id, msg.to, "Rname updated to:\n{}".format(rnamed.title()))

                    if cmd == ".keykick" or cmd == "keykick":
                        client.sendFlexText(
                            to, "「   Usage   」\n.keykick: YOUR KEY\n.keykick: reset\n.keykick: cek")
                    if cmd.startswith(".keykick: ") or cmd.startswith("keykick: "):
                        kicked = cmd.split("kick: ")[1]
                        if kicked == "reset":
                            setting["keykick"] = ""
                            with open('Data/settings.json', 'w') as fp:
                                json.dump(
                                    setting, fp, sort_keys=True, indent=4)
                            client.sendReplyMessage(
                                msg.id, msg.to, "Key reseted")
                        elif kicked == "cek":
                            client.sendReplyMessage(
                                msg.id, msg.to, "Your key: {}".format(setting["keykick"]))
                        else:
                            setting["keykick"] = kicked
                            with open('Data/settings.json', 'w') as fp:
                                json.dump(
                                    setting, fp, sort_keys=True, indent=4)
                            client.sendReplyMessage(
                                msg.id, msg.to, "Key updated to:\n{}".format(kicked.title()))

                    if cmd.startswith(".leavemsg: ") or cmd.startswith("leavemsg: "):
                        data = cmd.split("msg: ")[1]
                        read["lmessage"] = data
                        client.sendMessage(
                            msg.to, "Leave message update to:\n{}".format(data))

                    if cmd.startswith(".welcomsg: ") or cmd.startswith("welcomsg: "):
                        data = cmd.split("msg: ")[1]
                        if msg.to in setting["welcome"]:
                            read["wmessage"][msg.to] = data
                            client.sendMessage(
                                msg.to, "Welcome message update to:\n{}".format(data))
                        else:
                            client.sendMessage(
                                msg.to, "Welcome message not active\nPlease enabled welcome first.")

                    if cmd.startswith(".gname: ") or cmd.startswith("gname: "):
                        gname = msg.text.split("name: ")[1]
                        g = client.getGroup(msg.to)
                        g.name = gname
                        client.updateGroup(g)
                        client.sendReplyMessage(
                            msg.id, msg.to, "Group updated to:\n{}".format(gname))

                    if cmd.startswith(".broadcast: ") or cmd.startswith("broadcast: "):
                        bc = cmd.split("broadcast: ")[1]
                        groups = client.getGroupIdsJoined()
                        allGc = client.getGroups(groups)
                        youBc = "「   Broadcast Message   」\nSender: @! \nSupport: https://{}\nBroadcasted: {} Groups\n────────────────\n{}".format(
                            host, len(allGc), bc)
                        for x in range(len(allGc)):
                            client.sendMention(allGc[x].id, youBc, [mid])
                        client.sendReplyMessage(
                            id, to, "Success Broadcasted on {} groups.".format(len(allGc)))

                    if cmd.startswith(".update") or cmd.startswith("updatepict"):
                        data = cmd.split("update")[1]
                        if data == "pict":
                            read["pp"] = True
                            client.sendMessage(msg.to, "send an image.")
                        elif data == "dual":
                            read["dual"] = True
                            client.sendMessage(msg.to, "send an video.")
                        elif data == "gpict":
                            read["gpict"][msg.to] = True
                            client.sendMessage(msg.to, "send an image.")

                if msg.contentType == 13:
                    target = msg.contentMetadata["mid"]
                    if read["addwhitelist"]:
                        if target != mid and target in setting["whitelist"]:
                            client.sendReplyMessage(
                                msg.to, "Already in whitelist")
                            read["addwhitelist"] = False
                        else:
                            if target not in setting["blacklist"]:
                                setting["whitelist"].append(target)
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMention(
                                    msg.to, "@!  added in whitelist.", [target])
                                read["addwhitelist"] = False
                            else:
                                client.sendMention(
                                    msg.to, "[Failed!]\n@! in blacklist.", [target])
                                read["addwhitelist"] = False

                    if read["delwhitelist"]:
                        if target != mid and target in setting["whitelist"]:
                            setting["whitelist"].remove(target)
                            with open('Data/settings.json', 'w') as fp:
                                json.dump(
                                    setting, fp, sort_keys=True, indent=4)
                            client.sendMention(
                                msg.to, "@!  removed from whitelist.", [target])
                            read["delwhitelist"] = False
                        else:
                            client.sendMention(
                                msg.to, "[Failed]\n@! not in whitelist.", [target])
                            read["delwhitelist"] = False

                    if read["addblacklist"]:
                        if target != mid and target in setting["blacklist"]:
                            client.sendReplyMessage(
                                msg.to, "Already in blacklist")
                            read["addblacklist"] = False
                        else:
                            if target not in setting["whitelist"]:
                                setting["blacklist"].append(target)
                                with open('Data/settings.json', 'w') as fp:
                                    json.dump(
                                        setting, fp, sort_keys=True, indent=4)
                                client.sendMention(
                                    msg.to, "@!  added in  blacklist.", [target])
                                read["addblacklist"] = False
                            else:
                                client.sendMention(
                                    msg.to, "[Failed!]\n@!  in whitelist.", [target])
                                read["addblacklist"] = False

                    if read["delblacklist"]:
                        if target != mid and target in setting["blacklist"]:
                            setting["blacklist"].remove(target)
                            with open('Data/settings.json', 'w') as fp:
                                json.dump(
                                    setting, fp, sort_keys=True, indent=4)
                            client.sendMention(
                                msg.to, "@!  removed from blacklist.", [target])
                            read["delblacklist"] = False
                        else:
                            client.sendMention(
                                msg.to, "[Failed]\n@!  not in blacklist.", [target])
                            read["delblacklist"] = False

                if msg.contentType == 2:
                    if read['dual']:
                        try:
                            client.downloadObjectMsg(
                                msg.id, 'path', 'video.mp4')
                            client.sendMessage(
                                msg.to, "Send picture to be profiled")
                            read['dual'] = False
                            read['dual2'] = True
                        except:
                            read['dual'] = True
                            client.sendMessage(
                                msg.to, "「  Failed  」\nPlease resend your video.")

                if msg.contentType == 1:
                    if msg.to in read["imgurl"]:
                        del read["imgurl"][msg.to]
                        try:
                            path = client.downloadObjectMsg(ids)
                            
                            main = data['result']
                            result = f"Image was converted :\n{main}"
                            client.sendReplyMessage(ids, to, result)
                        except Exception as e:
                            client.sendReplyMessage(ids, to, f"ERROR : {e}")
                            

                    if read['dual2']:
                        client.downloadObjectMsg(msg.id, 'path', 'foto.jpg')
                        client.updateProfileVideoPicture(
                            'video.mp4', 'foto.jpg')
                        client.sendMessage(
                            msg.to, 'Success change profile video.')
                        client.deleteFile('path')
                        read['dual2'] = False

                    if read["pp"]:
                        path = client.downloadObjectMsg(msg.id)
                        read["pp"] = False
                        client.updateProfilePicture(path)
                        client.deleteFile(path)
                        client.sendMessage(msg.to, "Profile image updated.")

                    if msg.to in read["gpict"]:
                        path = client.downloadObjectMsg(msg.id)
                        del read["gpict"][msg.to]
                        client.updateGroupPicture(msg.to, path)
                        client.deleteFile(path)
                        client.sendMessage(msg.to, "Group image updated.")

        except Exception as error:
            #ERROR = flex.ERROR(f"{error}")
            print(error)
            client.sendFlex(to, f"{error}")
            traceback.print_tb(error.__traceback__)    
                    # if cmd == ".uti":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/utility.txt', 'r').read()
                    #     client.center(msg.to, label, menu)

                    # if cmd == ".listing" or cmd == "listing":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/listing.txt', 'r').read()
                    #     client.center(msg.to, label, menu)

                    # if cmd == ".stealing" or cmd == "stealing":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/stealing.txt', 'r').read()
                    #     client.help(msg.to, label, menu)

                    # if cmd == ".group" :
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/groupset.txt', 'r').read()
                    #     client.help(msg.to, label, menu)

                    # if cmd == ".protect":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/protect.txt', 'r').read()
                    #     client.help(msg.to, label, menu)

                    # if cmd == ".cust":
                    #     if cmd.startswith('.'):
                    #         label = cmd.replace('.', '')
                    #     else:
                    #         label = cmd.replace(rname, "")
                    #     menu = open('help/customing.txt', 'r').read()
                    #     client.help(msg.to, label, menu)

        except Exception as e:
                client.sendMessage(msg.to, str(e))



def prostaff(op):
    try:
        if op.param3 in setting["whitelist"]:
            if op.param2 not in setting["whitelist"]:
                client.kickoutFromGroup(op.param1, [op.param2])
                client.findAndAddContactsByMid(op.param3)
                client.inviteIntoGroup(op.param1, [op.param3])
                if op.param2 not in setting["blacklist"]:
                    setting["blacklist"].append(op.param2)
                    with open('Data/settings.json', 'w') as fp:
                        json.dump(setting, fp, sort_keys=True, indent=4)
    except Exception as error:
        print(error)


def promax(op):
    try:
        if op.param2 not in setting["whitelist"]:
            client.kickoutFromGroup(op.param1, [op.param2])
            client.findAndAddContactsByMid(op.param3)
            client.inviteIntoGroup(op.param1, [op.param3])
            if op.param2 not in setting["blacklist"]:
                setting["blacklist"].append(op.param2)
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
    except Exception as e:
        print(e)


def proinvite(op):
    try:
        if op.param2 not in setting["whitelist"]:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except:
                pass
            mbul = client.getGroup(op.param1)
            no = 0
            for a in mbul.invitee:
                if a.mid in op.param3:
                    if no > 10:
                        pass
                    else:
                        try:
                            no = (no+1)
                            client.cancelGroupInvitation(op.param1, [a.mid])
                            time.sleep(0.04)
                        except:
                            pass
            for b in mbul.members:
                if b.mid in op.param3:
                    try:
                        client.kickoutFromGroup(op.param1, [b.mid])
                    except:
                        pass
            if op.param2 not in setting["blacklist"]:
                setting["blacklist"].append(op.param2)
                with open('Data/settings.json', 'w') as fp:
                    json.dump(setting, fp, sort_keys=True, indent=4)
        else:
            mbul = client.getGroup(op.param1)
            for a in mbul.invitee:
                if a.mid in op.param3:
                    if a.mid in setting["blacklist"]:
                        try:
                            client.cancelGroupInvitation(op.param1, [a.mid])
                            client.sendMessage(
                                msg.to, "Caution!, user in blacklist")
                        except:
                            pass
                    else:
                        pass
            for b in mbul.members:
                if b.mid in op.param3:
                    if b.mid in setting["blacklist"]:
                        try:
                            client.kickoutFromGroup(op.param1, [b.mid])
                        except:
                            pass
    except Exception as e:
        #logError(e)
        print(e)


def kekick(op):
    if op.param2 not in setting["whitelist"]:
        if op.param2 not in setting["blacklist"]:
            setting["blacklist"].append(op.param2)
            with open('Data/settings.json', 'w') as fp:
                json.dump(setting, fp, sort_keys=True, indent=4)


def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def liff():
    url = 'https://access.line.me/dialog/api/permissions'
    data = {'on': ['P', 'CM'], 'off': []}
    headers = {'X-Line-Access': client.authToken, 'X-Line-Application': client.server.APP_NAME,
               'X-Line-ChannelId': '1602876096', 'Content-Type': 'application/json'}
    requests.post(url, json=data, headers=headers)



def run():
    while True:
        try:
            Operation = ops.singleTrace(count=50)
            if Operation is not None:
                for op in Operation:
                    ops.setRevision(op.revision)
                    #self.OpInterrupt[op.type], args=(op,)
                    thread1 = threading.Thread(target=LINE_OP_TYPE, args=(op,))
                    thread1.start()
                    thread1.join()
                    #Lottovip()
                    #LottoRuay()
                    #LottoHuay()
                    #LottoJet()
        except Exception as e :
            client.log("「   ERROR 」\n{}".format(str(e)))
            traceback.print_tb(e.__traceback__)
            #logError(e)
        time.sleep(1)     


if __name__ == "__main__":
    run()
