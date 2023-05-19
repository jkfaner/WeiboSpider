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
import sched
import time

from loader import ProjectLoader
from main import SpiderFollow, SpiderDefaultFollow, SpiderNewFollow, SpiderNewPublishFollow, SpiderRefresh


def main():
    spider_set = {
        # 爬取关注博主->默认规则
        1: SpiderFollow(SpiderDefaultFollow()),
        # 爬取关注博主->最新关注规则
        2: SpiderFollow(SpiderNewFollow()),
        # 爬取关注博主->最新发布规则
        3: SpiderFollow(SpiderNewPublishFollow()),
        # 刷微博
        4: SpiderRefresh(None),
    }
    rule = ProjectLoader.getSpiderConfig()["rule"]
    obj = spider_set[rule]
    obj.execute()


class StrategyScheduler:
    def __init__(self, strategy, interval):
        self.strategy = strategy
        self.interval = interval
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def _execute_strategy(self):
        self.strategy.execute()
        self.scheduler.enter(self.interval, 1, self._execute_strategy)

    def start(self):
        self.scheduler.enter(0, 1, self._execute_strategy)
        self.scheduler.run()


def task():
    spider_set = {
        # 爬取关注博主->默认规则
        1: StrategyScheduler(SpiderFollow(SpiderDefaultFollow()), 60*60),
        # 爬取关注博主->最新关注规则
        2: StrategyScheduler(SpiderFollow(SpiderNewFollow()), 60*60),
        # 爬取关注博主->最新发布规则
        3: StrategyScheduler(SpiderFollow(SpiderNewPublishFollow()), 60*60),
        # 刷微博
        4: StrategyScheduler(SpiderRefresh(None), 60*60),
    }
    rule = ProjectLoader.getSpiderConfig()["rule"]
    obj = spider_set[rule]
    # 启动策略调度器
    obj.start()


if __name__ == '__main__':
    task()
