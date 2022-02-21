#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/12 16:07
@Project:WeiboSpider
@File:weiboTypeEntity.py
@Desc:
"""
class WeiboTypeEntity(object):
    """
    原创 or 转发
    original or forward
    """

    def __init__(self):
        self.__forward = None
        self.__original = None

    @property
    def original(self):
        return self.__original

    @original.setter
    def original(self, original):
        self.__original = original

    @property
    def forward(self):
        return self.__forward

    @forward.setter
    def forward(self, forward):
        self.__forward = forward