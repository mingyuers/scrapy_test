#coding=utf-8

import requests
cookies_str = '_qqq_uuid_=2|1:0|10:1499700816|10:_qqq_uuid_|56:YmJhNTNjNzdjYTVjZjU2YTQwMTZjYTdkODk1YzQ3NDUyOTJmYjQzMA==|3c6503f6bbf3e714f596ff9c50fba54921b26fceb9e31b1b259c863397d9896e; FTAPI_BLOCK_SLOT=FUCKIE; FTAPI_ST=FUCKIE; Hm_lvt_18a964a3eb14176db6e70f1dd0a3e557=1499737221; __cur_art_index=5500; FTAPI_Source=www.qiushibaike.com/joke/; _xsrf=2|77f7c5bb|9e3f9bb49a8a654838b84f91b3d33c66|1499831805; _HY_CTK_747691ed591b462da60e407f234f3a3a=90ef429c73dc377bf69628cd4dc4fcd2; _gat=1; _qqq_user_id=33996349; FTAPI_ASD=1; FTAPI_PVC=1026761-6-j50znnls; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1499700810,1499732388,1499782636,1499831806; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1499834120; _ga=GA1.2.730153594.1499700812; _gid=GA1.2.1075381948.1499700812; callback_url=/'

def list_cookies(cookies):
    list = {}
    cks = cookies.split(';')
    for ck in cks:
        k,v = ck.split('=',1)
        list[k] = v
    return list

cookies = list_cookies(cookies_str)
print cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
    }
url = 'https://www.qiushibaike.com/users/33996349/'
r = requests.get(url,headers = headers,cookies = cookies)
print r.text