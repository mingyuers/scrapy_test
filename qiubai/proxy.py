# _*_coding:utf-8_*_
import random
import MySQLdb
import sys
reload(sys)
# sys.setdefaultencoding('utf-8')

class Proxy(object):
    def changeProxy(self):
        with open('proxies.txt','r') as f:
            lines = f.readlines()
            line = random.choice(lines)
            return line.strip()

# p = Proxy()
# print p.getProxy()


# db = MySQLdb.connect(host='localhost',user='root',passwd='root',db='mycrawl',charset="utf8")
# db.autocommit(1)
# cursor = db.cursor()
# sql = 'insert into links_qiubai(imgurl) values(%s)'
# print sql
# print cursor.execute(sql,"发")