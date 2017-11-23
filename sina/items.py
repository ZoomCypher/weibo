# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class InformationItem(Item):
    """ personal information"""
    _id = Field()                # ID
    NickName = Field()           # Nickname
    Gender = Field()             # gender
    Province = Field()           # Province
    City = Field()               # city
    BriefIntroduction = Field()  # introduction
    Birthday = Field()           # birth
    Num_Tweets = Field()         # weibo numbers
    Num_Follows = Field()        # follows
    Num_Fans = Field()           # fans
    SexOrientation = Field()     # sex orientation
    Sentiment = Field()          # affective states
    VIPlevel = Field()           # memebership lv.
    Authentication = Field()     # auth
    URL = Field()                # url


class TweetsItem(Item):
    """ tweets infomation"""
    _id = Field()                # user id- weibo id
    ID = Field()                 # user id
    Content = Field()            # content
    PubTime = Field()            # publish 
    Co_oridinates = Field()      # location
    Tools = Field()              # phone/platform
    Like = Field()               # thump up
    Comment = Field()            # comment
    Transfer = Field()           # reprint


class RelationshipsItem(Item):
    """ relationship """
    fan_id = Field()             # fans id
    followed_id = Field()        # followee id
