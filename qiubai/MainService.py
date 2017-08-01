# coding=utf-8
from get_proxies import *
from spider import *
from Email import mail
import time, MySQLdb
from setting import *

start = True
flag = True

db = MySQLdb.connect(host='localhost', user=mysql_user, passwd=mysql_password, db='mycrawl', charset="utf8")
cursor = db.cursor()


def letsgo():
    stime = time.time()
    # get_ip()
    spiderGo()
    etime = time.time()
    d_hour = str(round((etime - stime) / 3600, 2))
    remain_links = getRemainUrlsLen()
    done_links = getDoneLinksLen()
    qiubai_len = getQiubaiLen()
    msg = "第一轮已跑完，耗时%s小时，共爬取%s条数据，共计%s个页面，爬取失败%s条链接，休息2小时。" % (d_hour, qiubai_len, done_links, remain_links)
    print msg
    if mail(msg):
        print '邮件发送成功'
    else:
        print '邮件发送失败'
    time.sleep(7200)


def getDoneLinksLen():
    sql = 'select url from links_qiubai'
    cursor.execute(sql)
    db.commit()
    cs = cursor.fetchall()
    return len(cs)


def getQiubaiLen():
    sql = 'select url from crawl_qiubai'
    cursor.execute(sql)
    db.commit()
    cs = cursor.fetchall()
    return len(cs)


def getRemainUrlsLen():
    sql = 'select url from links_todo'
    cursor.execute(sql)
    db.commit()
    cs = cursor.fetchall()
    return len(cs)


def alldone():
    remain_links = getRemainUrlsLen()
    done_links = getDoneLinksLen()
    qiubai_len = getQiubaiLen()
    msg = "全部已跑完，耗时%s小时，共爬取%s条数据，共计%s个页面，爬取失败%s条链接，休息2小时。" % (d_hour, qiubai_len, done_links, remain_links)
    if mail(msg):
        print '邮件发送成功'
    else:
        print '邮件发送失败'


def main():
    global flag
    global start
    while flag:
        stime = time.time()
        if getRemainUrlsLen <= 500 and (not start):
            etime = time.time()
            d_hour = str(round((etime - stime) / 3600, 2))
            remain_links = getRemainUrlsLen()
            done_links = getDoneLinksLen()
            qiubai_len = getQiubaiLen()
            msg = "全部已跑完，耗时%s小时，共爬取%s条数据，共计%s个页面，爬取失败%s条链接。恭喜您，糗事百科已通关。" % (
            d_hour, qiubai_len, done_links, remain_links)
            if mail(msg):
                print '邮件发送成功'
            else:
                print '邮件发送失败'
            flag = False
        else:
            letsgo()
        start = False


main()
