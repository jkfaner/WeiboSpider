#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/19 17:04
@Project:WeiboSpiderStation
@File:media.py
@Desc:
"""
import json

from entity.base import BaseEntity


class Media(BaseEntity):

    def __init__(self):
        self._blog = None
        self._blog_id = None
        self._url = None
        self._filename = None
        self._filepath = None
        self._folder_name = None

    @property
    def blog(self):
        return self._blog

    @blog.setter
    def blog(self, blog):
        self._blog = blog

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def folder_name(self):
        return self._folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self._folder_name = folder_name

    @property
    def blog_id(self):
        return self._blog_id

    @blog_id.setter
    def blog_id(self, blog_id):
        self._blog_id = blog_id

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        self._filepath = filepath

    def to_dict(self):
        obj_dict = self.__dict__
        cleaned_dict = {}
        for key, value in obj_dict.items():
            if key.startswith('_'):
                key = key[1:]
            cleaned_dict[key] = value
        return cleaned_dict

    def to_json(self):
        media_dict = self.to_dict()
        media_dict["blog"] = media_dict["blog"].to_dict()
        return json.dumps(media_dict, ensure_ascii=False)
