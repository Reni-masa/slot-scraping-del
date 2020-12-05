# ページ取得
import requests
#DOM取得
from bs4 import BeautifulSoup

import MySQLdb
import os
import registration

#herokuに接続用
# import pymysql
# import pymysql.cursors

def individualScraping(search_url, search_name):
  getPage = requests.get(search_url)
  mainsoup = BeautifulSoup(getPage.content, "html.parser")

  #Db接続
  try:
    #本番DB(本番上げるときコメントアウト解除)
    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    conn = MySQLdb.connect(user=DB_USERNAME, passwd=DB_PASSWORD, host=DB_HOSTNAME, db=DB_NAME, charset="utf8")
    
    #ローカルDB(本番上げるときコメントアウト)
    # conn = MySQLdb.connect(user='root', passwd='root', host='localhost', db='slot_DB')
    
    conn = conn.cursor()

  except MySQLdb.Error as ex:
    print('MySQL Error: ', ex)
  
  #機種id取得
  sql = "SELECT id FROM slot_information WHERE slot_name = '{slot_name}'".format(slot_name=search_name)
  try:
    conn.execute(sql)
    print("①===========")
    slot_id = conn.fetchone() #機種ID取得
    print("②===========")
    slot_id = slot_id[0]
    print("slot_id：",slot_id) #問題切り分け　todo 削除
  finally:
    conn.close()

  #代番号取得
  element = mainsoup.select_one("#store_page > div > div.title_container2 > div > ul > li:nth-child(2)")
  number = element.text
  number = number.replace(" ","") #空白削除
  number = number.replace("台番","") #数字のみに変換

  #slotData取得
  elements = mainsoup.select("#store_page > div > div.bonus_summary2.card-content > div.row > div.col-md-2")
  bb_val = 0
  rb_val = 0
  bb_ave = ""
  rb_ave = ""
  total_game = 0
  bonus_average = ""

  for element in elements:
    elem = element.prettify()

    #BB RBとかの名前取得
    soup = BeautifulSoup(elem, "html.parser")
    dataName = soup.find('div').contents[0]
    dataName = dataName.replace('\n',"") #改行削除
    dataName = dataName.replace(" ","") #空白削除
    
    #BB RBの数値取得
    soup = BeautifulSoup(elem, "html.parser")
    dataNum = soup.find('span').text
    dataNum = dataNum.replace('\n',"") #改行削除
    dataNum = dataNum.replace(" ","") #空白削除

    if dataName == "BB":
      bb_val = dataNum
    elif dataName == "RB":
      rb_val = dataNum
    elif dataName == "総回転数":
      total_game = dataNum
    elif dataName == "BB確率":
      bb_ave = dataNum
    elif dataName == "RB確率":
      rb_ave = dataNum
    elif dataName == "合成確率":
      bonus_average = dataNum

  setting_class = setting_judgement(bb_ave,rb_ave,bonus_average)

  registration.registration(slot_id, number, bb_val, rb_val, bb_ave, rb_ave, total_game, bonus_average,setting_class)

#設定判別
def setting_judgement(bb_ave,rb_ave,bonus_average):
  bb_ave = slash_replace(bb_ave)
  rb_ave = slash_replace(rb_ave)
  bonus_average = int(slash_replace(bonus_average))

  if bonus_average <= 189:
    setting = 1
    if bonus_average <= 181:
      setting = 2
      if bonus_average <= 171:
        setting = 3
        if bonus_average <= 161:
          setting = 4
          if bonus_average <= 151:
            setting = 5
            if bonus_average <= 138:
              setting = 6
              if bonus_average == 0:
                setting = 1
  else:
    setting = 1

  return setting

def slash_replace(replace_data):
  slashPosition = replace_data.find("/")
  slashPosition += 1
  data = replace_data[slashPosition:]
  return data
