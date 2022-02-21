#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/8 20:00
@Project:LofterSpider
@File:redisDB.py
@Desc:
"""
import redis


class RedisPool(object):

    def __init__(self, host: str, port: int, password: str, db: int):
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db, decode_responses=True)
        self.redis = redis.Redis(connection_pool=pool)

    def __del__(self):
        self.redis.connection_pool.disconnect()

if __name__ == '__main__':
    r = RedisPool("222.222.222.1",6379,"redis123",15)
    name = "weibo_blogFinished"
    print(r.redis.hget(name,"96d9252eb74efc8b5dca6d4663a7c800"))
    print(r.redis.hget(name,"ecb47bbe5b8621d4ae5951d6cda4d817"))
    print(r.redis.hget(name,"04d67167bace8b2893a33b613440a8bb"))
    print(r.redis.hget(name,"e2339df9c0ebaea3a6989bfe32c35bd8"))