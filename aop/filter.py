#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/18 17:16
@Project:WeiboSpider
@File:filter.py
@Desc:
"""
import functools
import os

from cache import Cache
from entity.user import User
from utils import constants
from utils.logger import logger
from utils.tool import compare_date, getRedisKey, time_formatting


class FilterUser:

    def __init__(self, filter_users, *args, **kwargs):
        self.filter_users = filter_users
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            result = func(*args, **kwargs)
            return self.do_filter(result)

        return wrapper

    def do_filter(self, users):
        if not self.filter_users:
            return users
        users = [user for user in users if user.idstr in self.filter_users]
        logger.info("[博主过滤]：有[{}]位博主的数据将会被采集".format(len(users)))
        return users


class FilterBlogType:

    def __init__(self, blog_type, *args, **kwargs):
        self.blog_type = blog_type
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            result = func(*args, **kwargs)
            return self.do_filter(result, *args, **kwargs)

        return wrapper

    def do_filter(self, blogs, *args, **kwargs):
        """
        通过筛选条件筛选博客
        原创 or 转发 or 原创+转发
        :param blogs:
        :param args:
        :param kwargs:
        :return:
        """
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

        user = kwargs['user'].screen_name
        idstr = kwargs['user'].idstr
        message = f"[博客类型过滤]：得到【{user}[{idstr}]】的博客，当前有{len(new_blogs)}条博客"
        logger.info(message)
        return new_blogs


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

    def do_filter(self, blogs, *args, **kwargs):
        user = kwargs["user"]  # 博主

        # 1.拿到博主的最后采集时间
        spider_time = self.get_spider_time(user.idstr)
        # 初次采集
        if spider_time is None:
            logger.info(f"[博客日期过滤]：初次采集【{user.screen_name}[{user.idstr}]】的博客，当前有{len(blogs)}条博客")
            return blogs

        # 2.增量采集
        # 拿到已经全量采集的用户
        full_uid_list = self.get_complete()
        new_blogs = list()
        if user.idstr in full_uid_list:
            # 遍历检查博客的时间
            for blog in blogs:
                # 放行上次记录之后的数据,且排除置顶(置顶优先爬取,全量即爬)
                if compare_date(stime=blog.created_at, etime=spider_time) and not blog.is_top:
                    new_blogs.append(blog)
            logger.info(f"[博客日期过滤]：增量采集【{user.screen_name}[{user.idstr}]】的博客，当前有{len(new_blogs)}条博客")
            if len(new_blogs) == 0:
                # 博主未更新中止采集
                return []
        else:
            # 3.间断采集
            # 遍历博客检查博客时间
            for blog in blogs:
                # 排除最后采集时间之后的博客,获取该时间之前的数据,且排除置顶博客
                if compare_date(stime=blog.created_at, etime=spider_time) and not blog.is_top:
                    new_blogs.append(blog)
            logger.info(f"[博客日期过滤]：间断采集【{user.screen_name}[{user.idstr}]】的博客，当前有{len(new_blogs)}条博客")

        return new_blogs


class FilterDownloaded(Cache):

    def __init__(self, *args, **kwargs):
        super(FilterDownloaded, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 执行装饰器操作
            result = func(*args, **kwargs)
            return self.do_filter(result, user=kwargs["user"])

        return wrapper

    def do_filter(self, blogs, user: User):
        # 没有媒体数据且全部采集过 更新采集时间
        if not blogs and user.idstr not in self.get_complete():
            self.record_spider_time(uid=user.idstr)
            logger.info("[下载过滤]：【{}[{}]】的博客不存在媒体数据且已经全量采集过".format(user.screen_name, user.idstr))
            return
        new_blogs = list()
        downloaded_blogs = list()
        for blog in blogs:
            uid = blog.blog.id
            screen_name = blog.blog.screen_name
            folder_name = blog.folder_name
            filename = blog.filename
            path, filepath = self.update_folder(uid, screen_name, folder_name, filename)
            # 是否已经下载 包含下载完成的以及404错误的以及该路径文件是否存在
            # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
            # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
            is_finished = self.finish_download(uid=blog.blog_id, url=blog.url, filepath=filepath)
            if not is_finished:
                blog.filepath = filepath
                new_blogs.append(blog)
            else:
                downloaded_blogs.append(blog)
                logger.info(f"[下载过滤]：【{user.screen_name}[{user.idstr}]】在{time_formatting(blog.created_at)}发表的博客，该媒体数据曾经已经成功下载")

        logger.info(f"[下载过滤]：【{user.screen_name}[{user.idstr}]】已下载{len(downloaded_blogs)}条，未下载{len(new_blogs)}条")
        return new_blogs

    def update_folder(self, uid: str, screen_name: str, folder_name: str, filename: str) -> tuple:
        """
        更新文件夹

        文件夹：self.rootPath/screen_name/folder_name
        os.path.join(os.path.join(self.rootPath, screen_name), folder_name)

        :param uid: uid
        :param filename: 20230514_4901317619223955_1.jpg
        :param folder_name: img/原创微博图片
        :param screen_name: 来去之间
        :return:
        """
        # 查询用户名是否存在
        _screen_name = self.select_weibo_user(uid=uid)
        if not _screen_name:
            new_path = os.path.join(os.path.join(self.rootPath, screen_name), folder_name)
            # 不存在->已修改
            self.update_folder_name(uid, screen_name, folder_name)
            # 更新博主screen_name
            self.update_weibo_user(uid=uid, screen_name=screen_name)
        else:
            # 存在->未修改、已修改
            self.update_folder_name(uid, _screen_name, folder_name)
            new_path = os.path.join(os.path.join(self.rootPath, _screen_name), folder_name)
            # 更新数据
            self.update_weibo_user(uid=uid, screen_name=_screen_name)
            # 记录曾用名
            self.insert_weibo_screen_name(uid, screen_name)
        filepath = os.path.join(new_path, filename)
        return new_path, filepath

    def update_folder_name(self, uid: str, screen_name: str, folder_name: str):
        """
        修改文件夹名称
        （需要就修改不需要就不修改）
        :param uid: uid
        :param screen_name: 来去之间（现名）
        :param folder_name: img/原创微博图片
        :return: True-修改
        """
        new_path = os.path.join(os.path.join(self.rootPath, screen_name), folder_name)
        # 查询曾用名
        former_name_item = self.select_weibo_former_name(uid)
        for former_name in former_name_item.get("list"):
            # 查询曾用名地址
            old_path = os.path.join(os.path.join(self.rootPath, former_name), folder_name)
            if (os.path.exists(old_path)) and (former_name != screen_name) and (not os.path.exists(new_path)):
                # 存在且曾用名与现名不同
                os.rename(old_path, new_path)
                logger.info("更新文件夹成功：{} -> {}".format(old_path, new_path))
                # 记录现名
                self.insert_weibo_screen_name(uid, screen_name)
                return True
        # 创建：首次、未修改
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            logger.info("文件夹创建成功：{}".format(new_path))
        return False

    def finish_download(self, uid, url, filepath):
        """
        是否已经下载完成

        注意：删除redis后仅通过配置路径下载文件进行判断
        :param uid:
        :param url:
        :param filepath:
        :return:
        """
        # 获取媒体地址在redis中的哈希值 条件：uid+链接+文件地址
        key = getRedisKey(uid=uid, url=url, filepath=filepath)

        # 获取媒体是否已经下载完成标识
        finished = self.check_finished(key=key)
        # 获取媒体异常标识
        error_404 = self.check_error(key=key)
        if error_404:
            # 媒体异常->媒体下载完成
            return True

        # 检查文件是否存在 存在分为两种情况：完整数据文件、非完整数据文件（该类数据会继续下载）
        file_in_path = os.path.exists(filepath)
        if not file_in_path:
            if finished:
                # 本地文件不存在，且已经下载完成（之前）->媒体下载完成
                return True
            return False
        else:
            if finished:
                # 本地文件存在，且已经完成下载->媒体下载完成
                return True
            # 本地文件存在，未被记录下载标志(此时存在文件不完成情况，故不记录)->未下载
        return False


class CompleteDownload(Cache):

    def __init__(self, *args, **kwargs):
        super(CompleteDownload, self).__init__()
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            blogs = kwargs['blogs']
            user = kwargs['user']
            if len(blogs) == 1 and blogs[0] == user.idstr:
                # 当前博主已经完成全量爬取
                self.record_complete(user.idstr)
                logger.info("[全部完成]：【{}[{}]】的媒体数据已经全部采集完毕".format(user.screen_name, user.idstr))
                return []
            # 执行装饰器操作
            return func(*args, **kwargs)

        return wrapper
