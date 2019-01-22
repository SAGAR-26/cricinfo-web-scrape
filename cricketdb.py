import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import urllib.request
import lxml
from bs4 import BeautifulSoup
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='', db='cricket')
a = conn.cursor()
class client(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()


wiki = "http://www.espncricinfo.com/scores"
client_response = client(wiki)
source = client_response.mainFrame().toHtml()

soup = BeautifulSoup(source,features="lxml")
content= soup.prettify()
sp =BeautifulSoup(content,"lxml")

for items in soup.find_all(class_='cscore_details'):
    teamname = soup.find(class_='cscore_name cscore_name--long')
    score = soup.find(class_='cscore_score')

a.execute("INSERT INTO cric (teamname,score) VALUES (%s,%s)",(teamname.text,score.text))
conn.commit()
a.close()
conn.close()
print("success")

