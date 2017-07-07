#coding=utf-8

from PIL import Image
import requests
url = 'https://www.qiushibaike.com/text/page/35/?s=4998156'
print requests.get(url).text