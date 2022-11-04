#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 19:50
@Project:WeiboSpiderStation
@File:spider_config.py
@Desc:
"""
from typing import List


class SpiderCrawlItemConfig(object):

    def __init__(self):
        self.__date = None
        self.__screen_name = None
        self.__uid = None
        self.__filter = None

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def screen_name(self):
        return self.__screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        self.__screen_name = screen_name

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid):
        self.__uid = uid

    @property
    def filter(self):
        return self.__filter

    @filter.setter
    def filter(self, filter):
        self.__filter = filter


class SpiderConfigEntity(object):

    def __init__(self):
        self.__mode = None
        self.__follow_mode = None
        self.__onlyCrawl_switch = None
        self.__excludeCrawl_switch = None
        self.__onlyCrawl_item = None
        self.__excludeCrawl_item = None

    @property
    def follow_mode(self):
        return self.__follow_mode

    @follow_mode.setter
    def follow_mode(self, follow_mode):
        self.__follow_mode = follow_mode

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode

    @property
    def onlyCrawl_switch(self):
        return self.__onlyCrawl_switch

    @onlyCrawl_switch.setter
    def onlyCrawl_switch(self, onlyCrawl_switch):
        self.__onlyCrawl_switch = onlyCrawl_switch

    @property
    def excludeCrawl_switch(self):
        return self.__excludeCrawl_switch

    @excludeCrawl_switch.setter
    def excludeCrawl_switch(self, excludeCrawl_switch):
        self.__excludeCrawl_switch = excludeCrawl_switch

    @property
    def onlyCrawl_item(self):
        return self.__onlyCrawl_item

    @onlyCrawl_item.setter
    def onlyCrawl_item(self, onlyCrawl_item:List[SpiderCrawlItemConfig]):
        self.__onlyCrawl_item = onlyCrawl_item

    @property
    def excludeCrawl_item(self):
        return self.__excludeCrawl_item

    @excludeCrawl_item.setter
    def excludeCrawl_item(self, excludeCrawl_item: List[SpiderCrawlItemConfig]):
        self.__excludeCrawl_item = excludeCrawl_item
