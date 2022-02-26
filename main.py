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
from typing import List, Tuple

import utils.businessConstants as constants
from config.load import create_new_spiderInfo
from entity.spiderConfigEntity import SpiderCrawlItemConfig
from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from init import spider_config
from middleware.spiderMinddleware import SpiderMinddleware
from request.download import Download
from request.fetch import Session
from request.login import Login
from request.requestIter import RequestIter
from utils.exception import ParameterError, DateError
from utils.logger import logger


class InitMain(SpiderMinddleware, Session):
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
        download_datas = self.download.filter_download(blogs=blogs, user=user)
        self.download.startDownload(download_datas)


class FollowMain(InitMain):

    def get_follow(self, spider_follow_mode: str):
        """
        爬取关注的数据
        :param spider_follow_mode:
        :return:
        """
        if spider_follow_mode == constants.SPIDER_FOLLOW_MODE:
            # 默认获取用户关注
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
                yield self.parse_user(item)

        elif spider_follow_mode == constants.SPIDER_FOLLOW_MODE_NEW:
            # 通过获取用户最新关注顺序
            for item in self.requestIter.getUserFollowByNewFollowIter():
                yield self.parse_user(item)

        elif spider_follow_mode == constants.SPIDER_FOLLOW_MODE_NEW_PUBLISH:
            # 通过获取最新有发布的用户顺序
            for item in self.requestIter.getUserFollowByNewPublicIter():
                yield self.parse_user(item)
        else:
            raise ParameterError("参数错误：'{}'不在规则范围内。".format(spider_follow_mode))

    def get_blog(self, users: List[Tuple[UserEntity, SpiderCrawlItemConfig]]):
        """
        获取博客
        :param user:
        :return:
        """
        for user, user_crawl in users:
            for blog in self.requestIter.getUserBlogIter(uid=user.idstr):
                blogs = None
                try:
                    blogs = self.filter_blog(response=blog, user=user, user_crawl=user_crawl)
                except DateError as e:
                    blogs = e.args[1]
                    break
                finally:
                    if blogs:
                        yield blogs, user
                    time.sleep(2)


class Main(FollowMain):

    def run(self):
        """
        运行
        :return:
        """
        if spider_config.mode == constants.SPIDER_MODE_FOLLOW:
            # 爬取关注
            for users in self.get_follow(spider_follow_mode=spider_config.follow_mode):
                for blogs, user in self.get_blog(users=users):
                    self.start_download(blogs=blogs, user=user)

        elif spider_config.mode == constants.SPIDER_MODE_REFRESH:
            # TODO 刷微博
            raise Exception("未定义：{}".format(spider_config.mode))
        else:
            raise ParameterError("参数错误：'{}'不在规则范围内。".format(spider_config.mode))


def main():
    m = Main()
    m.run()


if __name__ == '__main__':
    while True:
        main()
        create_new_spiderInfo()
        sleep_time = 60 * 5
        while sleep_time > 0:
            print('\r等待再次运行，倒计时(s):{}'.format(sleep_time), flush=True, end='')
            time.sleep(1)
            sleep_time -= 1