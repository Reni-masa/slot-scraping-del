# 【slot-scraping】

# 基本機能
スロットデータの収集をwebスクレイピングを利用して行う個人用ツールです。

herokuを使用し、定時刻(23:30)にデータ収集を自動化。

スクレイピングしたデータに対して評価をし、一式のデータをDBにため込むというシンプルな機能。

# 使用技術
言語：python

ライブラリ：

DB：mysql

インフラ：heroku

# 構成図
![構成図](https://user-images.githubusercontent.com/46840997/103073699-66e80b80-460b-11eb-8566-cd2b3a2cb6ff.PNG)

# 今後の展開
・DBに格納したデータの参照機能は別アプリケーションとして作成。
>[analyze-to-slot(参照機能)](https://analyze-to-slot.herokuapp.com/slot/)
<img width="1440" alt="スクリーンショット 2021-03-07 22 46 22" src="https://user-images.githubusercontent.com/46840997/110241993-358aa500-7f97-11eb-850a-defe9ea454b5.png">

