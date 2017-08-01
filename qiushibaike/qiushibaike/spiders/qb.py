# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from qiushibaike.items import QiushibaikeItem

class QiushibaikeComSpider(scrapy.Spider):
    name = 'qb'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        for res in response.xpath("//div[@class='article block untagged mb15']"):
            qi = QiushibaikeItem()
            qi['content'] = (res.xpath('a/div[@class="content"]/span/text()').extract())[0]
            qi['funny'] = (res.xpath("div[@class='stats']/span[@class='stats-vote']/i/text()").extract())[0]
            comment = res.xpath("div[@class='stats']/span[@class='stats-comments']/a/i/text()").extract()
            if len(comment)== 0 :
                qi['comment'] = '0'
            else:
                qi['comment'] = comment[0]
            god = (res.xpath("a"))[-1].xpath("div/div/text()").extract()
            if len(god) == 0 :
                qi['god'] = ''
            else:
                qi['god'] = god[0].replace('\\n', '').replace('\\t', '').replace(u'：','').strip()

            with open('qb.txt','a') as f:
                line = qi['content'] + '\t' + qi['funny'] + '\t' + qi['comment'] + '\t' + qi['god'] + '\n'
                f.write(line.encode('utf-8'))
            

            yield qi

        for url in response.xpath("//a/@href").extract():
            yield scrapy.Request('http://' + self.allowed_domains[0] + url, callback=self.parse)

        # next_url = ((response.xpath("//ul[@class='pagination']/li/a/"))
        # yield scrapy.Request('https://' + self.allowed_domains[0] + next_url,callback=self.parse)

