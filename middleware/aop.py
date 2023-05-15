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
import logging
from typing import List
from collections.abc import Iterator
import utils.constants as constants
from entity.downloadEntity import DownloadEntity
from loader import ProjectLoader
from utils.logger import logger, Logger

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

        def init_update_folder(download_datas: List[DownloadEntity]) -> list[DownloadEntity]:
            # 遵循先后原则 重复后者覆盖前者 uid唯一不变
            cache = set()
            result = list()
            for download_data in download_datas[::-1]:
                uid = download_data.blog.id
                if uid not in cache:
                    cache.add(uid)
                    result.append(download_data)
            return result

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            download_datas = func(self, *args, **kwargs)
            new_download_datas = list()
            for download_data in init_update_folder(download_datas):
                uid = download_data.blog.id
                screen_name = download_data.blog.screen_name
                folder_name = download_data.folder_name
                filename = download_data.filename
                path, filepath = self.update_folder(uid, screen_name, folder_name, filename)
                # 是否已经下载 包含下载完成的以及404错误的以及该路径文件是否存在
                # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
                # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
                if not self.finish_download(blog_id=download_data.blog_id, url=download_data.url, filepath=filepath):
                    download_data.filepath = filepath
                    new_download_datas.append(download_data)
            return new_download_datas

        return new_func


class LoggerAOP(Logger):

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.level == logging.INFO:
                self.logger.info(self.message)
            elif self.level == logging.DEBUG:
                self.logger.debug(self.message)
            elif self.level == logging.WARNING:
                self.logger.warning(self.message)
            elif self.level == logging.ERROR:
                self.logger.error(self.message)
            elif self.level == logging.CRITICAL:
                self.logger.critical(self.message)
            else:
                raise "日志类型设置错误"
            return func(*args, **kwargs)

        return wrapper

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
