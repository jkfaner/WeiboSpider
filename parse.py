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
from typing import List

from aop.complete import CompleteDownload
from aop.date import FilterBlogDate
from aop.downloaded import FilterDownloaded
from aop.type import FilterBlogType
from aop.user import FilterUser
from entity.blog import Blog
from entity.blogType import BlogType
from entity.media import Media
from entity.user import User
from extractor.extractor_wb import ExtractorWeibo
from loader import FilterFactory
from request.fetch import Session


class WeiboParse(object):
    """解析"""
    extractorWeibo = ExtractorWeibo()

    @FilterUser(FilterFactory.get_filterUser())  # 过滤博主
    def extractor_user(self, response, *args, **kwargs) -> List[User]:
        """
        提取用户
        :param response: json str or dict
        :return:
        """
        return self.extractorWeibo.extractor_userInfo(resp=response)

    @FilterBlogDate()  # 过滤日期
    @FilterBlogType(FilterFactory.filter_type())  # 过滤类型：原创、转发
    def extractor_blog(self, response, *args, **kwargs) -> List[BlogType]:
        """
        提取博客
        :param response:
        :return:
        """
        return self.extractorWeibo.extractor_weibo(resp=response)


class DownloadParse(WeiboParse, Session):

    @FilterDownloaded()
    @CompleteDownload()
    def extractor_media(self, blogs: List[Blog], user: User) -> List[Media]:
        return self.extractorWeibo.extractor_media(blogs)


class Parse(DownloadParse):
    pass
