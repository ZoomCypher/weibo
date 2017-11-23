# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient  
from scrapy.conf import settings  
from scrapy import log
from sina.items import RelationshipsItem, TweetsItem, InformationItem

class MongoDBPipeline(object):
    
    def __init__(self):
        connection = MongoClient(  
           settings[ 'MONGODB_SERVER' ],  
           settings[ 'MONGODB_PORT' ]  
        )  
        db = connection[settings[ 'MONGODB_DB' ]] 

        self.Information = db[settings[ 'MONGODB_COLLECTION_INFOMATION' ]]
        self.Tweets = db[settings['MONGODB_COLLECTION_TWEETS']]
        self.Relationships = db[settings['MONGODB_COLLECTION_RELATIONSHIPS']]

    def process_item(self, item, spider):
        """
        judge & insert
        """
        if isinstance(item, RelationshipsItem):
            try:
                self.Relationships.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        return item
