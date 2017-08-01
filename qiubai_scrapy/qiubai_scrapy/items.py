# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiScrapyItem(scrapy.Item):
    content = scrapy.Field()
    funny = scrapy.Field()
    comment = scrapy.Field()
    god = scrapy.Field()
