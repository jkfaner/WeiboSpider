#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/19 15:24
@Project:WeiboSpider
@File:downloaded.py
@Desc:
"""
import functools
import os
from typing import List, Union

from cache import Cache
from entity.media import Media
from entity.user import User
from utils.logger import logger
from utils.tool import getRedisKey, get_time_now


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

    def do_filter(self, medias: List[Media], user: User) -> Union[List[Media], bool]:
        cache = dict()
        # 去重顺序的博客id
        blog_id_list = [b.blog_id for b in medias]
        blog_id_list = sorted(set(blog_id_list), key=lambda x: blog_id_list.index(x))
        for blog_id in blog_id_list:
            cache[blog_id] = self.get_blog_progress(blog_id=blog_id)

        new_blogs = list()
        downloaded_num = 0
        for media in medias:
            progress = cache[media.blog_id]
            if not progress.downloaded_time and not progress.download_time:
                path, filepath = self.update_folder(
                    uid=media.blog.id,
                    screen_name=media.blog.screen_name,
                    folder_name=media.folder_name,
                    filename=media.filename
                )
                # 是否已经下载 包含下载完成的以及404错误的以及该路径文件是否存在
                # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
                # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
                is_finished = self.finish_download(uid=media.blog_id, url=media.url, filepath=filepath)
                if not is_finished:
                    media.filepath = filepath
                    new_blogs.append(media)
                else:
                    downloaded_num += 1
                    # 记录状态 已经下载
                    progress.download_num = 1 if progress.download_num is None else progress.download_num + 1
                    if progress.download_num == progress.media_num:
                        progress.download_time = get_time_now()
                        progress.downloaded_time = get_time_now()

        # 记录redis
        for p in cache.values():
            self.record_blog_progress(p)

        logger.info(f"[下载过滤]：【{user.screen_name}[{user.idstr}]】已下载{downloaded_num}条，未下载{len(new_blogs)}条")
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
            self.record_user_name(uid, screen_name)
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
        former_name_item = self.get_user_former_name(uid)
        for former_name in former_name_item.get("list"):
            # 查询曾用名地址
            old_path = os.path.join(os.path.join(self.rootPath, former_name), folder_name)
            if (os.path.exists(old_path)) and (former_name != screen_name) and (not os.path.exists(new_path)):
                # 存在且曾用名与现名不同
                os.rename(old_path, new_path)
                logger.info("更新文件夹成功：{} -> {}".format(old_path, new_path))
                # 记录现名
                self.record_user_name(uid, screen_name)
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
