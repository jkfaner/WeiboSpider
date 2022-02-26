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

    def disconnect(self):
        self.redis.connection_pool.disconnect()