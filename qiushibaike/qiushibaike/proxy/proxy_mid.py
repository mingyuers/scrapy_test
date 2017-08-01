import random
import scrapy
import os
import time

class ProxyMiddleWare(object):
    def process_request(self,request,spider):
        proxy = self.get_random_proxy()
        print("this is request ip:" + proxy)
        # request.meta['proxy'] = str(proxy)
        request.meta['proxy'] = 'http://122.72.32.72:80'

    # def process_response(self,request,response,spider):
    #     if response.status != 200:
    #         proxy = self.get_random_proxy()
    #         print "this is response ip:"+proxy
    #         # request.meta['proxy'] = str(proxy)
    #         request.meta['proxy'] = 'http://122.72.32.72:80'
    #         return request
    #     return response

    def get_random_proxy(self):
        while 1:
            with open(os.getcwd()+'/proxy/proxies.txt','r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        return proxy