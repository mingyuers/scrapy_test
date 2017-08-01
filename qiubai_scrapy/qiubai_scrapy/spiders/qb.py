# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiubai_scrapy.items import QiubaiScrapyItem


class QbSpider(scrapy.Spider):
    name = 'qb'
    allowed_domains = ['runoob.com']
    start_urls = ['http://www.runoob.com/redis/redis-tutorial.html']

    # rules = (
    #     Rule(LinkExtractor(allow=r'/text/page/\d.'),callback = 'parse_item', follow=True),
    # )

    def parse_item(self, response):
        qi = QiubaiScrapyItem()
        # for res in response.xpath("//div[@class='article block untagged mb15']"):
            
        #     qi['content'] = (res.xpath('a/div[@class="content"]/span/text()').extract())[0]
        #     qi['funny'] = (res.xpath("div[@class='stats']/span[@class='stats-vote']/i/text()").extract())[0]
        #     comment = res.xpath("div[@class='stats']/span[@class='stats-comments']/a/i/text()").extract()
        #     if len(comment)== 0 :
        #         qi['comment'] = '0'
        #     else:
        #         qi['comment'] = comment[0]
        #     god = (res.xpath("a"))[-1].xpath("div/div/text()").extract()
        #     if len(god) == 0 :
        #         qi['god'] = ''
        #     else:
        #         qi['god'] = god[0].replace('\\n', '').replace('\\t', '').replace(u'：','').strip()

        #     with open('qb.txt','a') as f:
        #         line = qi['content'] + '\t' + qi['funny'] + '\t' + qi['comment'] + '\t' + qi['god'] + '\n'
        #         f.write(line.encode('utf-8'))
        qi['comment'] = response.text
        qi['god'] = '666'
        yield qi
