# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from pymongo import MongoClient
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    # def process_item(self, item, spider):
    #     self.collection.insert(dict(item))
    #     log.msg("Item wrote to MongoDB database %s/%s" %
    #             (settings['MONGODB_DB'],
    #              settings['MONGODB_COLLECTION']),
    #             level=log.DEBUG, spider=spider)
    #     return item

    def process_item(self, item, spider):
        # valid = True
        date = item["time_series"]
        name = item['coin_data']['name']
        date_query = "time_series." + str(date)
        valid_check = self.collection.find(
            {"coin_data.name": name, date_query: {"$exists": True}}).count()
        if valid_check == 0:
            # self.collection.insert(dict(item))
            self.collection.update(
                {"coin_data.name": name}, {"$addToSet": {date_query: date}})
            log.msg("Entries updated!",
                    level=log.DEBUG, spider=spider)
        else:
            raise DropItem("Existed {0}!".format(date))
        return item
