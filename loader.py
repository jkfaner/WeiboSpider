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
from database import MySQlPool, RedisPool
from utils.logger import logger
from utils.tool import load_json


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
    _mysqlClient = None
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
    def getMysqlClient(cls):
        if cls._mysqlClient is None:
            client = cls._database_config.get("mysql").get("client")
            cls._mysqlClient = MySQlPool(
                host=client.get("host"),
                port=client.get("port"),
                user=client.get("user"),
                password=client.get("password"),
                database=client.get("database")
            )
            logger.info("[mysql数据库连接池]:初始化成功->>> {} -> {}".format(client.get("host"), client.get("database")))
        return cls._mysqlClient

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
