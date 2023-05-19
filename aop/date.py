#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 15:23
@Project:WeiboSpider
@File:date.py
@Desc:
"""
import functools
from typing import List, Union

from cache import Cache
from entity.blog import Blog
from entity.blogType import BlogType
from entity.progress import Progress
from utils.logger import logger
from utils.tool import compare_date, get_time_now


class FilterBlogDate(Cache):

    def __init__(self, *args, **kwargs):
        super(FilterBlogDate, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            result = func(*args, **kwargs)
            return self.do_filter(result, *args, **kwargs)

        return wrapper

    def do_filter(self, blogs: List[Union[Blog, BlogType]], *args, **kwargs) -> Union[List[Blog], bool]:
        user = kwargs["user"]  # 博主
        is_full = False
        # 判断是否全量爬取
        if self.check_full_download(uid=user.idstr):
            is_full = True

        if is_full and not blogs:
            logger.info(f"[博客日期过滤]：【{user.screen_name}[{user.idstr}]】已经全部采集完毕，并未更新内容")
            return False

        if not blogs:
            logger.info(f"[博客日期过滤]：没有【{user.screen_name}[{user.idstr}]】的博客，无法过滤")
            return blogs

        new_blogs = list()
        for blog in blogs:
            progress = self.get_blog_progress(blog.blog_id)
            if not progress.download_time or not progress.downloaded_time:
                new_blogs.append(blog)
            progress.parse_time = get_time_now()
            self.record_blog_progress(progress)

        if is_full and not new_blogs or not blogs:
            logger.info(f"[博客日期过滤]：【{user.screen_name}[{user.idstr}]】已经全部采集完毕，并未更新内容")
            return False

        logger.info(f"[博客日期过滤]：【{user.screen_name}[{user.idstr}]】共{len(blogs)}条博客，其中未采集有{len(new_blogs)}条")
        return new_blogs