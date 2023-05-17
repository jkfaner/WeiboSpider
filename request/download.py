#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/12 11:13
@Project:WeiboSpider
@File:download.py
@Desc:
"""
import logging
import os
from typing import List

import requests
from tqdm import tqdm

import utils.constants as constants
from entity.downloadEntity import DownloadEntity
from entity.user import User
from entity.blog import Blog
from loader import ProjectLoader
from aop import FilterAOP, LoggerAOP
from utils.exception import NOTContentLengthError, FinishedError, NotFound
from utils.logger import logger
from utils.tool import getRedisKey, time_formatting, get_time_now
from utils.tool import thread_pool, EntityToJson


class DownloadLoader(object):
    _spider_config = ProjectLoader.getSpiderConfig()
    _database_config = ProjectLoader.getDatabaseConfig()
    _redis_client = ProjectLoader.getRedisClient()

    def __init__(self):
        self.root_path = self._spider_config["download"]["root"]
        self.redis_client = self._redis_client
        self.thread = self._spider_config["download"]["thread"]
        self.workers = self._spider_config["download"]["workers"]


class RedisCache(DownloadLoader):

    def select_weibo_user(self, uid: str):
        """
        查询数据库微博用户
        :param uid:
        :return:
        """
        return self.redis_client.hget(constants.REDIS_SPIDER_USER_NAME, uid)

    def update_weibo_user(self, uid: str, screen_name: str):
        """
        插入数据&更新数据 数据库有数据就写入 没数据就跟行 weibo_id为唯一索引
        :param uid:
        :param screen_name:
        :return:
        """
        self.redis_client.hset(constants.REDIS_SPIDER_USER_NAME, uid, screen_name)


class Cache(RedisCache):
    pass


class DownloadMiddleware(Cache):

    def __init__(self):
        super(DownloadMiddleware, self).__init__()
        # 创建weibo专属路径
        self.rootPath = os.path.join(self.root_path, "weibo")
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)

    @staticmethod
    def get_file_suffix(url):
        """
        通过url确定文件后缀
        # url = "http://zzx.sinaimg.cn/large/008bRrn7ly1gzolla2v1yj564w3g94qv2.jpg?KID=imgbed,photo&Expires=1677222140&ssig=NZi9yMSvUa&uid=7367188627&referer=weibo.com"
        # url = "http://zzx.sinaimg.cn/large/008bRrn7ly1gzolla2v1yj564w3g94qv2.jpg"
        # url = "https://video.weibo.com/media/play?livephoto=https%3A%2F%2Fus.sinaimg.cn%2F001rxuzpgx07TMPgS3TG0f0f0100mrIJ0k01.mov"
        :param url:
        :return:
        """
        try:
            http_path = os.path.split(url)
            filename = http_path[1].split("?")[0]
            if "." in filename:
                suffix = filename.split(".")[-1]
            else:
                livephoto_path = http_path[1].split("?")[1]
                suffix = livephoto_path.split(".")[-1]
            return suffix
        except IndexError:
            logger.error("通过url确定文件后缀:{}".format(url))
            import sys
            sys.exit()

    @FilterAOP.filter_download
    @LoggerAOP(message="[{}]博客数据分发中:{}", index=["kwargs['user'].screen_name", "len(kwargs['blogs'])"],
               level=logging.INFO, save=True)
    def distribute_data(self, blogs: List[Blog], user: User) -> List[DownloadEntity]:
        """
        数据分发
        :param blogs:
        :param user:
        :return:
        """
        new_blogs = list()
        for blog in blogs:
            base_filename = "{}_{}".format(time_formatting(blog.created_at), blog.blog_id)
            # 视频
            if blog.videos:
                filename = "{}.mp4".format(base_filename)

                video_download_entity = DownloadEntity()
                video_download_entity.blog = blog
                video_download_entity.blog_id = blog.blog_id
                video_download_entity.filename = filename
                video_download_entity.folder_name = blog.video_str
                video_download_entity.url = blog.videos.url
                new_blogs.append(video_download_entity)

            # 图片
            for image in blog.images:
                suffix = self.get_file_suffix(image["url"])
                filename = "{}_{}.{}".format(base_filename, image['index'], suffix)

                image_download_entity = DownloadEntity()
                image_download_entity.blog = blog
                image_download_entity.blog_id = blog.blog_id
                image_download_entity.filename = filename
                image_download_entity.folder_name = blog.image_str
                image_download_entity.url = image['url']
                new_blogs.append(image_download_entity)

            # livephoto
            for livephoto in blog.livephoto_video:
                suffix = self.get_file_suffix(livephoto["url"])
                filename = "{}_{}.{}".format(base_filename, livephoto['index'], suffix)

                livephoto_download_entity = DownloadEntity()
                livephoto_download_entity.blog = blog
                livephoto_download_entity.blog_id = blog.blog_id
                livephoto_download_entity.filename = filename
                livephoto_download_entity.folder_name = blog.video_str
                livephoto_download_entity.url = livephoto['url']
                new_blogs.append(livephoto_download_entity)

        return new_blogs

    def update_folder(self, uid: str, screen_name: str, folder_name: str, filename: str) -> tuple:
        """
        更新文件夹
        :param uid:
        :param filename:
        :param folder_name:
        :param screen_name:
        :return:
        """
        _screen_name = self.select_weibo_user(uid=uid)
        if not _screen_name:
            # 创建文件夹
            path = os.path.join(os.path.join(self.rootPath, screen_name), folder_name)
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info("文件夹创建成功：{}".format(path))
            self.update_weibo_user(uid=uid, screen_name=screen_name)
        else:
            # 数据库有数据
            # 修改本地文件夹
            # '/Users/xxx/Downloads/weibo/_screen_name'
            _screen_name_path = os.path.join(self.rootPath, _screen_name)
            # '/Users/xxx/Downloads/weibo/_screen_name/img/原创微博图片'
            _path = os.path.join(_screen_name_path, folder_name)
            # '/Users/xxx/Downloads/weibo/screen_name'
            screen_name_path = os.path.join(self.rootPath, screen_name)
            # '/Users/xx/Downloads/weibo/screen_name/img/原创微博图片'
            path = os.path.join(screen_name_path, folder_name)

            if not os.path.exists(path) and os.path.exists(_path):
                os.rename(_screen_name_path, screen_name_path)
                logger.info("更新文件夹成功：{} -> {}".format(_path, path))
            elif not os.path.exists(path):
                # 创建新文件夹
                os.makedirs(path)
                logger.info("文件夹创建成功：{}".format(path))
            # 更新数据
            self.update_weibo_user(uid=uid, screen_name=screen_name)

        filepath = os.path.join(path, filename)
        return path, filepath

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
        finished = self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=key)
        # 获取媒体异常标识
        error_404 = self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=key)
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


class Download(DownloadMiddleware):

    @staticmethod
    def __get_file_size(url, filepath) -> tuple:
        """
        获取文件大小
        :param url:
        :param filepath:
        :return:
        """
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise NotFound("404 Not Found")
        # 获取文件大小
        try:
            file_size = int(r.headers['content-length'])
        except Exception:
            raise NOTContentLengthError("url资源没有文件大小数据")
        # 如果文件存在获取文件大小，否在从 0 开始下载，
        first_byte = 0
        if os.path.exists(filepath):
            first_byte = os.path.getsize(filepath)
        # 判断是否已经下载完成
        if first_byte >= file_size:
            raise FinishedError("文件已经下载完毕")
        return first_byte, file_size

    @staticmethod
    @LoggerAOP(message="媒体下载链接：{}", index=["args[0].url"], level=logging.INFO, save=True)
    def __segmented_download(item: DownloadEntity, first_byte, file_size, bar=True):
        """
        分段下载
        :param item: dict{url=url, filepath=filepath}
        :param first_byte:
        :param file_size:
        :param bar:是否显示进度条
        :return:
        """
        # Range 加入请求头
        # 加 headers 参数
        header = {"Range": f"bytes={first_byte}-{file_size}"}
        pbar = None
        if bar:
            # 设置显示进度条
            pbar = tqdm(total=file_size, initial=0, unit='B', unit_scale=True, desc=item.filepath)
        with requests.get(item.url, headers=header, stream=True) as r:
            with open(item.filepath, 'ab') as fp:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        fp.write(chunk)
                        if bar:
                            pbar.update(1024)  # 更新进度条
        if bar:
            pbar.close()

    def __download(self, item: DownloadEntity):
        """
        下载
        :param item:
        :return:
        """
        redis_key = getRedisKey(uid=item.blog_id, url=item.url, filepath=item.filepath)
        redis_value = EntityToJson(item)
        try:
            first_byte, file_size = self.__get_file_size(url=item.url, filepath=item.filepath)
        except FinishedError:
            # 再次写入数据库 防止下载完成后没有及时写入数据库
            logger.warning("媒体文件已经下载，重新记录中：key -> {}".format(redis_key))
            self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=redis_key, value=redis_value)
            return
        except NotFound:
            logger.error("请求链接404错误：{}".format(item.url))
            self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=redis_key, value=redis_value)
            return
        except Exception as e:
            logger.error("请求错误：{}".format(e))
            return

        try:
            # 开启线程下载就没有详情精度条提示 只有完成精度条提示
            if self.thread:
                self.__segmented_download(item, first_byte, file_size, False)
            else:
                self.__segmented_download(item, first_byte, file_size, True)
        except requests.exceptions.SSLError as e:
            logger.error(e)
            self.__download(item)

        # 下载完成就写入数据库
        self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=redis_key, value=redis_value)
        self.redis_client.hset(name=constants.REDIS_SPIDER_USER_START, key=item.blog.id, value=get_time_now())

    def startDownload(self, download_list: List[DownloadEntity]):
        """
        开始下载
        :param download_list:
        :return:
        """
        if not download_list:
            return
        if self.thread:
            thread_pool(
                method=self.__download,
                data=download_list,
                thread_num=min(len(download_list), self.workers),
            )
        else:
            for _ in download_list:
                self.__download(item=_)
