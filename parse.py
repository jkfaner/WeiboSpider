#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 17:08
@Project:WeiboSpiderStation
@File:parse.py
@Desc:解析类
"""
import logging
from typing import List

from aop.filter import FilterUser, FilterBlogType, FilterBlogDate, FilterDownloaded, CompleteDownload
from aop.log import LoggerAOP
from entity.blog import Blog
from entity.blogType import BlogType
from entity.user import User
from extractor.extractor_wb import ExtractorWeibo
from loader import FilterFactory
from request.fetch import Session


class WeiboParse(object):
    """解析"""
    extractorWeibo = ExtractorWeibo()

    @FilterUser(FilterFactory.get_filterUser())
    def extractor_user(self, response, *args, **kwargs) -> List[User]:
        """
        提取用户
        :param response: json str or dict
        :return:
        """
        return self.extractorWeibo.extractor_userInfo(resp=response)

    @FilterBlogDate()
    @FilterBlogType(FilterFactory.filter_type())
    def extractor_blog(self, response, *args, **kwargs) -> List[BlogType]:
        """
        提取博客
        :param response:
        :return:
        """
        return self.extractorWeibo.extractor_weibo(resp=response)


class DownloadParse(WeiboParse, Session):

    @FilterDownloaded()
    @LoggerAOP(message="[{}]即将下载的媒体数据有{}条", index=["kwargs['user'].screen_name", "len(kwargs['blogs'])"],level=logging.INFO, save=True)
    @CompleteDownload()
    def extractor_media(self, blogs: List[Blog], user: User):
        return self.extractorWeibo.extractor_media(blogs)


class Parse(DownloadParse):
    pass
