#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/19 13:17
@Project:WeiboSpiderStation
@File:download_config.py
@Desc:
"""
class DownloadConfigEntity(object):

    def __init__(self):
        self.__root = None
        self.__thread = None
        self.__workers = None

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, root):
        self.__root = root

    @property
    def thread(self):
        return self.__thread

    @thread.setter
    def thread(self, thread):
        self.__thread = thread

    @property
    def workers(self):
        return self.__workers

    @workers.setter
    def workers(self, workers):
        self.__workers = workers
