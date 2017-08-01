# coding=utf-8
import requests
import Queue
import threading
import time
from bs4 import BeautifulSoup

requests.adapters.DEFAULT_RETRIES = 5

url = 'https://www.qiushibaike.com/'
# url = 'http://101.200.42.84:5000/'
# url = 'http://pv.sohu.com/cityjson'
queue = Queue.Queue()

with open('proxies.txt', 'r') as f:
    for line in f.readlines():
        queue.put(line)

good_paoxies = []
flag = True


def test_url():
    proxy = eval(queue.get())
    print proxy
    with requests.Session() as s:
        try:
            html = s.get(url, proxies=proxy, timeout=10).text
            soup = BeautifulSoup(html,'lxml')
            if (not html.__contains__("https://static.qiushibaike.com/qb_waf_403.png")) and (not html.__contains__('capInit(document.getElementById("TCaptcha"), capOption)')):
                good_paoxies.append(proxy)
                print 'true'
            else:
                print 'false=============================='

            print len(soup.find_all('div', class_='article block untagged mb15'))
        except Exception as e:
            print e
        # raw_input()
        queue.task_done()
    if queue.qsize() == 0:
        print 'qsize:',queue.qsize()
        flag = False

def test_url_always():
    while flag:
        test_url()


for i in range(1):
    t = threading.Thread(target=test_url_always)
    t.start()


def save_file():
    if (queue.qsize() == 0):
        with open('proxies3.txt', 'w') as f:
            for p in good_paoxies:
                print p
                f.write(str(p) + '\n')

# ff = True
# while True:
#     time.sleep(1)
#     while ff:
#         if queue.qsize()==0:
#             save_file()
#             ff = False