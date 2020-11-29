# ページ取得
import requests
#DOM取得
from bs4 import BeautifulSoup
#ブラウザアクセス
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

import time
import individualScraping

def slot_main():
  search_lists = {"ツインドラゴンハナハナ":"https://p-ken.jp/p-kingkankosakaewakamiya/bonus/lot?model_nm=%C2%B2%DD%C4%DE%D7%BA%DE%DD%CA%C5%CA%C5-30&cost=20&ps_div=2&mode=",
                  "ハナハナ鳳凰":"https://p-ken.jp/p-kingkankosakaewakamiya/bonus/lot?model_nm=%CA%C5%CA%C5%CE%B3%B5%B3-30&cost=20&ps_div=2&mode=",
                  "プレミアムハナハナ":"https://p-ken.jp/p-kingkankosakaewakamiya/bonus/lot?model_nm=%CC%DF%DA%D0%B1%D1%CA%C5%CA%C5-30&cost=20&ps_div=2&mode="}

  for searchNama, searchUrl in search_lists.items():
    #開発環境path
    # DRIVER_PATH = '/Users/sugitamasataka/app/chromedriver/bin/chromedriver'
    #本番環境path
    DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    # ブラウザの起動
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    driver.get(searchUrl)

    # #待機
    driver.implicitly_wait(2) # 秒

    # #クリック回数保持
    selector = '#sort_graph > button'
    element = driver.find_element_by_css_selector(selector)
    click_times = int(element.get_attribute('data-max-page')) - 1

    # #最後までページを表示させる
    for i in range(click_times):
      element.click()
      time.sleep(2)

    # #ページソースを取得
    html = driver.page_source

    # #ブラウザ閉じる
    driver.close()
    driver.quit()

    soup = BeautifulSoup(html, "html.parser").encode("utf-8")

    # #個別URL全取得
    lists = soup.find_all("a", class_="select_lot_button")

    #https:を追加して配列に格納
    url_lists = []
    for list in lists:
      url_lists.append("https:" + list.get('href'))

    #台ごとに取得
    for url_list in url_lists:
      time.sleep(2)
      individualScraping.individualScraping(url_list,searchNama)
    
slot_main()









