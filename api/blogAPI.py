#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 16:39
@Project:WeiboSpiderStation
@File:blogAPI.py
@Desc:微博博客接口
"""
from utils.tool import join_url


class BlogAPI(object):
    """微博博客接口"""

    def getUserBlog(self, uid: str, page: int, since_id: str = None) -> str:
        """
        获取用户博客
        参数说明：
            1.首页没有since_id参数
            2.其他页面必须携带since_id
            3.feature始终为0（已经写死）
        :param uid: 用户uid
        :param page: 页码
        :param since_id: 上一页since_id值
        :return:
        """
        url = "https://weibo.com/ajax/statuses/mymblog"
        return join_url(url=url, params=dict(uid=uid, page=page, since_id=since_id, feature=0))
