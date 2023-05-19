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
import json

from entity.base import BaseEntity


class BlogType(BaseEntity):

    def __init__(self):
        self._forward = None
        self._original = None
        self._original_uid = None
        self._forward_uid = None

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, original):
        self._original = original

    @property
    def original_uid(self):
        return self._original_uid

    @original_uid.setter
    def original_uid(self, original_uid):
        self._original_uid = original_uid

    @property
    def forward_uid(self):
        return self._forward_uid

    @forward_uid.setter
    def forward_uid(self, forward_uid):
        self._forward_uid = forward_uid

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, forward):
        self._forward = forward

    def to_dict(self):
        obj_dict = self.__dict__
        cleaned_dict = {}
        for key, value in obj_dict.items():
            if key.startswith('_'):
                key = key[1:]
            cleaned_dict[key] = value
        return cleaned_dict

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
