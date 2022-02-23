#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 19:06
@Project:WeiboSpider
@File:userEnum.py
@Desc:微博用户信息PC端接口
"""
from utils.tool import join_url


class Info(object):
    """微博用户信息接口"""

    @staticmethod
    def getUserInfo(uid: str) -> str:
        """
        获取微博用户信息
        :param uid: 用户uid
        :return: URL
        """
        url = "https://weibo.com/ajax/profile/info"
        return join_url(url=url, params=dict(uid=uid))

    @staticmethod
    def getUserInfoDetail(uid: str) -> str:
        """
        获取微博用户信息详情
        :param uid: 用户uid
        :return: URL
        """
        url = "https://weibo.com/ajax/profile/detail"
        return join_url(url=url, params=dict(uid=uid))


class UserFollowAPI(Info):
    """微博用户关注接口"""

    @staticmethod
    def getUserFollow(uid: str, page: int) -> str:
        """
        获取用户关注
        :param uid: 用户uid
        :param page: 页码
        :return:
        """
        url = "https://weibo.com/ajax/friendships/friends"
        params = dict(page=page, uid=uid)
        return join_url(url=url, params=params)

    @staticmethod
    def getUserFollowByNewFollow(page: int, next_cursor: int = None) -> str:
        """
        通过最新关注获取关注用户
        参数说明：
            1.首页：next_cursor为None
            2.其他页：next_cursor默认+50 也可为None
        :param page: 页码
        :param next_cursor:
        :return:
        """
        url = "https://weibo.com/ajax/profile/followContent"
        return join_url(url=url, params=dict(page=page, next_cursor=next_cursor))

    @staticmethod
    def getUserFollowByNewPublic(next_cursor: int) -> str:
        """
        通过最新发布获取用户 (微博接口限制 只展示一周的数据)
        参数说明：
            page参数无效
            首页不带next_cursor参数
        :param next_cursor: 上一次请求next_cursor值
        :return:
        """
        url = "https://weibo.com/ajax/profile/followContent"
        return join_url(url=url, params=dict(next_cursor=next_cursor, sortType="timeDown"))


class UserAPI(UserFollowAPI):
    pass
