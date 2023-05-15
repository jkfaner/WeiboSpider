#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/17 23:56
@Project:WeiboSpiderStation
@File:request.py
@Desc:Request请求
"""
from aop import LoggerAOP
from extractor.extractor import ExtractorApi
from loader import ProjectLoader
from request.fetch import Session
from request.login import Login
from utils.logger import logger
from utils.tool import join_url


class SessionMiddleware(Session):
    loginObj = Login()
    login_times = 1

    @LoggerAOP(message="Request URL：{}", index=1)
    def fetch(self, url, headers=None, method='get', session=None, **kwargs):
        # 首次必须登录
        if self.login_times == 1:
            logger.info("开始第{}登录...".format(self.login_times))
            if self.loginObj.login_localhost(session=self.session):
                if not self.loginObj.is_login(fetch=super(SessionMiddleware, self).fetch):
                    self.loginObj.login_online(session=self.session, insert=False)
            else:
                self.loginObj.login_online(session=self.session, insert=True)
            self.login_times += 1
        response = super(SessionMiddleware, self).fetch(url, headers, method, session, **kwargs)
        if response.url != url:
            self.loginObj.login_online(session=self.session, insert=False)
            return self.fetch(url, headers, method, session, **kwargs)
        return response

    def fetch_json(self, url, headers=None, method='get', session=None, **kwargs):
        return self.fetch(url, headers, method, session, **kwargs).json()


class Request(SessionMiddleware):

    def __init__(self):
        self.spiderAPI = ProjectLoader.getSystemConfig().get("api")
        super(Request, self).__init__()

    def getUserFollow(self, uid: str, page: int):
        """
        获取用户关注
        :param uid: 用户uid
        :param page: 页码
        :return:
        """
        url = join_url(url=self.spiderAPI.get("userFriends"), params=dict(page=page, uid=uid))
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
        url = join_url(url=self.spiderAPI.get("userFollow"), params=dict(page=page, next_cursor=next_cursor))
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
        url = join_url(url=self.spiderAPI.get("userFollow"), params=dict(next_cursor=next_cursor, sortType="timeDown"))
        return self.fetch_json(url=url)

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
        url = join_url(url=self.spiderAPI.get("userBlog"),
                       params=dict(uid=uid, page=page, since_id=since_id, feature=0))
        return self.fetch_json(url=url)


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
        result_list = self.extractorApi.find_first_data(resp=response_json, target="list")
        if result_list:
            yield response_json
            since_id = self.extractorApi.find_first_data(resp=response_json, target="since_id")
            if since_id:
                yield from self.getUserBlogIter(uid=uid, page=page + 1, since_id=since_id)
        else:
            # 用于全量爬取标志
            yield [uid]
