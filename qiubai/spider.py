# coding=utf-8
import random
import time
from items import QbItem
import logging
import requests
from bs4 import BeautifulSoup
import traceback
import MySQLdb
import Queue
import threading
import urllib3
import re
from Email import mail
from setting import *

import objgraph

urllib3.disable_warnings()

# cookies_str = '_qqq_uuid_=2|1:0|10:1499700816|10:_qqq_uuid_|56:YmJhNTNjNzdjYTVjZjU2YTQwMTZjYTdkODk1YzQ3NDUyOTJmYjQzMA==|3c6503f6bbf3e714f596ff9c50fba54921b26fceb9e31b1b259c863397d9896e; FTAPI_BLOCK_SLOT=FUCKIE; FTAPI_ST=FUCKIE; Hm_lvt_18a964a3eb14176db6e70f1dd0a3e557=1499737221; __cur_art_index=5500; FTAPI_Source=www.qiushibaike.com/joke/; _xsrf=2|77f7c5bb|9e3f9bb49a8a654838b84f91b3d33c66|1499831805; _HY_CTK_747691ed591b462da60e407f234f3a3a=90ef429c73dc377bf69628cd4dc4fcd2; _gat=1; _qqq_user_id=33996349; FTAPI_ASD=1; FTAPI_PVC=1026761-6-j50znnls; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1499700810,1499732388,1499782636,1499831806; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1499834120; _ga=GA1.2.730153594.1499700812; _gid=GA1.2.1075381948.1499700812; callback_url=/'
# def list_cookies(cookies):
#     list = {}
#     cks = cookies.split(';')
#     for ck in cks:
#         k,v = ck.split('=',1)
#         list[k] = v
#     return list
# cookies = list_cookies(cookies_str)

logging.basicConfig(filename='crawl.log', level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', filemode='a')

# avaliable_str = {'/joke'}
# avaliable_str = {'/8hr','/hot','/imgrank','/text','/history','/pic','textnew','/page'}
pattern = re.compile(r'/joke/\d*/')

local_proxies = []

domain = 'https://www.qiushibaike.com'
user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# todo_links = []
done_links = []
q_todo = Queue.Queue()
q_lock = threading.Lock()


def parse(html, db, cursor):
    soup = BeautifulSoup(html, 'lxml')
    objs = soup.find_all('div', class_='article block untagged mb15')
    for obj in objs:
        qbi = QbItem()
        tag = obj['id']
        qbi.tag = tag
        # print tag,'tag'
        url = obj.find('a', class_='contentHerf')['href']
        qbi.url = url
        # print url,'url'
        content = obj.find('div', class_='content').get_text().strip().encode('utf-8')
        qbi.content = content
        # print content,'content'
        imgurl = obj.find('div', class_='thumb')
        if imgurl:
            imgurl = 'http:' + imgurl.find('a').find('img').get('src').encode('utf-8')
        else:
            imgurl = ''
        qbi.imgurl = imgurl
        # print imgurl
        funny = obj.find('span', class_='stats-vote').find('i', class_='number').get_text().encode('utf-8')
        qbi.funny = funny
        # print funny, 'funny'
        comment = obj.find('span', class_='stats-comments').find('i', class_='number')
        if comment:
            comment = comment.get_text().encode('utf-8')
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
        sql = "insert into crawl_qiubai (tag,url,content,imgurl,funny,comment,god,godnum) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,
                       [str(qbi.tag), str(qbi.url), str(qbi.content), str(qbi.imgurl), str(qbi.funny), str(qbi.comment),
                        str(qbi.god), str(qbi.godnum)])
        db.commit()
    for link in soup.find_all('a'):
        link = link.get('href')
        if aviliableLink(link):
            print link
            q_todo.put(domain + link)
            time.sleep(0.01)


def downloadalways():
    while not q_todo.empty():
        download()


