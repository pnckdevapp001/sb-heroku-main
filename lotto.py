# import os
# import traceback
# import sys
# import json
# import ast
# import requests
# import re
# import random
# import pytz
# import schedule
# import time
# from datetime import datetime
# from bs4 import BeautifulSoup

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# _session = requests.session()


# # Fetch the service account key JSON file contents
# cred = credentials.Certificate('serviceAccountKey.json')

# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://pnck-dev-app-default-rtdb.asia-southeast1.firebasedatabase.app'
# })

# Lotto_ref = db.reference('LOTTODATA/')


# def saveDataLotto(label, textData):
#     Lotto_ref.child(label+'/').set({
#     label: {
#         'text': textData
#     }
# })


# def getDataLotto(label):
#     snapshot = Lotto_ref.child(label+'/'+label).get()
#     return snapshot["text"]


# def remove(string):
#     pattern = re.compile(r'\s+')
#     # pattern = re.compile(r'รอบที่ บน-ล่าง รายละเอียด')
#     return re.sub(pattern, ',', string)


# def Lottovip():
#     url = "https://www.ballsod55.com/tmp/bailek/lottoshuay.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all('table', {"class": "table table-striped"})
#     label = "lottovip"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         regexT = r'\d{3}'
#         roundNowLotto = "ผลหวยยี่กี จาก ʟᴏᴛᴛᴏᴠɪᴘ\n"+textdata[28]+"ที่ "+textdata[29]+"\n❸ ตัวบน "+textdata[31] + \
#             "\n❷ ตัวล่าง " + textdata[32]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[37]+" "+textdata[38] + " 🔸 3บน : " + textdata[40] + " | 2ล่าง : " + textdata[41] +\
#             "\n"+textdata[46]+" "+textdata[47] + " 🔸 3บน : " + textdata[49] + " | 2ล่าง : " + textdata[50] +\
#             "\n"+textdata[55]+" "+textdata[56] + " 🔸 3บน : " + textdata[58] + " | 2ล่าง : " + textdata[59] +\
#             "\n"+textdata[64]+" "+textdata[65] + " 🔸 3บน : " + textdata[67] + " | 2ล่าง : " + textdata[68] +\
#             "\n"+textdata[73]+" "+textdata[74] + " 🔸 3บน : " + textdata[76] + " | 2ล่าง : " + textdata[77] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         # print(roundNowLotto)
#     dataget = getDataLotto(label)
#     # print(dataget)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     if re.match(regexT, textdata[31]):
#         if roundNowLotto != dataget:
#             SaveLottoData = saveDataLotto(label, roundNowLotto)
#             # return client.center(toGroup, label, roundNowLotto)
#             print("OK_"+label.upper())
#         else:
#           print("DUB_"+label.upper())
#     else:
#         print("RUN_"+label.upper())


# def LottoHuay():
#     url = "https://formula.aapsite.com/stock1huayresult.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all(
#         'table', {"class": "table responsive table-bordered table-sm"})
#     label = "huay"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         # print(textdata)
#         roundNowLotto = "ผลหวยยี่กี จาก HUAY\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
#             "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
#             "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
#             "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
#             "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
#             "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         # print(roundNowLotto)
#     #dataget = getDataLotto(label)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     #try:
#       #if roundNowLotto != dataget:
#     SaveLottoData = saveDataLotto(label, roundNowLotto)
#          #client.center(toGroup, label, roundNowLotto)
#     print("OK_"+label.upper())
#     #except Exception as error:
#         #print(error)


# def LottoRuay():
#     url = "https://www.ballsod55.com/tmp/bailek/ruayshuay.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all('table', {"class": "table table-striped"})
#     label = "ruay"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         regexT = r'\d{3}'
#         roundNowLotto = "ผลหวยยี่กี จาก 𝐑𝐮𝐚𝐲𝐬𝐇𝐮𝐚𝐲\n"+textdata[28]+"ที่ "+textdata[29]+"\n❸ ตัวบน "+textdata[31] + \
#             "\n❷ ตัวล่าง " + textdata[32]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[37]+" "+textdata[38] + " 🔸 3บน : " + textdata[40] + " | 2ล่าง : " + textdata[41] +\
#             "\n"+textdata[46]+" "+textdata[47] + " 🔸 3บน : " + textdata[49] + " | 2ล่าง : " + textdata[50] +\
#             "\n"+textdata[55]+" "+textdata[56] + " 🔸 3บน : " + textdata[58] + " | 2ล่าง : " + textdata[59] +\
#             "\n"+textdata[64]+" "+textdata[65] + " 🔸 3บน : " + textdata[67] + " | 2ล่าง : " + textdata[68] +\
#             "\n"+textdata[73]+" "+textdata[74] + " 🔸 3บน : " + textdata[76] + " | 2ล่าง : " + textdata[77] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         #print(roundNowLotto)        
#     #dataget = getDataLotto(label)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     #if re.match(regexT, textdata[31]):
#         #if roundNowLotto != dataget:
#     SaveLottoData = saveDataLotto(label,roundNowLotto)
#             #client.center(toGroup, label, roundNowLotto)
#     print("OK_"+label.upper())
#        # else:
#           #print("DUB_"+label.upper())
#    #else:
#         #print("RUN_"+label.upper())

