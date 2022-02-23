#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/19 19:37
@Project:WeiboSpider
@File:load.py
@Desc:
"""
import os
from multiprocessing import cpu_count

from config.config import Config
from entity.downloadConfigEntity import DownloadConfigEntity
from entity.loginEntity import LoginEntity
from entity.mysqlEntity import MysqlEntity
from entity.redisConfigEntity import RedisConfigEntity
from entity.spiderConfigEntity import SpiderConfigEntity
from utils.exception import IntError
from utils.logger import logger
from utils.tool import is_valid_date, load_json
GLOBAL_CONFIG = Config()
logger.info("配置文件加载成功...")


def load_loginInfo() -> LoginEntity:
    """
    加载登录配置信息
    :return:
    """
    login = LoginEntity()
    login.username = GLOBAL_CONFIG.get("login", "username")
    login.password = GLOBAL_CONFIG.get("login", "password")
    login.mode = GLOBAL_CONFIG.get("login", "mode")
    assert login.mode in ['pc', 'mobile', 'scanqr'], "你选择的登录方式有误，只能将mode设置为pc、mobile、scanqr，其中任意一个"
    return login


def load_mysqlInfo() -> MysqlEntity:
    """
    加载mysql配置信息
    :return:
    """
    mysql = MysqlEntity()
    mysql.host = GLOBAL_CONFIG.get("mysql", "host")
    mysql.port = GLOBAL_CONFIG.getInt("mysql", "port")
    mysql.user = GLOBAL_CONFIG.get("mysql", "user")
    mysql.password = GLOBAL_CONFIG.get("mysql", "password")
    mysql.database = GLOBAL_CONFIG.get("mysql", "database")
    return mysql


def load_redis() -> RedisConfigEntity:
    """
    加载redis配置信息
    :return:
    """
    redis = RedisConfigEntity()
    redis.host = GLOBAL_CONFIG.get("redis", "host")
    redis.port = GLOBAL_CONFIG.getInt("redis", "port")
    redis.password = GLOBAL_CONFIG.get("redis", "password")
    redis.db = GLOBAL_CONFIG.getInt("redis", "db")
    return redis


def load_downloadInfo() -> DownloadConfigEntity:
    """
    加载下载配置信息
    :return:
    """
    # 读取download信息
    downloadConfigEntity = DownloadConfigEntity()
    downloadConfigEntity.root = GLOBAL_CONFIG.get("download", "root")
    try:
        downloadConfigEntity.thread = GLOBAL_CONFIG.getBoolean("download", "thread")
    except ValueError:
        raise IntError("是否开启多线程下载，True or False")
    try:
        workers = GLOBAL_CONFIG.getInt("download", "workers")
    except ValueError:
        raise IntError("线程数仅允许为整数")
    if workers > cpu_count():
        logger.warning("下载线程数超过CPU核心数，已修正为CPU核心数：{}".format(cpu_count()))
        workers = cpu_count()
    elif workers <= 0:
        logger.warning("下载线程数超过CPU核心数，已修正为CPU核心数：{}".format(cpu_count()))
        workers = cpu_count()
    downloadConfigEntity.workers = workers
    return downloadConfigEntity


def load_spiderInfo() -> SpiderConfigEntity:
    """
    加载爬虫配置信息
    :return:
    """
    spiderConfigEntity = SpiderConfigEntity()
    spiderConfigEntity.mode = GLOBAL_CONFIG.get("spider", "mode")
    spiderConfigEntity.follow_mode = GLOBAL_CONFIG.get("spider", "follow_mode")

    spiderConfigEntity.onlyCrawl_switch = GLOBAL_CONFIG.getBoolean("spider", "onlyCrawl_switch")
    spiderConfigEntity.excludeCrawl_switch = GLOBAL_CONFIG.getBoolean("spider", "excludeCrawl_switch")

    config = GLOBAL_CONFIG.get("spider", "config")
    config_path = os.path.join(os.getcwd(), config)
    if not os.path.exists(config_path):
        raise Exception("配置的json文件不存在")

    data = load_json(config_path)
    oc_name = data["onlyCrawl_screen_name"]
    oc_uid = data["onlyCrawl_uid"]
    spiderConfigEntity.onlyCrawl_screen_name = sorted(set(oc_name), key=oc_name.index) if set(oc_name) else list()
    spiderConfigEntity.onlyCrawl_uid = list(set(oc_uid)) if set(oc_uid) else list()

    ec_name = data["excludeCrawl_screen_name"]
    ec_uid = data["excludeCrawl_uid"]
    spiderConfigEntity.excludeCrawl_screen_name = sorted(set(ec_name), key=ec_name.index) if set(ec_name) else list()
    spiderConfigEntity.excludeCrawl_uid = list(set(ec_uid)) if set(ec_uid) else list()

    date = GLOBAL_CONFIG.get("spider", "date")
    s_filter = GLOBAL_CONFIG.get("spider", "filter")
    assert is_valid_date(date), "日期格式错误"
    spiderConfigEntity.date = date
    spiderConfigEntity.spiderFilter = s_filter
    return spiderConfigEntity
