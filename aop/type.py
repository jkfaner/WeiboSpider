#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 15:22
@Project:WeiboSpider
@File:type.py
@Desc:
"""
import functools
from typing import List, Union

from cache import Cache
from entity.blog import Blog
from entity.blogType import BlogType
from entity.progress import Progress
from utils import constants
from utils.logger import logger
from utils.tool import get_time_now, time_formatting


class FilterBlogType(Cache):

    def __init__(self, blog_type, *args, **kwargs):
        super(FilterBlogType, self).__init__()
        self.blog_type = blog_type
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            result = func(*args, **kwargs)
            blogs = self.do_filter(result)
            blogs = self._record_blog_progress(blogs)

            user = kwargs['user'].screen_name
            idstr = kwargs['user'].idstr
            message = f"[博客类型过滤]：得到【{user}[{idstr}]】的博客，当前有{len(blogs)}条博客存在媒体数据"
            logger.info(message)
            return blogs

        return wrapper

    def do_filter(self, blogs: List[BlogType]) -> List[Union[Blog, BlogType]]:
        if not self.blog_type:
            return blogs
        new_blogs = list()
        for blog in blogs:
            if self.blog_type == constants.BLOG_FILTER_ORIGINAL:
                # 获取原创
                if blog.original:
                    new_blogs.append(blog.original)
            elif self.blog_type == constants.BLOG_FILTER_FORWARD:
                # 获取转发
                if blog.forward:
                    new_blogs.append(blog.forward)
            else:
                # 原创+转发
                if blog.original:
                    new_blogs.append(blog.original)
                if blog.forward:
                    new_blogs.append(blog.forward)
        return new_blogs

    def _record_blog_progress(self, blogs: List[Union[Blog, BlogType]]) -> List[Union[Blog, BlogType]]:
        # 记录进度并过滤无媒体数据
        new_blogs = list()
        for blog in blogs:
            # 媒体数据
            media_num = len(blog.images) + len(blog.livephoto_video)
            if blog.videos and blog.videos.url:
                media_num += 1

            p = Progress()
            p.uid = blog.id
            p.blog_id = blog.blog_id
            p.blog_create_time = time_formatting(blog.created_at, usefilename=False, strftime=True)
            p.start_time = get_time_now()
            p.media_num = media_num
            if media_num == 0:
                p.downloaded_time = get_time_now()
                p.parse_time = get_time_now()
                p.download_num = 0
                p.download_error_num = 0
                p.download_time = get_time_now()
            else:
                new_blogs.append(blog)
            self.record_blog_progress(p)
        return new_blogs
