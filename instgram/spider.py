# coding:utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import Queue
import sys,os
import requests

mainurl_queue = Queue.Queue()
imgurl_queue = Queue.Queue()
img_queue = Queue.Queue()

domain = 'https://www.instagram.com'

def parse_main_url():
    while not mainurl_queue.empty():
        browser = webdriver.Chrome('F:/chromedriver.exe')
        browser.set_window_size(50,50)
        print '正在翻页扫描图片,剩余',mainurl_queue.qsize(),'页'
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
                # with open('imgurl.txt','a+') as f:
                #     f.write(url+'\n')
            if re.findall('max_id',url):
                print 'mainurl',url
                # with open('mainurl.txt','a+') as f:
                #     f.write(url+'\n')
                mainurl_queue.put(url)
    parse_img_url()

def parse_img_url():
    while not imgurl_queue.empty():
        browser = webdriver.Chrome('F:/chromedriver.exe')
        browser.set_window_size(50, 50)
        print '正在保存图片url,剩余',imgurl_queue.qsize(),'条'
        url = imgurl_queue.get()
        browser.get(url)
        imgurl_queue.task_done()
        htmlSource = browser.page_source
        browser.close()
        soup = BeautifulSoup(htmlSource, 'lxml')
        imgs = soup.find_all('div',class_='_jjzlb')[0].find_all('img')
        for i in range(len(imgs)):
            url = imgs[i]['src']
            print url
            # with open('img.txt','a+') as f:
            #     f.write(url+'\n')
    download_img()


def download_img():
    while not img_queue.empty():
        print '剩余',img_queue.qsize(),'张图片'
        url = img_queue.get()
        # folder = os.getcwd()+'/liuyifeioff/'
        # if not os.path.exists(folder):
        #     os.makedirs(folder)
        r = requests.get(url)
        print '正在下载图片========',url
        path = 'bingbing_fan\\'+url.split('/')[-1]
        with open(path,'wb') as f:
            f.write(r.content)
        img_queue.task_done()

def main():
    url = 'https://www.instagram.com/bingbing_fan/'
    # url = 'https://www.instagram.com/bingbing_fan/?max_id=670016532071053971'
    mainurl_queue.put(url)
    parse_main_url()

# def save_img():
#     with open('imgurl.txt','r') as f:
#         lines = f.readlines()
#         for i in range(len(lines)):
#             line = lines[i].strip()
#             if line:
#                 imgurl_queue.put(line)
#     parse_img_url()
#
# def save_jpg():
#     with open('img.txt','r') as f:
#         lines = f.readlines()
#         for i in range(len(lines)):
#             line = lines[i].strip()
#             if line:
#                 img_queue.put(line)
#     download_img()



main()