#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/17 23:56
@Project:WeiboSpiderStation
@File:request.py
@Desc:Request请求
"""
from api import WeiBoAPI
from middleware.sessionMiddleware import SessionMiddleware


class Request(SessionMiddleware, WeiBoAPI):

    def getUserFollow(self, uid: str, page: int):
        """
        获取用户关注
        :param uid: 用户uid
        :param page: 页码
        :return:
        """
        url = super(Request, self).getUserFollow(uid=uid, page=page)
        return self.fetch_json(url=url)

    def getUserFollowByNewFollow(self, page: int, next_cursor: int = None) -> str:
        """
        通过最新关注获取关注用户
        参数说明：
            1.首页：next_cursor为None
            2.其他页：next_cursor默认+50 也可为None
        :param page: 页码
        :param next_cursor:
        :return:
        """
        url = super(Request, self).getUserFollowByNewFollow(page=page, next_cursor=next_cursor)
        return self.fetch_json(url=url)

    def getUserFollowByNewPublic(self, next_cursor: int) -> str:
        """
        通过最新发布获取用户 (微博接口限制 只展示一周的数据)
        参数说明：
            page参数无效
            首页不带next_cursor参数
        :param next_cursor: 上一次请求next_cursor值
        :return:
        """
        url = super(Request, self).getUserFollowByNewPublic(next_cursor=next_cursor)
        return self.fetch_json(url=url)

    def getUserBlog(self, uid: str, page: int, since_id: str = None) -> str:
        """
        获取用户博客
        参数说明：
            1.首页没有since_id参数
            2.其他页面必须携带since_id
        :param uid: 用户uid
        :param page: 页码
        :param since_id: 上一页since_id值
        :return:
        """
        url = super(Request, self).getUserBlog(uid=uid, page=page, since_id=since_id)
        return self.fetch_json(url=url)
