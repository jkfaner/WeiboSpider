#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 16:39
@Project:WeiboSpiderStation
@File:blogAPI.py
@Desc:微博博客PC端接口
# TODO 开发中
"""
from utils.tool import join_url


class BlogAPI(object):
    """微博博客接口"""

    def getUserBlog(self, uid: str,containerid: str = None) -> str:
        """
        获取用户博客
        参数说明：
            1.首页没有since_id参数
            2.其他页面必须携带since_id
            3.jumpfrom始终为weibocom（已经写死）
            3.type始终为uid（已经写死）
        :param uid: 用户uid
        :param containerid: 上一页since_id值
        :return:
        """
        url = "https://m.weibo.cn/api/container/getIndex"
        return join_url(url=url, params=dict(jumpfrom="weibocom",type="uid",value=uid,containerid=containerid))
