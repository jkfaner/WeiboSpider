#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/21 17:56
@Project:WeiboSpider
@File:constants.py
@Desc:业务常量
"""
BLOG_FILTER_ORIGINAL = "original"
BLOG_FILTER_FORWARD = "forward"

DOWNLOAD_PATH_IMG_FORWARD_STR = "img/转发微博图片"
DOWNLOAD_PATH_VIDEO_FORWARD_STR = "video/转发微博视频"
DOWNLOAD_PATH_IMG_ORIGINAL_STR = "img/原创微博图片"
DOWNLOAD_PATH_VIDEO_ORIGINAL_STR = "video/原创微博视频"

REDIS_LOGIN_NAME = "weibo:login"  # 登录

REDIS_SPIDER_USER_START = "weibo:spider:blog:start"  # 最新爬取时间
REDIS_SPIDER_USER_FULL = "weibo:spider:blog:full"  # 是否完整爬取
SPIDER_BLOG_TIME = "weibo:spider:blog:time"  # 记录博客爬取的时间

REDIS_DOWNLOAD_FINISH_NAME = "weibo:spider:blog:download:ok"  # 已经下载
REDIS_DOWNLOAD_FAIL_NAME = "weibo:spider:blog:download:error"  # 下载错误

REDIS_SPIDER_USER_NAME = "weibo:spider:user:isSpider"  # 博主
REDIS_SPIDER_USER_FORMER_NAME = "weibo:spider:user:formerName"  # 曾用名

# 博客进度
SPIDER_PROGRESS = "weibo:spider:blog:progress"