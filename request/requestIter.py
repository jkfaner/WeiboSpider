#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 00:02
@Project:WeiboSpiderStation
@File:requestIter.py
@Desc:
"""
from extractor.jsonExtractorAPI import ExtractorApi
from request.request import Request


class RequestIter(Request):
    extractorApi = ExtractorApi()

    def getUserFollowIter(self, uid: str, page=1):
        """
        获取用户关注
        :param uid: 用户uid
        :param page: 页码
        :return:
        """
        response_json = self.getUserFollow(uid=uid, page=page)
        if self.extractorApi.find_first_data(resp=response_json, target="users"):
            yield response_json
            yield from self.getUserFollowIter(uid=uid, page=page + 1)

    def getUserFollowByNewFollowIter(self, page=1):
        """
        通过最新关注获取关注用户
        :param page: 页码
        :return:
        """
        response_json = self.getUserFollowByNewFollow(page=page)
        if self.extractorApi.find_first_data(resp=response_json, target="users"):
            yield response_json
            yield from self.getUserFollowByNewFollowIter(page=page + 1)

    def getUserFollowByNewPublicIter(self, next_cursor=None):
        """
        通过最新发布获取用户 (微博接口限制 只展示一周的数据)
        参数说明：
            page参数无效
            首页不带next_cursor参数
        :param page: 页码
        :param next_cursor: 上一次请求next_cursor值
        :return:
        """
        response_json = self.getUserFollowByNewPublic(next_cursor=next_cursor)
        if self.extractorApi.find_first_data(resp=response_json, target="users"):
            yield response_json
            next_cursor = self.extractorApi.find_first_data(resp=response_json, target="next_cursor")
            if next_cursor:
                yield from self.getUserFollowByNewPublicIter(next_cursor=next_cursor)

    def getUserBlogIter(self, uid: str, page=1, since_id=None):
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
        response_json = self.getUserBlog(uid=uid, page=page, since_id=since_id)
        if self.extractorApi.find_first_data(resp=response_json, target="list"):
            yield response_json
            since_id = self.extractorApi.find_first_data(resp=response_json, target="since_id")
            if since_id:
                yield from self.getUserBlogIter(uid=uid, page=page + 1, since_id=since_id)
