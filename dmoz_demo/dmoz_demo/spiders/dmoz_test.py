# -*- coding: utf-8 -*-
import scrapy
from dmoz_demo.items import DmozItem

class DmozTestSpider(scrapy.Spider):
    name = 'dmoz_test'
    allowed_domains = ['dmoztools.net']
    start_urls = ['http://dmoztools.net']

    def parse(self, response):
        if 'title-and-desc' in response.body:
            for res in response.xpath("//div[@class='site-item ']"):
                item = DmozItem()
                item['title'] = (res.xpath("div[@class='title-and-desc']/a/div/text()").extract())[0]
                item['link'] = 'http://' + self.allowed_domains[0] + \
                               (res.xpath("div[@class='site-flag']/a/@href").extract())[0]
                des = (res.xpath("div[@class='title-and-desc']/div[@class='site-descr ']/text()").extract())[0]
                item['desc'] = des.replace(' ', '').replace('\\r', '').replace('\\n', '').replace('\\t', '').strip()
                with open('items' + '.txt', 'a') as f:
                    f.write('title:\t' + item['title'] + '\nlink:\t' + item['link'] + '\ndesc:\t' + item['desc'] + '\n\n')
                yield item

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request('http://' + self.allowed_domains[0] + url, callback=self.parse)


        # title = response.xpath('//title/text()').extract()[0]
        # if title == 'DMOZ - World: Chinese Simplified':
        #     for url in response.xpath('//div[@class="cat-item"]/a/@href').extract():
        #         yield scrapy.Request('http://'+self.allowed_domains[0] + url, callback=self.parse)
        # else:
        #     if 'title-and-desc' not in response.body:
        #         for url in response.xpath('//div[@class="cat-item"]/a/@href').extract():
        #             yield scrapy.Request('http://'+self.allowed_domains[0] + url, callback=self.parse)
        #     else:
        #         for res in response.xpath("//div[@class='site-item ']"):
        #             item = DmozItem()
        #             item['title'] = (res.xpath("div[@class='title-and-desc']/a/div/text()").extract())[0]
        #             item['link'] = 'http://' + self.allowed_domains[0] + \
        #                            (res.xpath("div[@class='site-flag']/a/@href").extract())[0]
        #             des = (res.xpath("div[@class='title-and-desc']/div[@class='site-descr ']/text()").extract())[0]
        #             item['desc'] = des.replace(' ', '').replace('\\r', '').replace('\\n', '').replace('\\t', '').strip()
        #             with open('items' + '.txt', 'a') as f:
        #                 f.write('title:\t' + item['title'] + '\nlink:\t' + item['link'] + '\ndesc:\t' + item[
        #                     'desc'] + '\n\n')
        #             yield item
