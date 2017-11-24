#!/usr/bin/env python
# encoding: utf-8

import requests
import json
import redis
import logging
import random
from .settings import REDIS_URL

logger = logging.getLogger(__name__)

WeiBoAccounts = [
# {'username': xxxx, 'password': xxxx},

]




# ##获取Cookie
# def get_cookie(cookiesPool):
       
#     cookie = cookiesPool.pop()
#     logger.warning("获取Cookie成功！（账号为:%s）" % account)
#     return json.dumps(cookies)


# def init_cookie(reds, spidername):
#     redkeys = reds.keys()
#     for user in redkeys:
#         password = reds.get(user)
#         if red.get("%s:Cookies" % (spidername)) is None:
#             cookie = get_cookie()
#             red.set("%s:Cookies"% (spidername), cookie)


# def update_cookie(red, accountText, spidername):
#     red = redis.Redis()
#     pass

# def remove_cookie(red, spidername, accountText):
#     #red = redis.Redis()
#     red.delete("%s :Cookies: %s" % (spidername, accountText))
