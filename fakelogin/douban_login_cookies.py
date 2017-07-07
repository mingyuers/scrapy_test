#coding=utf-8
import requests



cookies_str = 'bid=cOJvWteOxbU; __yadk_uid=v1lMBifEshCDsxBkpeC2zyvCnuOlSwVA; ct=y; ll="108296"; ps=y; _ga=GA1.2.1358058283.1498552520; _gid=GA1.2.1963167322.1499395798; dbcl2="143487885:/06kzpwkXnY"; ck=Ja50; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1499400121%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%22%5D; _pk_id.100001.8cb4=1355fcdc03b5c251.1498552520.6.1499400121.1499397940.; push_noty_num=0; push_doumail_num=0; __utma=30149280.1358058283.1498552520.1499396288.1499400122.6; __utmc=30149280; __utmz=30149280.1499400122.6.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.14348'

def list_cookies(cookies):
    list = {}
    cks = cookies.split(';')
    for ck in cks:
        k,v = ck.split('=',1)
        list[k] = v
    return list

cookies = list_cookies(cookies_str)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }
url = 'https://www.douban.com/people/143487885/'

r = requests.get(url,cookies = cookies,headers = headers)
print r.text.__contains__('kist')
