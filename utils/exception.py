#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 14:33
@Project:WeiboSpiderStation
@File:exception.py
@Desc:
"""


class IntError(Exception):
    pass


class ParameterError(Exception):
    # 参数错误
    pass


class DateError(Exception):
    """日期错误"""
    pass


class NOTContentLengthError(Exception):
    """资源链接失效"""
    pass


class FinishedError(Exception):
    """已完成"""
    pass


class NotFound(Exception):
    """404错误"""
    pass