# def LottoJet():
#     url = "https://formula.aapsite.com/stock1jetsadabetresult.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all(
#         'table', {"class": "table responsive table-bordered table-sm"})
#     label = "jetsadabet"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         # print(textdata)
#         roundNowLotto = "ผลหวยยี่กี จาก JETSADABET\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
#             "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
#             "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
#             "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
#             "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
#             "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         # print(roundNowLotto)
#     #dataget = getDataLotto(label)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     #try:
#       #if roundNowLotto != dataget:
#     SaveLottoData = saveDataLotto(label, roundNowLotto)
#          #client.center(toGroup, label, roundNowLotto)
#     print("OK_"+label.upper())
#     #except Exception as error:
#         #print(error)

# def Lotto2lottovip():
#     url = "https://formula.aapsite.com/stock1lottovipresult.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all(
#         'table', {"class": "table responsive table-bordered table-sm"})
#     label = "2lottovip"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         # print(textdata)
#         roundNowLotto = "ผลหวยยี่กี จาก LOTTOVIP\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
#             "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
#             "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
#             "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
#             "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
#             "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         # print(roundNowLotto)
#     #dataget = getDataLotto(label)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     #try:
#       #if roundNowLotto != dataget:
#     SaveLottoData = saveDataLotto(label, roundNowLotto)
#          #client.center(toGroup, label, roundNowLotto)
#     print("OK_"+label.upper())
#     #except Exception as error:
#         #print(error)

# def Lotto2ruay():
#     url = "https://formula.aapsite.com/stock1ruayresult.php"
#     content = requests.get(url)
#     content.encoding = "utf-8"
#     soup = BeautifulSoup(content.text, 'html.parser')
#     tags = soup.find_all(
#         'table', {"class": "table responsive table-bordered table-sm"})
#     label = "2ruay"
#     for tag in tags:
#         textdata = remove(tag.get_text()).split(',')
#         # print(textdata)
#         roundNowLotto = "ผลหวยยี่กี จาก RUAY\n"+textdata[6]+" "+textdata[7]+"\n❸ ตัวบน "+textdata[10] + \
#             "\n❷ ตัวล่าง " + textdata[12]+"\n----- ย้อนหลัง -----" + \
#             "\n"+textdata[15]+" "+textdata[16] + " 🔸 3บน : " + textdata[19] + " | 2ล่าง : " + textdata[21] +\
#             "\n"+textdata[24]+" "+textdata[25] + " 🔸 3บน : " + textdata[28] + " | 2ล่าง : " + textdata[30] +\
#             "\n"+textdata[33]+" "+textdata[34] + " 🔸 3บน : " + textdata[37] + " | 2ล่าง : " + textdata[39] +\
#             "\n"+textdata[42]+" "+textdata[43] + " 🔸 3บน : " + textdata[46] + " | 2ล่าง : " + textdata[48] +\
#             "\n"+textdata[51]+" "+textdata[52] + " 🔸 3บน : " + textdata[55] + " | 2ล่าง : " + textdata[57] +\
#             "\n-----------------------\n   🎲 พื้นที่ว่าง ให้เช่าโฆษณา\n-----------------------"
#         # print(roundNowLotto)
#     #dataget = getDataLotto(label)
#     toGroup = 'c28b23fb070c90a0d42d8f444e61d47b2'
#     #try:
#       #if roundNowLotto != dataget:
#     SaveLottoData = saveDataLotto(label, roundNowLotto)
#          #client.center(toGroup, label, roundNowLotto)
#     print("OK_"+label.upper())
#     #except Exception as error:
#         #print(error)
# Lotto2ruay()