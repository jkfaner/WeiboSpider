#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 15:24
@Project:WeiboSpider
@File:complete.py
@Desc:
"""
import functools

from cache import Cache
from utils.logger import logger


class CompleteDownload(Cache):

    def __init__(self, *args, **kwargs):
        super(CompleteDownload, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            blogs = kwargs['blogs']
            user = kwargs['user']
            if isinstance(blogs, list) and blogs[0] ==user.idstr:
                # TODO 存在bug
                # 当前博主已经完成全量爬取
                self.record_complete(user.idstr)
                logger.info("[全部完成]：【{}[{}]】的媒体数据已经全部采集完毕".format(user.screen_name, user.idstr))
                return []
            # 执行装饰器操作
            return func(*args, **kwargs)

        return wrapper
