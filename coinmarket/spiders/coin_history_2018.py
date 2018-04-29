# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import dateparser
from ..convert_functions import convertNumber, convertDate
from ..items import coinItem


class CoinHistorySpider(scrapy.Spider):
    name = 'coinhistory_2018'
    allowed_domains = ['coinmarketcap.com/']
    start_urls = ['https://coinmarketcap.com/coins/']

    def parse(self, response):
        today = datetime.datetime.today().strftime('%Y%m%d')
        url = "https://coinmarketcap.com"
        table = response.xpath('//table')
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            link = tr.xpath('.//td[2]/a/@href').extract_first()
            rank = int(tr.xpath('.//td[1]/text()').extract_first())
            name = tr.xpath('.//td[2]/a/text()').extract_first()
            symbol = tr.xpath(
                './/td[2]/span/a/text()').extract_first()
            # Get all data
            coin_url = url + link + "historical-data/?start=20180101&end=" + today
            yield scrapy.Request(coin_url, callback=self.parse_history, meta={'name': name, 'symbol': symbol}, dont_filter=True)

    def parse_history(self, response):
        table = response.xpath('//table')
        trs = table.xpath('.//tr')[1:]
        item = coinItem()
        item['coin_data'] = {
            'name': response.meta['name'], 'symbol': response.meta['symbol']}
        item['time_series'] = {}
        for tr in trs:
            date = tr.xpath('.//td[1]/text()').extract_first()
            date_ = convertDate(date)
            open_p = tr.xpath('.//td[2]/text()').extract_first()
            high_p = tr.xpath('.//td[3]/text()').extract_first()
            low_p = tr.xpath('.//td[4]/text()').extract_first()
            close_p = tr.xpath('.//td[5]/text()').extract_first()
            volume = tr.xpath('.//td[6]/text()').extract_first()
            market_cap = tr.xpath('.//td[7]/text()').extract_first()

            item["time_series"][date_] = {
                "open_p": convertNumber(open_p, float),
                "high_p": convertNumber(high_p, float),
                "low_p": convertNumber(low_p, float),
                "close_p": convertNumber(close_p, float),
                "volume": convertNumber(volume, int),
                "market_cap": convertNumber(market_cap, int)
            }
        yield item
