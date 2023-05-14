#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/19 19:32
@Project:WeiboSpider
@File:init.py
@Desc:项目初始化
"""
from database.mysqlDB import MySQlPool
from database.redisDB import RedisPool

from utils.logger import logger
from utils.tool import load_json

logger.info("程序正在初始化...")
SystemInfo = load_json("./src/resource/system-info.json")
SystemDB = load_json("./src/resource/system-db.json")
SystemSQL = load_json("./src/resource/system-sql.json")
SpiderSetting = load_json("./src/resource/spider-setting.json")

_mysql = SystemDB.get("mysql")
mysqlPool = MySQlPool(
    host=_mysql.get("host"),
    port=_mysql.get("port"),
    user=_mysql.get("user"),
    password=_mysql.get("password"),
    database=_mysql.get("database")
)
logger.info("[mysql数据库连接池]:初始化成功->>> {} -> {}".format(_mysql.get("host"), _mysql.get("database")))

_redis = SystemDB.get("redis")
redisPool = RedisPool(
    host=_redis.get("host"),
    port=_redis.get("port"),
    password=_redis.get("password"),
    db=_redis.get("db"),
).redis
logger.info("[redis数据库连接池]:初始化成功->>> {} -> {}".format(_redis.get("host"), _redis.get("db")))