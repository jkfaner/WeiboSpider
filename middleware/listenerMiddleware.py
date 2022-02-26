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

    def listener(self):
        """
        监听是否有博主更新数据
            1.监听是否有新关注的用户
                1.1 有新关注->是否需要爬取->爬取
            2.监听关注用户有无更新内容
                2.1 有更新->是否需要爬取->爬取
        1.通过访问关注者最新关注接口检测是否有更新的用户
        2.通过访问关注者最新发布接口检测是否有更新的用户
        注：优先爬取先关注的用户数据
        :return:
        """
        # TODO 开发中
        for item in self.requestIter.getUserFollowByNewPublicIter():
            users = self.parse_user(item)
            for blogs,user in self.get_blog(users=users):
                self.start_download(blogs=blogs, user=user)
