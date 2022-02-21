#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/17 20:37
@Project:WeiboSpiderStation
@File:__init__.py.py
@Desc:
"""
from api.blogAPI import BlogAPI
from api.userAPI import UserAPI


class WeiBoAPI(UserAPI, BlogAPI):
    pass
