# -*- coding: utf-8 -*-
import scrapy

import scrapy.cmdline

if __name__ == '__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'qbspider'])



class QbspiderSpider(scrapy.Spider):
    name = 'qbspider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/']
#     allowed_domains = ["dmoz.org"]
#     start_urls = [
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
#         "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
#     ]

    def parse(self, response):
        divs = response.xpath("//div[@class='article block untagged mb15 typs_hot']")
        for div in divs:
            author = div.xpath("//div[@class='author clearfix'/a[1]/h2/text()]").extract().encode('GB18030')
            contents = div.xpath("//div[@class='content']/span").extract().encode('GB18030')
#             content = ''
#             for con in contents:
#                 content = content + con
            with open('result.txt', 'rb') as f:
                f.write("---------" + author + "\n" + contents)
#         titles = response.xpath("//div[@class='author clearfix']/a/h2/text()").extract()
#         contents = response.xpath("//a[@class='contentHerf']/div/span/text()").extract()
#         filename = response.url.split("/")[-2]
#         with open(filename + '.txt', 'wb') as f:
#             for i in range(len(titles)): 
#                 f.write(str(i) + ':' + titles[i].encode('GB18030') + '\n' + contents[i].encode('GB18030') + "\n")
