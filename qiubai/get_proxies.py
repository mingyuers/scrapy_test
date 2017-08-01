#coding:utf-8
import requests
from bs4 import BeautifulSoup
import threading
import Queue
import time

class Get_ips():
    def __init__(self, page):
        self.ips = []
        self.urls_xici = []
        self.url_kuai = []
        for i in range(1,page+1):
            self.urls_xici.append("http://www.xicidaili.com/nn/" + str(i))
            self.urls_xici.append("http://www.xicidaili.com/nt/" + str(i))
            self.urls_xici.append("http://www.xicidaili.com/wn/" + str(i))
            self.urls_xici.append("http://www.xicidaili.com/wt/" + str(i))
        for i in range(1,page*3+1):
            self.url_kuai.append("http://www.kuaidaili.com/free/inha/" +str(i))
            self.url_kuai.append("http://www.kuaidaili.com/free/intr/" +str(i))
            self.url_kuai.append("http://www.kuaidaili.com/free/outha/" +str(i))
            self.url_kuai.append("http://www.kuaidaili.com/free/outtr/" +str(i))
            
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.q = Queue.Queue()
        self.Lock = threading.Lock()

    def get_ips(self):
        for url in self.urls_xici:
            time.sleep(0.5)
            res = requests.get(url, headers=self.header)
            soup = BeautifulSoup(res.text, 'lxml')
            ips = soup.find_all('tr')
            for i in range(1, len(ips)):
                ip = ips[i]
                tds = ip.find_all("td")
                ip_temp = tds[5].contents[0].lower() + "://" + tds[1].contents[0] + ":" + tds[2].contents[0]
                # print '===',str(ip_temp)
                self.q.put(str(ip_temp))

        for url in self.url_kuai:
            time.sleep(0.5)
            res = requests.get(url, headers=self.header)
            while res.text.strip()=='-10':
                res = requests.get(url, headers=self.header)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                ips = soup.find('tbody').find_all('tr')
                for i in range(len(ips)):
                    ip_temp = ips[i].find_all('td')[3].contents[0].lower()+'://'+ips[i].find_all('td')[0].contents[0]+':'+ips[i].find_all('td')[1].contents[0]
                    print '===',str(ip_temp) 
                    self.q.put(str(ip_temp))
            except Exception as e:
                print e

    def review_ips(self):
        time.sleep(0.1)
        while not self.q.empty():
            ip = self.q.get()
            try:
                proxy = {"http":ip}
                print proxy
                with requests.session() as s :
                    s.keep_alive = False
                    res = s.get("https://www.qiushibaike.com/", proxies=proxy, timeout=3)
                    html = res.text
                    soup = BeautifulSoup(html,'lxml')
                    # print html
                    print len(soup.find_all('div', class_='article block untagged mb15'))
                    # raw_input()
                    if (len(soup.find_all('div', class_='article block untagged mb15'))!=0) and (not html.__contains__("https://static.qiushibaike.com/qb_waf_403.png")) and (not html.__contains__('capInit(document.getElementById("TCaptcha"), capOption)')):
                        self.Lock.acquire()
                        self.ips.append(ip)
                        print ip,'succccccccccccccccccccccc'
                        with open('proxies.txt', 'a') as f:
                            f.write(str(proxy) + '\n')
                        self.Lock.release()
            except Exception,e:
                print e
            self.q.task_done()
            print self.q.qsize()

    def main(self):
        self.get_ips()
        threads = []
        for i in range(10):
            threads.append(threading.Thread(target=self.review_ips, args=[]))
        for t in threads:
            t.start()
            t.join()
        return self.ips

def get_ip():
    with open('proxies.txt','w') as f:
        f.write('')
    my=Get_ips(1)
    return my.main()

requests.adapters.DEFAULT_RETRIES = 5
# get_ip()
