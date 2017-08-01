# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['xd-ganggeban.com']
    start_urls = ['http://www.xd-ganggeban.com/']

    def parse(self, response):
        self.logger.info("parse_page: %r" % response)
