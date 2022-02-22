#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
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
from init import redisPoolObj
from middleware.spiderMinddleware import SpiderMinddleware
from request.download import Download
from request.fetch import Session
from request.login import Login
from request.requestIter import RequestIter
import utils.businessConstants as constants
from utils.exception import ParameterError, DateError
from utils.logger import logger


class Main(SpiderMinddleware,Session):
    mode_follow_weibo = "follow_weibo"
    mode_follow_img = "follow_img"
    mode_refresh = "refresh"
    spider_mode_item = dict(follow_weibo="爬取关注", refresh="刷微博")
    requestIter = RequestIter()
    download = Download()

    def get_follow(self, mode: str):
        """
        爬取关注的数据
        :param mode:
        :return:
        """
        if mode == constants.SPIDER_FOLLOW_MODE:
            # 默认获取用户关注
            # 获取uid
            login = Login()
            cookies_item = login.select_cookies()
            if cookies_item:
                uid =cookies_item['uid']
            else:
                login.login_online(session=self.session, insert=True)
                cookies_item = login.select_cookies()
                uid =cookies_item['uid']

            for item in self.requestIter.getUserFollowIter(uid=uid):
                yield self.parse_user(item)

        elif mode == constants.SPIDER_FOLLOW_MODE_NEW:
            # 通过获取用户最新关注顺序
            for item in self.requestIter.getUserFollowByNewFollowIter():
                yield self.parse_user(item)

        elif mode == constants.SPIDER_FOLLOW_MODE_NEW_PUBLISH:
            # 通过获取最新有发布的用户顺序
            for item in self.requestIter.getUserFollowByNewPublicIter():
                yield self.parse_user(item)
        else:
            raise ParameterError("参数错误：'{}'不在规则范围内。".format(mode))

    def get_blog(self,users:List[UserEntity]):
        """
        获取博客
        :param user:
        :return:
        """
        for user in users:
            for blog in self.requestIter.getUserBlogIter(uid=user.idstr):
                blogs = None
                try:
                    blogs = self.filter_blog(response=blog,user=user)
                except DateError as e:
                    blogs = e.args[1]
                    break
                finally:
                    if blogs:
                        yield blogs,user
                    time.sleep(2)
            # TODO DEBUG
            #     break
            # break


    def run(self):
        for users in self.get_follow("最新发布"):
            for blog,user in self.get_blog(users=users):
                download_datas = self.download.filter_download(blogs=blog,user=user)
                self.download.startDownload(download_datas)


if __name__ == '__main__':
    while True:
        m = Main()
        m.run()
        logger.info("关闭redis中...")
        redisPoolObj.disconnect()
        logger.info("等待中...")
        time.sleep(60*30)
