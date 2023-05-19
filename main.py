#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 14:30
@Project:WeiboSpiderStation
@File:testRequestIter.py
@Desc:
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import List

from aop.log import LoggerAOP
from entity.blogType import BlogType
from entity.user import User
from parse import Parse
from request.download import Download
from request.login import Login
from request.request import RequestIter


class BaseStrategy(Parse, ABC):
    requestIter = RequestIter()
    download = Download()

    @abstractmethod
    def execute(self):
        raise NotImplementedError("子类必须实现execute()方法")


class SpiderDefaultFollow(BaseStrategy):
    """爬取关注->默认爬虫规则"""

    @LoggerAOP(message="爬取关注->默认爬虫规则", level=logging.INFO, save=True)
    def execute(self):
        print("执行策略A的操作")
        login = Login()
        cookies_item = login.select_cookies()
        if cookies_item:
            uid = cookies_item['uid']
        else:
            login.login_online(session=self.session, insert=True)
            cookies_item = login.select_cookies()
            uid = cookies_item['uid']

        for item in self.requestIter.getUserFollowIter(uid=uid):
            yield self.extractor_user(item)


class SpiderNewFollow(BaseStrategy):
    """爬取关注->最新关注顺序"""

    @LoggerAOP(message="爬取关注->最新关注顺序", level=logging.INFO, save=True)
    def execute(self):
        print("执行策略B的操作")
        for item in self.requestIter.getUserFollowByNewFollowIter():
            yield self.extractor_user(item)


class SpiderNewPublishFollow(BaseStrategy):
    """爬取关注->最新有发布的用户顺序"""

    def execute(self):
        print("执行策略C的操作")
        for item in self.requestIter.getUserFollowByNewPublicIter():
            yield self.extractor_user(item)


class SpiderFollow(BaseStrategy):

    def __init__(self, inner_strategy):
        super(SpiderFollow, self).__init__()
        self.inner_strategy = inner_strategy

    @LoggerAOP(message="获取博客信息", level=logging.INFO, save=True)
    def get_blog_iter(self, users: List[User]) -> List[BlogType]:
        """
        获取博客
        :param users:
        :return:
        """
        for user in users:
            for blog in self.requestIter.getUserBlogIter(uid=user.idstr):
                if isinstance(blog, list):
                    yield blog, user

                blogs = self.extractor_blog(response=blog, user=user)
                if isinstance(blogs, bool):
                    # 全量采集
                    break
                if blogs:
                    yield blogs, user
                time.sleep(1)

    @LoggerAOP(message="执行入口->爬取关注", level=logging.INFO, save=True)
    def execute(self):
        for users in self.inner_strategy.execute():
            for blogs, user in self.get_blog_iter(users=users):
                medias = self.extractor_media(blogs=blogs, user=user)
                if not medias:
                    # 非全量
                    continue
                self.download.startDownload(medias)


class SpiderRefresh(BaseStrategy):

    def __init__(self, inner_strategy):
        super(SpiderRefresh, self).__init__()
        self.inner_strategy = inner_strategy

    @LoggerAOP(message="执行入口->刷微博", level=logging.INFO, save=True)
    def execute(self):
        print("执行嵌套策略B的操作")
        self.inner_strategy.execute()
