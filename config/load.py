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
import datetime
import json
import os
from multiprocessing import cpu_count

from config.config import Config
from entity.downloadConfigEntity import DownloadConfigEntity
from entity.loginEntity import LoginEntity
from entity.mysqlEntity import MysqlEntity
from entity.redisConfigEntity import RedisConfigEntity
from entity.spiderConfigEntity import SpiderConfigEntity, SpiderCrawlItemConfig
from utils.exception import IntError, ParameterError
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
    config = GLOBAL_CONFIG.get("spider", "config")
    config_path = os.path.join(os.getcwd(), config)
    if not os.path.exists(config_path):
        raise Exception("""配置的json文件不存在，请这样设置json文件格式：{
  "onlyCrawl": {
    "switch": 1,
    "list": [
      {
        "date": "2021-01-01",
        "screen_name": "xxx",
        "uid": "12345678",
        "filter": "original"
      }
    ]
  },
  "excludeCrawl": {
    "switch": 1,
    "list": [
      {
        "date": "2021-01-01",
        "screen_name": "xxx",
        "uid": "12345678",
        "filter": "original"
      }
    ]
  }
}""")
    json_data = load_json(config_path)
    spiderConfigEntity.onlyCrawl_switch = json_data["onlyCrawl"]["switch"]
    spiderConfigEntity.excludeCrawl_switch = json_data["excludeCrawl"]["switch"]

    if spiderConfigEntity.onlyCrawl_switch:
        onlyCrawl_item = dict()
        for item in json_data["onlyCrawl"]["list"]:
            spiderCrawlItemEntity = SpiderCrawlItemConfig()
            date = item['date']
            screen_name = item.get("screen_name")
            uid = item.get("uid")
            assert is_valid_date(date), "日期格式错误"
            if (not screen_name) and (not uid):
                raise ParameterError("配置文件参数错误：{}".format(item))
            spiderCrawlItemEntity.date = date
            spiderCrawlItemEntity.screen_name = screen_name
            spiderCrawlItemEntity.uid = uid
            spiderCrawlItemEntity.filter = item["filter"]
            onlyCrawl_item[uid] = spiderCrawlItemEntity
        spiderConfigEntity.onlyCrawl_item = [v for v in onlyCrawl_item.values()]

    if spiderConfigEntity.excludeCrawl_switch:
        excludeCrawl_item = dict()
        for item in json_data["excludeCrawl"]["list"]:
            spiderCrawlItemEntity = SpiderCrawlItemConfig()
            date = item['date']
            screen_name = item.get("screen_name")
            uid = item.get("uid")
            assert is_valid_date(date), "日期格式错误"
            if (not screen_name) and (not uid):
                raise ParameterError("配置文件参数错误：{}".format(item))
            spiderCrawlItemEntity.date = date
            spiderCrawlItemEntity.screen_name = screen_name
            spiderCrawlItemEntity.uid = uid
            spiderCrawlItemEntity.filter = item["filter"]
            excludeCrawl_item[uid] = spiderCrawlItemEntity
        spiderConfigEntity.excludeCrawl_item = [v for v in excludeCrawl_item.values()]

    return spiderConfigEntity


def create_new_spiderInfo():
    spiderConfigEntity = load_spiderInfo()
    new_item = {"onlyCrawl": dict(switch=0, list=list()), "excludeCrawl": dict(switch=0, list=list())}

    if spiderConfigEntity.excludeCrawl_switch:
        new_item['excludeCrawl']["switch"] = 1
        for item in spiderConfigEntity.excludeCrawl_item:
            new_item["excludeCrawl"]["list"].append({
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "screen_name": item.screen_name,
                "uid": item.uid,
                "filter": item.filter
            })
    else:
        new_item['excludeCrawl']["switch"] = 0

    if spiderConfigEntity.onlyCrawl_switch:
        new_item['onlyCrawl']["switch"] = 1
        for item in spiderConfigEntity.onlyCrawl_item:
            new_item["onlyCrawl"]["list"].append({
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "screen_name": item.screen_name,
                "uid": item.uid,
                "filter": item.filter
            })
    else:
        new_item['onlyCrawl']["switch"] = 0

    with open(os.path.join(os.getcwd(), "new-config.json"), "w") as f:
        json.dump(new_item, f, ensure_ascii=False)
