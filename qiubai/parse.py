#-*- coding: utf-8 -*-
from agent import UserAgent
from proxy import Proxy
import requests
import time
from bs4 import BeautifulSoup
from items import QbItem
import MySQLdb
import threading


class ParseHtml(UserAgent,Proxy):
    def __init__(self,urls=[],delay=0.8):
        self.urls = urls
        self.delay = delay
        self.domain = 'https://www.qiushibaike.com'
        self.urls_down = []
        self.db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='mycrawl',charset="utf8")
        # self.db.autocommit(1)
        self.cursor = self.db.cursor()

    def start(self):
        for url in self.urls:
            self.download(url)

    def downloadThread(self,url):
        t = threading.Thread(target=self.download,args=(url,))
        t.start()

    def download(self,url):
        if url not in self.urls_down:
            print 'download===========',url
            # time.sleep(self.delay)
            headers = self.getheaders()
            proxy = {"http": super(ParseHtml,self).changeProxy()}
            # print proxy
            r = requests.get(url, headers=headers,proxies=proxy)
            self.urls_down.append(url)
            status_code = r.status_code
            if status_code == 200:
                print 'download----------', status_code
                sql = 'insert into links_qiubai(url) values(%s)'
                self.cursor.execute(sql,url)
                self.db.commit()
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
                self.parse(soup)
            else:
                print 'download----------',status_code
                pass

    def parse(self,soup):
        objs = soup.find_all('div', class_='article block untagged mb15')
        for obj in objs:
            qbi = QbItem()
            content = obj.find('div', class_='content').get_text().strip().encode('utf-8')
            qbi.content = content
            # print content,'content'
            imgurl = obj.find('div',class_='thumb')
            if imgurl:
                imgurl ='http:' + imgurl.find('a').find('img').get('src').encode('utf-8')
            else:
                imgurl = ''
            qbi.imgurl = imgurl
            # print imgurl
            funny = obj.find('span', class_='stats-vote').find('i').get_text().encode('utf-8')
            qbi.funny = funny
            # print funny, 'funny'
            comment = obj.find('span', class_='stats-comments').find('a')
            if comment:
                comment = comment.find('i').get_text().encode('utf-8')
            else:
                comment = '0'
            qbi.comment = comment
            # print comment, 'comment'
            god = obj.find('div', class_='main-text')
            if god:
                godnum = god.find('div', class_='likenum').text.strip().encode('utf-8')
                god = god.text.strip().replace(u'：', '').replace('\n', '').replace(godnum, '').encode('utf-8')
            else:
                god = ''
                godnum = '0'
            qbi.god = god
            qbi.godnum = godnum
            # print god, 'god'
            # print godnum, 'godnum'
            # with open('result.txt','a') as f:
            #     line = content+'\t'+imgurl+"\t"+'funny'+'\t'+comment+'\t'+god+'\t\n'
            #     f.write(line.encode('utf-8'))
            print self.handle_data(qbi)
        print len(soup.find_all('a'))
        for link in soup.find_all('a') :
            link = link.get('href')
            if self.aviliableLink(link):
                1
                # print 'after==',link
                self.download(self.domain+link)

    def aviliableLink(self,link):
        # print 'befor==',link
        avaliable_str = {'/8hr','/hot','/imgrank','/text','/history','pic','textnew','/joke','/page'}
        if link and (not link.startswith('http')) and link != '/':
            for str in avaliable_str:
                if str in link:
                    return True
                    break;
        return False

    def getheaders(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.qiushibaike.com',
            'User-Agent': super(ParseHtml, self).changeAgent()
        }
        # print headers
        return headers

    def handle_data(self,qbi):
        sql = "insert into crawl_qiubai (content,imgurl,funny,comment,god,godnum) values (%s,%s,%s,%s,%s,%s)"
        # sql = "insert into crawl_qiubai(content,imgurl,funny,comment,god,godnum) values(%s,%s,%s,%s,%s,%s)"
        # print sql
        print self.cursor.execute(sql,[str(qbi.content),str(qbi.imgurl),str(qbi.funny),str(qbi.comment),str(qbi.god),str(qbi.godnum)])
        self.db.commit()