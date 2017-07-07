import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = 'dmoz_demo'
    allowed_domains = ['dmoztools.net']
    start_urls = [
        'http://dmoztools.net/Society/Philosophy/Aesthetics/'
    ]
    def parse(self, response):
        filename = self.name
        with open(self.name+'.txt','wb') as f:
            f.write(response.body)
        for res in response.xpath("//div[@class='site-item ']"):
            item = DmozItem()
            item['title'] = (res.xpath("div[@class='title-and-desc']/a/div/text()").extract())[0]
            item['link'] = 'http://'+self.allowed_domains[0] + (res.xpath("div[@class='site-flag']/a/@href").extract())[0]
            des = (res.xpath("div[@class='title-and-desc']/div[@class='site-descr ']/text()").extract())[0]
            item['desc'] = des.replace(' ','').replace('\\r','').replace('\\n','').replace('\\t','').strip()
            with open('items'+'.txt','a') as f :
                f.write('title:\t'+item['title'] +'\nlink:\t'+item['link']+'\ndesc:\t'+item['desc']+'\n\n')
            yield item
