import MySQLdb
import datetime
import os

#herokuに接続用
# import pymysql
# import pymysql.cursors

def registration(slot_id, slot_number, bb_val, rb_val, bb_ave, rb_ave, total_game, bonus_ave,setting_class):

  #Db接続
  try:
    #本番DB(本番上げるときコメントアウト解除)
    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    conn = MySQLdb.connect(user=DB_USERNAME, passwd=DB_PASSWORD, host=DB_HOSTNAME, db=DB_NAME)
    
    #ローカルDB(本番上げるときコメントアウト)
    # conn = MySQLdb.connect(user='root', passwd='root', host='localhost', db='slot_DB')

    cursor = conn.cursor()

  except MySQLdb.Error as ex:
    print('MySQL Error: ', ex)

  today = datetime.date.today()
  #slotdataインサート
  sql = "INSERT INTO slot_game_data(number,BB,RB,BB_average,RB_average,total_game,bonus_average,class,date_time,user_id,store_id,slot_id) " \
          "VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  try:
    cursor.execute(sql,(slot_number,bb_val,rb_val,bb_ave,rb_ave,total_game,bonus_ave,setting_class,today,1,1,slot_id))
    
    cursor.close()
    conn.commit()
    conn.close()
  except MySQLdb.Error as ex:
    print('MySQL Error: ', ex)
    cursor.close()
    conn.close()
