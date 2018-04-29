# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CoinsmarketItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field()
    name = scrapy.Field()
    symbol = scrapy.Field()
    market_cap = scrapy.Field()
    price = scrapy.Field()
    supply = scrapy.Field()
    volume_24h = scrapy.Field()
    change_1h = scrapy.Field()
    change_24h = scrapy.Field()
    change_7d = scrapy.Field()


class coinItem(scrapy.Item):
    coin_data = scrapy.Field()
    time_series = scrapy.Field()
    # name = scrapy.Field()
    # price = scrapy.Field()
    # date_yyyymmdd = scrapy.Field()
    # open_p = scrapy.Field()
    # high_p = scrapy.Field()
    # low_p = scrapy.Field()
    # close_p = scrapy.Field()
    # volume = scrapy.Field()
    # market_cap = scrapy.Field()
