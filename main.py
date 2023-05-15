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
import time
from typing import List

from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from entity.weiboTypeEntity import WeiboTypeEntity
from middleware.aop import LoggerAOP
from parse import WeiboParse
from request.download import Download
from request.fetch import Session
from request.login import Login
from request.requestIter import RequestIter
from utils.exception import DateError


class InitMain(WeiboParse, Session):
    requestIter = RequestIter()
    download = Download()

    def start_download(self, blogs: List[WeiboEntity], user: UserEntity):
        """
        开始下载：
            数据筛选&下载
        :param blogs:
        :param user:
        :return:
        """
        download_datas = self.download.distribute_data(blogs=blogs, user=user)
        self.download.startDownload(download_datas)


class BaseSpider(InitMain):

    def spider_iter(self, *args, **kwargs):
        yield []

    def run(self, *args, **kwargs):
        pass


class SpiderDefaultFollow(BaseSpider):
    """爬取关注->默认爬虫规则"""

    @LoggerAOP(message="爬取关注->默认爬虫规则")
    def spider_iter(self, *args, **kwargs):
        # 获取uid
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


class SpiderNewFollow(BaseSpider):
    """爬取关注->最新关注顺序"""

    @LoggerAOP(message="爬取关注->最新关注顺序")
    def spider_iter(self, *args, **kwargs):
        for item in self.requestIter.getUserFollowByNewFollowIter():
            yield self.extractor_user(item)


class SpiderNewPublishFollow(BaseSpider):
    """爬取关注->最新有发布的用户顺序"""

    @LoggerAOP(message="爬取关注->最新有发布的用户顺序")
    def spider_iter(self, *args, **kwargs):
        for item in self.requestIter.getUserFollowByNewPublicIter():
            yield self.extractor_user(item)


class SpiderFollow(BaseSpider):
    """爬取关注"""

    def __init__(self, obj: BaseSpider):
        super(SpiderFollow, self).__init__()
        self.obj = obj

    @LoggerAOP(message="获取博客信息")
    def get_blog_iter(self, users: List[UserEntity]) -> List[WeiboTypeEntity]:
        """
        获取博客
        :param users:
        :return:
        """
        for user in users:
            for blog in self.requestIter.getUserBlogIter(uid=user.idstr):
                blogs = None
                try:
                    blogs = self.extractor_blog(response=blog, user=user)
                except DateError as e:
                    blogs = e.args[1]
                    break
                finally:
                    if blogs:
                        yield blogs, user
                    time.sleep(2)

    @LoggerAOP(message="执行入口->爬取关注")
    def run(self, *args, **kwargs):
        for users in self.obj.spider_iter():
            for blogs, user in self.get_blog_iter(users=users):
                self.start_download(blogs=blogs, user=user)


class SpiderRefresh(BaseSpider):
    """刷微博"""

    @LoggerAOP(message="执行入口->刷微博")
    def run(self, *args, **kwargs):
        pass


class Spider(object):

    def __init__(self, obj: BaseSpider):
        self.obj = obj

    def run(self, *args, **kwargs):
        self.obj.run(*args, **kwargs)
