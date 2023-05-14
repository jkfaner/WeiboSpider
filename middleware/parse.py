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

from entity.userEntity import UserEntity
from entity.weiboTypeEntity import WeiboTypeEntity
from extractor.weiboJsonExtractor import ExtractorWeibo
from middleware.aop import FilterAOP, LoggerAOP


class Parse(object):
    """解析"""
    extractorWeibo = ExtractorWeibo()

    @FilterAOP.filter_user
    @LoggerAOP.extractor_user_log
    def extractor_user(self, response, *args, **kwargs) -> List[UserEntity]:
        """
        提取用户
        :param response: json str or dict
        :return:
        """
        return self.extractorWeibo.extractor_userInfo(resp=response)

    @FilterAOP.filter_blog_by_type
    @FilterAOP.filter_blog_by_date
    @LoggerAOP.extractor_blog_log
    def extractor_blog(self, response, *args, **kwargs) -> List[WeiboTypeEntity]:
        """
        提取博客
        :param response:
        :return:
        """
        return self.extractorWeibo.extractor_weibo(resp=response)
