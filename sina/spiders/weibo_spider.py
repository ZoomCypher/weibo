#!/usr/bin/env python
# encoding: utf-8

import logging
import datetime
import requests
import re
from lxml import etree
from scrapy import Spider
from scrapy.http import Request
from sina.seedUrls import weiboID
from scrapy.selector import Selector
# from sina.scrapy_redis.spiders import RedisSpider
from scrapy_redis.spiders import RedisSpider
from sina.items import TweetsItem, InformationItem, RelationshipsItem


class Spider(RedisSpider):
    name = "sinaSpider"
    host = "https://weibo.cn"

    redis_key = "weibo_spider:start_urls"
    start_urls = list(set(weiboID))

    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)

    def parse_information(self, response):
        """
        functions:
           1. catch basic informations
           2. catch the number of tweets, follows, fans
           3. request tweets as a corpus
           4. request follows to make a loop for crawling all worthly user
           5. request fans for analyzing the relationship 
        """
        informationItem = InformationItem()
        ID = re.findall('(\d+)/info', response.url)[0]
        try:
            # all infomation
            basicInfo = ';'.join(response.xpath('//div[@class="c"]/text()').extract())
            # id
            informationItem["_id"] = ID
            # nickname
            if re.findall('昵称[：:]?(.*?);', basicInfo):
                nickname = re.findall('昵称[：:]?(.*?);', basicInfo)
                informationItem["NickName"] = nickname[0].replace(u"\xa0", "")
            # gender
            if re.findall('性别[：:]?(.*?);', basicInfo):
                gender = re.findall('性别[：:]?(.*?);', basicInfo)
                informationItem["Gender"] = gender[0].replace(u"\xa0", "")
            # place
            if re.findall('地区[：:]?(.*?);', basicInfo):
                place = re.findall('地区[：:]?(.*?);', basicInfo)[0].replace(u"\xa0", "").split(" ")
                informationItem["Province"] = place[0]
                if len(place) > 1:
                    informationItem["City"] = place[1]
            # briefIntroduction
            if re.findall('简介[：:]?(.*?);', basicInfo):
                briefIntroduction = re.findall('简介[：:]?(.*?);', basicInfo)
                informationItem["BriefIntroduction"] = briefIntroduction[0].replace(u"\xa0", "")
            # birthday or Sign
            if re.findall('生日[：:]?(.*?);', basicInfo):
                birthday = re.findall('生日[：:]?(.*?);', basicInfo)
                try:
                    birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                    informationItem["Birthday"] = birthday - datetime.timedelta(hours=8)
                except Exception:
                    # maybe zodiac
                    informationItem['Birthday'] = birthday[0]
            # sexOrientaion
            if re.findall('性取向[：:]?(.*?);', basicInfo):
                sexOrientation = re.findall('性取向[：:]?(.*?);', basicInfo)
                if sexOrientation[0].replace(u"\xa0", "") == gender[0]:
                    informationItem["SexOrientation"] = "同性恋"
                else:
                    informationItem["SexOrientation"] = "异性恋"
            # sentiment
            if re.findall('感情状况[：:]?(.*?);', basicInfo):
                sentiment = re.findall('感情状况[：:]?(.*?);', basicInfo)
                informationItem["Sentiment"] = sentiment[0].replace(u"\xa0", "")
            # vipLevel
            if re.findall('会员等级[：:]?(.*?);', basicInfo):
                vipLevel = re.findall('会员等级[：:]?(.*?);', basicInfo)
                informationItem["VIPlevel"] = vipLevel[0].replace(u"\xa0", "")
            # authentication
            if re.findall('认证[：:]?(.*?);', basicInfo):
                authentication = re.findall('认证[：:]?(.*?);', basicInfo)
                informationItem["Authentication"] = authentication[0].replace(u"\xa0", "")
            # url
            if re.findall('互联网[：:]?(.*?);', basicInfo):
                url = re.findall('互联网[：:]?(.*?);', basicInfo)
                informationItem["URL"] = url[0]
           
            # get Tweets, Follows, Fans 
            try:
                tweet_url = "https://weibo.cn/attgroup/opening?uid=%s" % ID
                r = requests.get(tweet_url, cookies=response.request.cookies, timeout = 5)
                if r.status_code == 200:
                    selector = etree.HTML(r.content)
                    data = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
                    if data:
                        num_tweets = re.findall('微博\[(\d+)\]', data)
                        num_follows = re.findall('关注\[(\d+)\]', data)
                        num_fans = re.findall('粉丝\[(\d+)\]', data)
                        if num_tweets:
                            informationItem["Num_Tweets"] = int(num_tweets[0])
                        if num_follows:
                            informationItem["Num_Follows"] = int(num_follows[0])
                        if num_fans:
                            informationItem["Num_Fans"] = int(num_fans[0])
            except Exception as e:
                self.logger.info(e)
                pass
        except Exception as e:
            self.logger.info(e)
            pass
        else:
            print(informationItem)
            yield informationItem
        # filter worthless data
        if int(num_tweets[0]) < 5000:
            yield Request(url="https://weibo.cn/%s/profile?filter=1&page=1" % ID, callback=self.parse_tweets, dont_filter=True)
        if int(num_follows[0]) < 500:
            yield Request(url="https://weibo.cn/%s/follow" % ID, callback=self.parse_relationship, dont_filter=True)
        if int(num_fans[0]) < 500:
            yield Request(url="https://weibo.cn/%s/fans" % ID, callback=self.parse_relationship, dont_filter=True)

    def parse_tweets(self, response):
        """
        functions:
           1. catch each tweet
           2. request next page if existed
        """
        ID = re.findall('(\d+)/profile', response.url)[0]
        divs = response.xpath('body/div[@class="c" and @id]')
        for div in divs:
            try:
                tweetsItems = TweetsItem()
                # _id and ID 
                id = div.xpath('@id').extract_first()
                tweetsItems["_id"] = ID + "-" + id
                tweetsItems["ID"] = ID
                # content
                if div.xpath('div/span[@class="ctt"]//text()').extract():
                    content = div.xpath('div/span[@class="ctt"]//text()').extract()
                    content = " ".join(content).strip('[位置]').strip()
                    # parse content
                    tweetsItems["Content"] = content.replace(u"\u200b", "").replace(u"\xa0 全文", "")
                # coordinates
                if div.xpath('div/a/@href').extract():
                    cooridinates = div.xpath('div/a/@href').extract()
                    cooridinates = re.findall('center=([\d.,]+)', cooridinates[0])
                    if cooridinates:
                        tweetsItems["Co_oridinates"] = cooridinates[0]
                # like
                if re.findall('赞\[(\d+)\]', div.extract()):
                    like = re.findall('赞\[(\d+)\]', div.extract())
                    tweetsItems["Like"] = int(like[0])
                # transfer
                if re.findall('转发\[(\d+)\]', div.extract()):
                    transfer = re.findall('转发\[(\d+)\]', div.extract()) 
                    tweetsItems["Transfer"] = int(transfer[0])
                # comment:
                if re.findall('评论\[(\d+)\]', div.extract()):
                    comment = re.findall('评论\[(\d+)\]', div.extract())
                    tweetsItems["Comment"] = int(comment[0])
                # date and equipments/platform
                if div.xpath('div/span[@class="ct"]/text()').extract():
                    others = div.xpath('div/span[@class="ct"]/text()').extract()
                    others = others[0].split('来自')
                    tweetsItems["PubTime"] = others[0].replace(u"\xa0", "")
                    if len(others) == 2:
                        tweetsItems["Tools"] = others[1].replace(u"\xa0", "")
                
                print(tweetsItems)
                yield tweetsItems
            except Exception as e:
                self.logger.info(e)
                pass
        # request next page
        next_url = "https://weibo.cn" + response.xpath("//div[@class='pa']/form/div/a[1]/@href").extract()
        if next_url:
            yield Request(url=next_url[0], callback=self.parse_tweets, dont_filter=True)
        

    def parse_relationship(self, response):
        """
        functions:
           1. parse followees, fans
           2. pull out followees' id to request a new user
           3. parse relationship
        """
        if "/follow" in response.url:
            ID = re.findall('(\d+)/follow', response.url)[0]
            flag = True
        else:
            ID = re.findall('(\d+)/fans', response.url)[0]
            flag = False
        urls = response.xpath('//a[text()="关注他" or text()="关注她"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        for uid in uids:
            relationshipsItem = RelationshipsItem()
            relationshipsItem["fan_id"] = ID if flag else uid
            relationshipsItem["followed_id"] = uid if flag else ID
            yield relationshipsItem 
            yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_information)

        next_url = "https://weibo.cn" + response.xpath("//div[@class='pa']/form/div/a[1]/@href").extract()
        if next_url:
            yield Request(url=next_url[0], callback=self.parse_relationship, dont_filter=True)

