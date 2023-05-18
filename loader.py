#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/15 11:18
@Project:WeiboSpider
@File:loader.py
@Desc:加载器
"""
import os

from database import RedisPool
from utils import constants
from utils.logger import logger
from utils.tool import load_json, parse_user


class ProjectLoader(object):
    print("""
         _          __  _____   _   _____   _____        _____   _____   _   _____   _____   _____   
        | |        / / | ____| | | |  _  \ /  _  \      /  ___/ |  _  \ | | |  _  \ | ____| |  _  \  
        | |  __   / /  | |__   | | | |_| | | | | |      | |___  | |_| | | | | | | | | |__   | |_| |  
        | | /  | / /   |  __|  | | |  _  { | | | |      \___  \ |  ___/ | | | | | | |  __|  |  _  /  
        | |/   |/ /    | |___  | | | |_| | | |_| |       ___| | | |     | | | |_| | | |___  | | \ \  
        |___/|___/     |_____| |_| |_____/ \_____/      /_____/ |_|     |_| |_____/ |_____| |_|  \_\ 
    """)
    logger.info("程序正在初始化...")
    _redisClient = None
    _system_config = load_json("./src/resource/system-config.json")

    _spider_config = _system_config.get("spider")
    _database_config = _system_config.get("database")
    _system_config = _system_config.get("system")

    @classmethod
    def getSpiderConfig(cls):
        return cls._spider_config

    @classmethod
    def getDatabaseConfig(cls):
        return cls._database_config

    @classmethod
    def getSystemConfig(cls):
        return cls._system_config

    @classmethod
    def getRedisClient(cls):
        if cls._redisClient is None:
            client = cls._database_config.get("redis")
            cls._redisClient = RedisPool(
                host=client.get("host"),
                port=client.get("port"),
                password=client.get("password"),
                db=client.get("db"),
            ).redis
            logger.info("[redis数据库连接池]:初始化成功->>> {} -> {}".format(client.get("host"), client.get("db")))
        return cls._redisClient


class FilterFactory:
    filter_config = ProjectLoader.getSpiderConfig().get("filter")

    @classmethod
    def filter_blog(cls):
        return cls.filter_config.get("filter-blog")

    @classmethod
    def filter_user(cls):
        return cls.filter_config.get("filter-user")

    @classmethod
    def filter_type(cls):
        return cls.filter_config.get("filter-type")

    @classmethod
    def original_user(cls):
        return cls.filter_config.get("original")

    @classmethod
    def forward_user(cls):
        return cls.filter_config.get("forward")

    @classmethod
    def get_filterUser(cls):
        original_users = parse_user(cls.original_user())
        forward_users = parse_user(cls.forward_user())
        filter_type = cls.filter_type()
        if filter_type == constants.BLOG_FILTER_ORIGINAL:
            users = list(set(original_users))
        elif filter_type == constants.BLOG_FILTER_FORWARD:
            users = list(set(forward_users))
        else:
            original_users.extend(forward_users)
            users = list(set(original_users))
        return users


class DownloadLoader(object):
    _spider_config = ProjectLoader.getSpiderConfig()
    _database_config = ProjectLoader.getDatabaseConfig()
    _redis_client = ProjectLoader.getRedisClient()

    def __init__(self):
        self.root_path = self._spider_config["download"]["root"]
        self.redis_client = self._redis_client
        self.thread = self._spider_config["download"]["thread"]
        self.workers = self._spider_config["download"]["workers"]
        # 创建weibo专属路径
        self.rootPath = os.path.join(self.root_path, "weibo")
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)
