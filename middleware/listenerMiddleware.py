#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/23 17:37
@Project:WeiboSpider
@File:listenerMiddleware.py
@Desc:监听中间件
"""
from typing import List
from init import mysqlPool

from entity.userEntity import UserEntity


class ListenerMiddleware(object):

    @staticmethod
    def select_weibo_user(uid: str):
        """
        查询数据库微博用户
        :param uid:
        :return:
        """
        sql = "SELECT weibo_id,screen_name FROM weibo_user WHERE weibo_id=%s"
        result = mysqlPool.getOne(sql=sql, param=[uid])
        return result

    def listener_new_follow(self, users: List[UserEntity]) -> List[UserEntity]:
        """
        监听有无新关注的用户
        :param users:
        :return: 新关注的用户
        """
        return [user for user in users if not self.select_weibo_user(uid=user.idstr)]

    def listener_new_publish(self):
        # TODO 开发中
        pass
