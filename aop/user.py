#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 15:21
@Project:WeiboSpider
@File:user.py
@Desc:
"""
import functools
from typing import List

from entity.user import User
from utils.logger import logger


class FilterUser:

    def __init__(self, filter_users, *args, **kwargs):
        self.filter_users = filter_users
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            users = func(*args, **kwargs)
            users = self.do_filter(users)
            log = "[博主过滤]：有[{}]位博主的数据将会被采集"
            logger.info(log.format(len(users)))
            return users

        return wrapper

    def do_filter(self, users: List[User]) -> List[User]:
        if not self.filter_users:
            return users
        users = [user for user in users if user.idstr in self.filter_users]
        return users
