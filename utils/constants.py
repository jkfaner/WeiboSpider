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

REDIS_DOWNLOAD_FINISH_NAME = "weibo_blogFinished"
REDIS_DOWNLOAD_FAIL_NAME = "weibo_blog404"