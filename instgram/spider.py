# coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import Queue

mainurl_queue = Queue.Queue()
imgurl_queue = Queue.Queue()
img_queue = Queue.Queue()

domain = 'https://www.instagram.com'

def parse_main_url():
    while mainurl_queue.not_empty():
        browser = webdriver.Chrome('F:/chromedriver.exe')
        url = mainurl_queue.get()
        browser.get(url)
        mainurl_queue.task_done()
        htmlSource = browser.page_source
        browser.close()
        soup = BeautifulSoup(htmlSource,'lxml')
        urls = soup.find_all('a')
        for i in range(len(urls)):
            url = domain + urls[i]['href']
            if re.findall('taken-by',url):
                print 'imgurl',url
                imgurl_queue.put(url)
                with open('imgurl.txt','a+') as f:
                    f.write(url+'\n')
            if re.findall('max_id',url):
                print 'mainurl',url
                with open('mainurl.txt','a+') as f:
                    f.write(url+'\n')
                mainurl_queue.put(url)

def parse_img_url():
    while imgurl_queue.not_empty:
        browser = webdriver.Chrome('F:/chromedriver.exe')
        url = imgurl_queue.get()
        browser.get(url)
        imgurl_queue.task_done()
        htmlSource = browser.page_source
        browser.close()
        print htmlSource
        soup = BeautifulSoup(htmlSource, 'lxml')
        imgs = soup.find_all('div',class_='_jjzlb')[0].find_all('img')
        for i in range(len(imgs)):
            url = imgs[i]['src']
            print url
            with open('img.txt','a+') as f:
                f.write(url+'\n')


def main():
    url = 'https://www.instagram.com/liuyifeioff/'
    mainurl_queue.put(url)
    parse_main_url()

def save_img():
    with open('imgurl.txt','r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line:
                imgurl_queue.put(line)
    parse_img_url()

save_img()