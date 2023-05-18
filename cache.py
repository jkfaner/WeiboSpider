#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/18 21:41
@Project:WeiboSpider
@File:cache.py
@Desc:
"""
import json

from loader import DownloadLoader
from utils import constants
from utils.tool import get_time_now


class RedisCache(DownloadLoader):

    def insert_weibo_screen_name(self, uid: str, screen_name: str):
        """
        插入博主用户名
        :param uid: uid
        :param screen_name: 用户名
        :return:
        """
        former_name_item = self.select_weibo_former_name(uid)
        former_names = former_name_item["list"]
        if screen_name not in former_names:
            former_names.append(screen_name)
        former_name_item['size'] = len(former_names)
        inset_data = json.dumps(former_name_item, ensure_ascii=False)
        self.redis_client.hset(constants.REDIS_SPIDER_USER_FORMER_NAME, uid, inset_data)

    def select_weibo_former_name(self, uid: str) -> dict:
        """
        获取博主曾用名
        :param uid:
        :return:
        """
        former_name_item = self.redis_client.hget(constants.REDIS_SPIDER_USER_FORMER_NAME, uid)
        if former_name_item:
            return json.loads(former_name_item)
        return dict(list=list(), size=0)

    def select_weibo_user(self, uid: str):
        """
        查询数据库微博用户
        :param uid:
        :return:
        """
        return self.redis_client.hget(constants.REDIS_SPIDER_USER_NAME, uid)

    def update_weibo_user(self, uid: str, screen_name: str):
        """
        插入数据&更新数据 数据库有数据就写入 没数据就跟行 weibo_id为唯一索引
        :param uid:
        :param screen_name:
        :return:
        """
        self.redis_client.hset(constants.REDIS_SPIDER_USER_NAME, uid, screen_name)

    def record_finished(self, key: str, value: str):
        """
        记录完成
        :param key: 哈希值
        :param value: 内容
        :return:
        """
        self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=key, value=value)

    def record_spider_time(self, uid: str):
        """
        记录时间
        :param uid: uid
        :return:
        """
        self.redis_client.hset(name=constants.REDIS_SPIDER_USER_START, key=uid, value=get_time_now())

    def get_spider_time(self, uid):
        """
        获取记录时间
        :param uid: uid
        :return:
        """
        return self.redis_client.hget(name=constants.REDIS_SPIDER_USER_START, key=uid)

    def record_error(self, key: str, value: str):
        """
        记录错误
        :param key: 哈希值
        :param value: 内容
        :return:
        """
        self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=key, value=value)

    def check_finished(self, key):
        """
        检查是否完成
        :param key: 哈希值
        :return:
        """
        return self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=key)

    def check_error(self, key):
        """
        检查是否异常
        :param key: 哈希值
        :return:
        """
        return self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=key)

    def record_complete(self, uid: str):
        """
        记录全量下载完成
        :param uid: uid
        :return:
        """
        self.redis_client.sadd(constants.REDIS_SPIDER_USER_FULL, uid)

    def get_complete(self):
        """
        获取全量下载用户
        :return:
        """
        return [i for i in self.redis_client.sscan_iter(name=constants.REDIS_SPIDER_USER_FULL)]


class Cache(RedisCache):
    pass
