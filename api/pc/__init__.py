#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/23 21:02
@Project:WeiboSpider
@File:__init__.py.py
@Desc:微博PC端接口
"""
from api.pc.blogAPI import BlogAPI
from api.pc.userAPI import UserAPI


class WeiBoPC_API(UserAPI, BlogAPI):
    pass