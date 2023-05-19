#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 19:38
@Project:WeiboSpider
@File:progress.py
@Desc:
"""
import json

from entity.base import BaseEntity


class Progress(BaseEntity):
    def __init__(self):
        self._uid = None
        self._blog_id = None
        self._blog_create_time = None
        self._start_time = None
        self._parse_time = None
        self._download_time = None
        self._downloaded_time = None
        self._media_num = None
        self._download_num = None
        self._download_error_num = None

    @property
    def blog_create_time(self):
        return self._blog_create_time

    @blog_create_time.setter
    def blog_create_time(self, value):
        self._blog_create_time = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def parse_time(self):
        return self._parse_time

    @parse_time.setter
    def parse_time(self, value):
        self._parse_time = value

    @property
    def download_time(self):
        return self._download_time

    @download_time.setter
    def download_time(self, value):
        self._download_time = value

    @property
    def downloaded_time(self):
        return self._downloaded_time

    @downloaded_time.setter
    def downloaded_time(self, value):
        self._downloaded_time = value

    @property
    def media_num(self):
        return self._media_num

    @media_num.setter
    def media_num(self, value):
        self._media_num = value

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = value

    @property
    def blog_id(self):
        return self._blog_id

    @blog_id.setter
    def blog_id(self, value):
        self._blog_id = value

    @property
    def download_num(self):
        return self._download_num

    @download_num.setter
    def download_num(self, value):
        self._download_num = value

    @property
    def download_error_num(self):
        return self._download_error_num

    @download_error_num.setter
    def download_error_num(self, value):
        self._download_error_num = value

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
