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
from config.load import load_mysqlInfo, load_redis, load_loginInfo, load_downloadInfo, load_spiderInfo
from database.mysqlDB import MySQlPool
from database.redisDB import RedisPool

from utils.logger import logger

logger.info("程序正在初始化...")
mysql_config = load_mysqlInfo()
logger.info("[mysql数据库配置]:加载成功...")
redis_config = load_redis()
logger.info("[redis数据库配置]:加载成功...")
login_config = load_loginInfo()
logger.info("[微博账户配置]:加载成功...")
download_config = load_downloadInfo()
logger.info("[下载配置]:加载成功...")
spider_config = load_spiderInfo()
logger.info("[爬虫配置]:加载成功...")

mysqlPool = MySQlPool(
    host=mysql_config.host,
    port=mysql_config.port,
    user=mysql_config.user,
    password=mysql_config.password,
    database=mysql_config.database
)
logger.info("[mysql数据库连接池]:初始化成功->>> {} -> {}".format(
    mysql_config.host, mysql_config.database
))

redisPoolObj = RedisPool(
    host=redis_config.host,
    port=redis_config.port,
    password=redis_config.password,
    db=redis_config.db
)
redisPool = redisPoolObj.redis
logger.info("[redis数据库连接池]:初始化成功->>> {} -> {}".format(
    redis_config.host, redis_config.db
))
