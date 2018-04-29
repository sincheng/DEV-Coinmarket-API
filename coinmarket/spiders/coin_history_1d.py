# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import dateparser
from ..convert_functions import convertNumber, convertDate
from ..items import coinItem


class CoinHistorySpider(scrapy.Spider):
    name = 'coinhistory_1d'
    allowed_domains = ['coinmarketcap.com/']
    start_urls = ['https://coinmarketcap.com/coins/']

    def parse(self, response):
        url = "https://coinmarketcap.com"
        today = datetime.date.today().strftime('%Y%m%d')
        day_ago = datetime.date.today() - datetime.timedelta(days=1)
        day_ago = day_ago.strftime('%Y%m%d')
        table = response.xpath('//table')
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            link = tr.xpath('.//td[2]/a/@href').extract_first()
            rank = tr.xpath('.//td[1]/text()').extract_first()
            name = tr.xpath('.//td[2]/a/text()').extract_first()
            symbol = tr.xpath(
                './/td[2]/span/a/text()').extract_first()
            # Get all data
            coin_url = url + link + "historical-data/?start=" + \
                day_ago + "&end=" + today
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
            open_p = tr.xpath('.//td[2]/text()').extract_first()
            high_p = tr.xpath('.//td[3]/text()').extract_first()
            low_p = tr.xpath('.//td[4]/text()').extract_first()
            close_p = tr.xpath('.//td[5]/text()').extract_first()
            volume = tr.xpath('.//td[6]/text()').extract_first()
            market_cap = tr.xpath('.//td[7]/text()').extract_first()
            item["time_series"][convertDate(date)] = {
                "open_p": convertNumber(open_p, float),
                "high_p": convertNumber(high_p, float),
                "low_p": convertNumber(low_p, float),
                "close_p": convertNumber(close_p, float),
                "volume": convertNumber(volume, int),
                "market_cap": convertNumber(market_cap, int)
            }
        yield item

#
# Dict = {"Coin Data":  , "Time Series Data"}
# Dict["coin_data"] = {"Name":name , "Symbol":symbol}
# Dict["Time Series Data"] = {"Date": Dict["Time Series Data"]["20180228"] }
# Dict["Time Series Data"]["20180228"] = { "Open":11,"Close":9}
