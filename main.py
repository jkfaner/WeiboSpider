#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 14:30
@Project:WeiboSpiderStation
@File:testRequestIter.py
@Desc:
"""
import time
from typing import List

from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from parse import WeiboParse
from request.download import Download
from request.fetch import Session
from request.login import Login
from request.requestIter import RequestIter
from utils.exception import DateError


class InitMain(WeiboParse, Session):
    requestIter = RequestIter()
    download = Download()

    def start_download(self, blogs: List[WeiboEntity], user: UserEntity):
        """
        开始下载：
            数据筛选&下载
        :param blogs:
        :param user:
        :return:
        """
        download_datas = self.download.distribute_data(blogs=blogs, user=user)
        self.download.startDownload(download_datas)


class BaseFollowObject(InitMain):

    def spider(self):
        yield []


class SpiderDefaultFollow(BaseFollowObject):
    """默认爬虫规则"""

    def spider(self):
        print("默认爬虫规则")
        # 获取uid
        login = Login()
        cookies_item = login.select_cookies()
        if cookies_item:
            uid = cookies_item['uid']
        else:
            login.login_online(session=self.session, insert=True)
            cookies_item = login.select_cookies()
            uid = cookies_item['uid']
        for item in self.requestIter.getUserFollowIter(uid=uid):
            yield self.extractor_user(item)


class SpiderNewFollow(BaseFollowObject):
    """爬取关注->最新关注顺序"""

    def spider(self):
        print("爬取关注->最新关注顺序")
        for item in self.requestIter.getUserFollowByNewFollowIter():
            yield self.extractor_user(item)


class SpiderNewPublishFollow(BaseFollowObject):
    """爬取关注->最新有发布的用户顺序"""

    def spider(self):
        print("爬取关注->最新有发布的用户顺序")
        for item in self.requestIter.getUserFollowByNewPublicIter():
            yield self.extractor_user(item)


#############
class BaseSpiderObject(BaseFollowObject):

    def run(self, action):
        pass


class SpiderFollow(BaseSpiderObject):
    """爬取关注"""

    def __init__(self, follow: BaseFollowObject):
        super(SpiderFollow, self).__init__()
        self.follow = follow

    def get_blog(self, users: List[UserEntity]):
        """
        获取博客
        :param users:
        :return:
        """
        for user in users:
            for blog in self.requestIter.getUserBlogIter(uid=user.idstr):
                blogs = None
                try:
                    blogs = self.extractor_blog(response=blog, user=user)
                except DateError as e:
                    blogs = e.args[1]
                    break
                finally:
                    if blogs:
                        yield blogs, user
                    time.sleep(2)

    def run(self, action):
        for users in self.follow.spider():
            for blogs, user in self.get_blog(users=users):
                self.start_download(blogs=blogs, user=user)


class SpiderRefresh(BaseSpiderObject):
    """刷微博"""

    def run(self, action):
        print("SpiderRefresh->{}".format(action))


class Spider(object):

    def __init__(self, action: BaseSpiderObject):
        self.action = action

    def do(self, action):
        self.action.run(action)


if __name__ == '__main__':
    strategy = {}
    strategy[1] = Spider(SpiderFollow(SpiderDefaultFollow()))
    strategy[2] = Spider(SpiderFollow(SpiderNewFollow()))
    strategy[3] = Spider(SpiderFollow(SpiderNewPublishFollow()))
    strategy[4] = Spider(SpiderRefresh())
    mode = input("1-4:")
    csuper = strategy[int(mode)]
    csuper.do("money")
