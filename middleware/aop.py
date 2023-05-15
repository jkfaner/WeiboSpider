#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/14 23:05
@Project:WeiboSpider
@File:aop.py
@Desc:
"""
import functools
from typing import List

import utils.constants as constants
from loader import ProjectLoader
from utils.logger import logger

filter_config = ProjectLoader.getSpiderConfig().get("filter")
FILTER_USER = filter_config.get("filter-user")
FILTER_BLOG = filter_config.get("filter-blog")


def parse_user(users: List) -> List:
    return [user.split("/")[-1] for user in users]


original_users = parse_user(filter_config.get("original"))
forward_users = parse_user(filter_config.get("forward"))
FILTER_TYPE = filter_config.get("filter-type")
if FILTER_TYPE == "original":
    USERS_LIST = list(set(original_users))
elif FILTER_TYPE == "forward":
    USERS_LIST = list(set(forward_users))
else:
    original_users.extend(forward_users)
    USERS_LIST = list(set(original_users))


class FilterAOP:

    def filter_user(func):
        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            userObjs = func(self, *args, **kwargs)
            if not FILTER_USER:
                return userObjs
            users = [userObj for userObj in userObjs if userObj.idstr in USERS_LIST]
            logger.info("筛选得到的用户，共{}条:".format(len(users)))
            for user in users:
                logger.info(user.screen_name)
            return users

        return new_func

    def filter_blog_by_type(func):
        """
        通过筛选条件筛选博客
        原创 or 转发 or 原创+转发
        :return:
        """

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            blogs = func(self, *args, **kwargs)
            if not FILTER_BLOG:
                return blogs
            new_blogs = list()
            for blog in blogs:
                if FILTER_TYPE == constants.BLOG_FILTER_ORIGINAL:
                    # 获取原创
                    if blog.original:
                        new_blogs.append(blog.original)
                elif FILTER_TYPE == constants.BLOG_FILTER_FORWARD:
                    # 获取转发
                    if blog.forward:
                        new_blogs.append(blog.forward)
                else:
                    # 原创+转发
                    if blog.original:
                        new_blogs.append(blog.original)
                    if blog.forward:
                        new_blogs.append(blog.forward)

            len_blogs = len(new_blogs)
            for index, new_blog in enumerate(new_blogs):
                msg1 = "[{index}/{len_blogs}]".format(index=index, len_blogs=len_blogs)
                msg2 = "[原创|转发|所有]"
                msg3 = f"筛选博客:{kwargs['user'].idstr}->{kwargs['user'].screen_name} ->> {new_blog.blog_id}"
                logger.info(msg1 + msg2 + msg3)
            return new_blogs

        return new_func

    def filter_blog_by_date(func):
        """通过设置的日期筛选博客"""

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            blogs = func(self, *args, **kwargs)
            new_blogs = list()
            # for blog in blogs:
            #     # 筛选爬取时间
            #     if not blog.is_top and not match_date(create_time=blog.created_at, filter_date=user_crawl.date):
            #         # 不符合时间&不是置顶数据 抛出异常 捕获异常后需要中断爬取
            #         create_time = time_formatting(blog.created_at, usefilename=False, strftime=True)
            #         logger.warning(f"[{user_crawl.date}]筛选的博客不在配置的下载时间之后:{create_time}")
            #         raise DateError("筛选的博客不在配置的下载时间内", new_blogs)
            #     else:
            #         new_blogs.append(blog)
            # en_blogs = len(new_blogs)
            # for index, new_blog in enumerate(new_blogs, 1):
            #     user_msg = f"{user.idstr}->{user.screen_name}"
            #     blog_msg = f"{new_blog.blog_id}->{time_formatting(created_at=new_blog.created_at, usefilename=False, strftime=True)}"
            #     msg = f"[{index}/{len_blogs}]通过日期[{user_crawl.date}]筛选博客:{user_msg} -->> {blog_msg}"
            #     logger.info(msg)
            return blogs

        return new_func

    def filter_download(func):
        """下载筛选->通过已下载和404筛选"""

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            download_datas = func(self, *args, **kwargs)
            new_download_datas = list()
            for download_data in download_datas:
                path, filepath = self.update_folder(download_data)
                # 是否已经下载 包含下载完成的以及404错误的以及该路径文件是否存在
                # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
                # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
                if not self.finish_download(blog_id=download_data.blog_id, url=download_data.url, filepath=filepath):
                    download_data.filepath = filepath
                    new_download_datas.append(download_data)
            return new_download_datas

        return new_func


class LoggerAOP:

    def extractor_user_log(func):
        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            users = func(self, *args, **kwargs)
            for index, user in enumerate(users, 1):
                logger.info(f"[{index}/{len(users)}]提取用户:{user.idstr}->{user.screen_name}")
            return users

        return new_func

    def extractor_blog_log(func):
        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            blogs = func(self, *args, **kwargs)
            logger.info(f"[{len(blogs)}]提取博客:{kwargs['user'].idstr}->{kwargs['user'].screen_name}")
            return blogs

        return new_func
