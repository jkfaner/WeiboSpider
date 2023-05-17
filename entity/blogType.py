#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/12 16:07
@Project:WeiboSpider
@File:blogType.py
@Desc:
"""


class BlogType(object):
    """
    原创 or 转发
    original or forward
    """

    def __init__(self):
        self.__forward = None
        self.__original = None
        self.__original_uid = None
        self.__forward_uid = None

    @property
    def original(self):
        return self.__original

    @original.setter
    def original(self, original):
        self.__original = original

    @property
    def original_uid(self):
        return self.__original_uid

    @original_uid.setter
    def original_uid(self, original_uid):
        self.__original_uid = original_uid

    @property
    def forward_uid(self):
        return self.__forward_uid

    @forward_uid.setter
    def forward_uid(self, forward_uid):
        self.__forward_uid = forward_uid

    @property
    def forward(self):
        return self.__forward

    @forward.setter
    def forward(self, forward):
        self.__forward = forward
