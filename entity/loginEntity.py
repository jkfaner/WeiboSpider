#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 16:04
@Project:WeiboSpiderStation
@File:login_config.py
@Desc:
"""


class LoginEntity(object):

    def __init__(self):
        self.__username = None
        self.__password = None
        self.__mode = None
        self.__uid = None

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, uid):
        self.__mode = uid
