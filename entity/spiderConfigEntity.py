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

class SpiderConfigEntity(object):
    def __init__(self):
        self.__mode = None
        self.__follow_mode = None
        self.__onlyCrawl_switch = None
        self.__excludeCrawl_switch = None
        self.__onlyCrawl_screen_name = None
        self.__onlyCrawl_uid = None
        self.__excludeCrawl_screen_name = None
        self.__excludeCrawl_uid = None
        self.__date = None
        self.__spiderFilter = None

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
    def onlyCrawl_screen_name(self):
        return self.__onlyCrawl_screen_name

    @onlyCrawl_screen_name.setter
    def onlyCrawl_screen_name(self, onlyCrawl_screen_name):
        self.__onlyCrawl_screen_name = onlyCrawl_screen_name

    @property
    def onlyCrawl_uid(self):
        return self.__onlyCrawl_uid

    @onlyCrawl_uid.setter
    def onlyCrawl_uid(self, onlyCrawl_uid):
        self.__onlyCrawl_uid = onlyCrawl_uid

    @property
    def excludeCrawl_screen_name(self):
        return self.__excludeCrawl_screen_name

    @excludeCrawl_screen_name.setter
    def excludeCrawl_screen_name(self, excludeCrawl_screen_name):
        self.__excludeCrawl_screen_name = excludeCrawl_screen_name

    @property
    def excludeCrawl_uid(self):
        return self.__excludeCrawl_uid

    @excludeCrawl_uid.setter
    def excludeCrawl_uid(self, excludeCrawl_uid):
        self.__excludeCrawl_uid = excludeCrawl_uid

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def spiderFilter(self):
        return self.__spiderFilter

    @spiderFilter.setter
    def spiderFilter(self, spiderFilter):
        self.__spiderFilter= spiderFilter
