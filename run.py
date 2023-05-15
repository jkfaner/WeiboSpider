#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/15 16:06
@Project:WeiboSpider
@File:run.py
@Desc:
"""
from loader import ProjectLoader
from main import Spider, SpiderDefaultFollow, SpiderFollow, SpiderNewFollow, SpiderNewPublishFollow, SpiderRefresh


def main():
    spider_set = {
        # 爬取关注博主->默认规则
        1: Spider(SpiderFollow(SpiderDefaultFollow())),
        # 爬取关注博主->最新关注规则
        2: Spider(SpiderFollow(SpiderNewFollow())),
        # 爬取关注博主->最新发布规则
        3: Spider(SpiderFollow(SpiderNewPublishFollow())),
        # 刷微博
        4: Spider(SpiderRefresh()),
    }
    rule = ProjectLoader.getSpiderConfig()["rule"]
    obj = spider_set[rule]
    obj.run("run...")


if __name__ == '__main__':
    main()
