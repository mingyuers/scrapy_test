#-*- coding: utf-8 -*-

from parse import ParseHtml
import sys
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

#设置遍历深度，防止报错：RuntimeError: maximum recursion depth exceeded
sys.setrecursionlimit(1000000)

urls = ['https://www.qiushibaike.com/']
# urls = ['https://www.qiushibaike.com/hot/']
pt = ParseHtml(urls)
pt.start()