def download():
    objgraph.show_growth()
    if True:
        db = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password, db='mycrawl', charset="utf8")
        cursor = db.cursor()
        url = q_todo.get()
        if url in done_links:
            print '去重6666666666', url
            q_todo.task_done()
        else:
            print 'url:', url, '---shengyu:', q_todo.qsize(), time.strftime('%Y-%m-%d %H:%M:%S',
                                                                            time.localtime(time.time()))
            headers = getheaders()
            proxy = changeProxy()
            print proxy
            with requests.session() as s:
                try:
                    q_lock.acquire()
                    r = s.get(url, headers=headers, proxies=proxy, allow_redirects=False, verify=False, timeout=10)
                    # print r.text
                    # print r.headers
                    status_code = r.status_code
                    soup = BeautifulSoup(r.text, 'lxml')
                    # print 'lenlenlen',len(soup.find_all('div', class_='article block untagged mb15'))
                    if (not len(soup.find_all('div',
                                              class_='article block untagged mb15')) == 0) and status_code == 200 and (
                    not r.text.__contains__("https://static.qiushibaike.com/qb_waf_403.png")):
                        parse(r.text, db, cursor)
                        sql = 'insert into links_qiubai(url) values(%s)'
                        print cursor.execute(sql, [url])
                        db.commit()
                    else:
                        sql = 'insert into links_todo(url) values(%s)'
                        print cursor.execute(sql, [url])
                        db.commit()
                    done_links.append(url)
                    q_todo.task_done()
                    q_lock.release()
                    logging.debug('status_code= %s ,url = %s' % (str(status_code), url))
                    print 'download----------', url, '----', status_code
                    delay = getDelay()
                    print 'waiting.....', delay
                    time.sleep(delay)
                except Exception as e:
                    q_todo.put(url)
                    q_todo.task_done()
                    print 'traceback===:'
                    traceback.print_exc()
                    logging.error('Exception:' + str(e) + '--' + repr(e))
    print '====================================='
    objgraph.show_growth()


# 符合规则，且不重复
def aviliableLink(link):
    if not link:
        return False
    if link in done_links:
        return False
    if pattern.match(link):
        return True
    else:
        return False


        # avaliable_str = {'/8hr','/hot','/imgrank','/text','/history','/pic','textnew','/page'}
        # avaliable_str = {'/joke'}
        # if link and (not link.startswith('http')) and link != '/':
        #     for str in avaliable_str:
        #         if str in link:
        #             return True
        # return False


def getheaders():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Host': 'www.qiushibaike.com',
        'User-Agent': changeAgent()
    }
    return headers


def getDelay():
    return round(random.random() * 6, 6) + 1.0


def changeProxy():
    if len(local_proxies) == 0:
        return {}
    else:
        line = random.choice(local_proxies)
        return line


def loadProxy():
    with open('proxies.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() != '':
                local_proxies.append(eval(line.strip()))
                # print local_proxies


def changeAgent():
    ua = random.choice(user_agent_list)
    if ua:
        return ua
    else:
        return user_agent_list[0]


def loadDoneUrls():
    db = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password, db='mycrawl', charset="utf8")
    cursor = db.cursor()
    sql = 'select url from links_qiubai'
    cursor.execute(sql)
    db.commit()
    for c in cursor.fetchall():
        done_links.append(c[0])


def loadLastUrls():
    db = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password, db='mycrawl', charset="utf8")
    cursor = db.cursor()
    sql = 'select url from links_todo'
    cursor.execute(sql)
    db.commit()
    cs = cursor.fetchall()
    for c in cs:
        q_todo.put(c[0])
    print 'loadLastUrls--', q_todo.qsize()
    sql2 = 'delete from links_todo'
    db.commit()


def spiderGo():
    loadProxy()
    loadLastUrls()
    loadDoneUrls()
    q_todo.put("https://www.qiushibaike.com/joke/624797/")
    for i in range(1):
        t = threading.Thread(target=downloadalways, args=())
        t.start()
        t.join()



        # q_todo.put("http://127.0.0.1:5000/")
        # while True:
        #     time.sleep(0.5)
        #     ls = todo_links
        #     if not len(ls)==0:
        #         for l in ls:
        #             q_todo.put(domain+l)
        #             todo_links.remove(l)
