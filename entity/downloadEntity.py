#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/19 17:04
@Project:WeiboSpiderStation
@File:downloadEntity.py
@Desc:
"""


class DownloadEntity(object):

    def __init__(self):
        self.__blog = None
        self.__blog_id = None
        self.__url = None
        self.__filename = None
        self.__filepath = None
        self.__folder_name = None

    @property
    def blog(self):
        return self.__blog

    @blog.setter
    def blog(self, blog):
        self.__blog = blog

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def folder_name(self):
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, folder_name):
        self.__folder_name = folder_name

    @property
    def blog_id(self):
        return self.__blog_id

    @blog_id.setter
    def blog_id(self, blog_id):
        self.__blog_id = blog_id

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, filename):
        self.__filename = filename

    @property
    def filepath(self):
        return self.__filepath

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath
