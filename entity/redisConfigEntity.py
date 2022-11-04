#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 16:17
@Project:WeiboSpiderStation
@File:redisConfigEntity.py
@Desc:
"""
class RedisConfigEntity(object):
    def __init__(self):
        self.__host = None
        self.__port = None
        self.__password = None
        self.__db = None

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db):
        self.__db = db
