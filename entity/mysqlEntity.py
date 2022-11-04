#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 15:58
@Project:WeiboSpiderStation
@File:mysql_config.py
@Desc:
"""


class MysqlEntity(object):

    def __init__(self):
        self.__host = None
        self.__port = None
        self.__user = None
        self.__password = None
        self.__database = None

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database):
        self.__database = database
