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
import sys
from typing import List

import utils.constants as constants
from loader import ProjectLoader
from utils.logger import logger, Logger
from utils.tool import compare_date, time_formatting

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

        def after(userObjs):
            if not FILTER_USER:
                return userObjs
            users = [userObj for userObj in userObjs if userObj.idstr in USERS_LIST]
            logger.info("筛选得到的用户，共{}条:".format(len(users)))
            for user in users:
                logger.info(user.screen_name)
            return users

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            userObjs = func(self, *args, **kwargs)
            return after(userObjs)

        return new_func

    def filter_blog_by_type(func):

        def after(blogs, *args, **kwargs) -> List:
            """
            通过筛选条件筛选博客
                原创 or 转发 or 原创+转发
            :param blogs:
            :param args:
            :param kwargs:
            :return:
            """
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

            message = f"[过滤类型]：放行--> {kwargs['user'].screen_name}[{kwargs['user'].idstr}]的{len(new_blogs)}条博客"
            logger.info(message)
            return new_blogs

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            blogs = func(self, *args, **kwargs)
            return after(blogs=blogs, *args, **kwargs)

        return new_func

    def filter_blog_by_date(func):
        """通过设置的日期筛选博客"""

        def log(blog, message):
            ctime = time_formatting(blog.created_at, usefilename=False, strftime=True)
            videos_length = 0 if not blog.videos else 1
            message_str1 = f"[过滤日期] 放行--> {message}：{blog.screen_name}[{blog.id}] 在{ctime}发表的博客，"
            message_str2 = f"包含：{len(blog.images)}张图片、{len(blog.livephoto_video)}条live视频、{videos_length}条视频"
            logger.info(message_str1 + message_str2)

        def filter_data(self, blog, entity, new_blogs):
            if entity.id is None:
                return
            spider_new_time = self.download.redis_client.hget(name=constants.REDIS_SPIDER_USER_START, key=entity.id)

            # 没有爬取记录（下载记录）：直接放行
            if spider_new_time is None:
                log(entity, "首次爬取")
                new_blogs.append(blog)
                return

            full_uid_list = [i for i in self.download.redis_client.sscan_iter(name=constants.REDIS_SPIDER_USER_FULL)]
            if str(entity.id) in full_uid_list:

                # 已经全量爬取，但是无下载记录，可能下载记录被删除：直接放行
                if spider_new_time is None:
                    log(entity, "未成功记录")
                    new_blogs.append(blog)
                    return

                # 放行上次记录之后的数据,且排除置顶(置顶优先爬取,全量即爬)
                if compare_date(stime=entity.created_at, etime=spider_new_time) and not entity.is_top:
                    log(entity, "已全量爬取")
                    new_blogs.append(blog)
                    return
            else:
                # 未全量且非首次（可能全量数据未记录）
                log(entity, "未全量且非首次")
                new_blogs.append(blog)

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            # 1.已经全量爬取 -> 记录当前时间 下次放行此时间之后的载数据
            # 2.未全量爬取 -> 放行所以数据
            # 注意置顶内容
            blogs = func(self, *args, **kwargs)
            new_blogs = list()
            for blog in blogs:
                forward = blog.forward
                original = blog.original
                if forward:
                    filter_data(self, blog, forward, new_blogs)
                if original:
                    filter_data(self, blog, original, new_blogs)
            return new_blogs

        return new_func

    def filter_download(func):
        """下载筛选->通过已下载和404筛选"""

        def after(self, download_datas):
            new_download_datas = list()

            for download_data in download_datas:
                uid = download_data.blog.id
                screen_name = download_data.blog.screen_name
                folder_name = download_data.folder_name
                filename = download_data.filename
                path, filepath = self.update_folder(uid, screen_name, folder_name, filename)
                # 是否已经下载 包含下载完成的以及404错误的以及该路径文件是否存在
                # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
                # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
                is_finished = self.finish_download(uid=download_data.blog_id, url=download_data.url, filepath=filepath)
                if not is_finished:
                    download_data.filepath = filepath
                    new_download_datas.append(download_data)
            return new_download_datas

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            download_datas = func(self, *args, **kwargs)
            return after(self, download_datas)

        return new_func

    def all_download(func):
        """全量下载"""

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            blogs = kwargs['blogs']
            user = kwargs['user']
            if len(blogs) == 1 and blogs[0] == user.idstr:
                # 当前博主已经完成全量爬取
                self.download.redis_client.sadd(constants.REDIS_SPIDER_USER_FULL, user.idstr)
                return
            return func(self, *args, **kwargs)

        return new_func


class LoggerAOP(Logger):

    @staticmethod
    def format_str(message: str, index: int or List, *args, **kwargs):
        dict_count = message.count("{}")
        index_len = index
        if isinstance(index, list):
            index_len = len(index)
        if dict_count != index_len and index == -1:
            sys.exit("ERROR: LoggerAOP.format_str")
        if isinstance(index, int):
            return message.format(args[index])
        format_list = list()
        if isinstance(index, list):
            for i in index:
                format_list.append(eval(i))
        return message.format(*format_list)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            message = self.message
            if "{}" in message:
                message = self.format_str(message, self.format_index, *args, **kwargs)
            if self.level == logging.INFO:
                self.logger.info(message)
            elif self.level == logging.DEBUG:
                self.logger.debug(message)
            elif self.level == logging.WARNING:
                self.logger.warning(message)
            elif self.level == logging.ERROR:
                self.logger.error(message)
            elif self.level == logging.CRITICAL:
                self.logger.critical(message)
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
            message = f"[解析博客]：成功解析--> {kwargs['user'].screen_name}[{kwargs['user'].idstr}]发布的{len(blogs)}条博客"
            logger.info(message)
            return blogs

        return new_func
