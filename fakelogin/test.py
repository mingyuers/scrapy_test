#coding=utf-8

from PIL import Image
import requests
import re
from bs4 import BeautifulSoup


url = 'https://www.qiushibaike.com/'
response = requests.get(url).text
soup = BeautifulSoup(response,'lxml')
objs =  soup.find_all('div',class_='article block untagged mb15')
obj = objs[0]

for obj in objs:
    content = obj.find('div', class_='content').get_text()
    print content
    funny = obj.find('span', class_='stats-vote').find('i').get_text()
    print funny, 'funny'
    comment = obj.find('span', class_='stats-comments').find('a')
    if comment:
        comment = comment.find('i').get_text()
    else:
        comment = '0'
    print comment, 'comment'
    god = obj.find('div', class_='main-text')
    if god:
        godnum = god.find('div',class_='likenum').text.strip()
        god = god.text.strip().replace(u'：','').replace('\n','').replace(godnum,'')
    else:
        god = ''
        godnum = '0'
    print god, '=========god'
    print godnum,'-----godnum'

# print obj.find('span',class_='stats-comments').find('a').find('i').get_text()

# str = re.findall(re.compile(r'.*'),obj.find('div',class_='content'))
# print str