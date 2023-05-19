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
import os
from typing import List

import requests
from tqdm import tqdm

from cache import Cache
from entity.media import Media
from utils.exception import NOTContentLengthError, FinishedError, NotFound
from utils.logger import logger
from utils.tool import getRedisKey, get_time_now
from utils.tool import thread_pool


class Download(Cache):

    @staticmethod
    def _get_file_size(url, filepath) -> tuple:
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
    # @LoggerAOP(message="媒体下载链接：{}", index=["args[0].url"], level=logging.INFO, save=True)
    def _segmented_download(item: Media, first_byte, file_size, bar=True):
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

    def _download(self, media: Media):
        """
        下载
        :param media:
        :return:
        """
        # 开始记录
        p = self.get_blog_progress(media.blog_id)
        p.download_time = get_time_now()
        p.download_num = 1 if p.download_num is None else p.download_num+1
        p.blog_id = media.blog_id

        redis_key = getRedisKey(uid=media.blog_id, url=media.url, filepath=media.filepath)
        media_json = media.to_json()
        try:
            first_byte, file_size = self._get_file_size(url=media.url, filepath=media.filepath)
        except FinishedError:
            # 再次写入数据库 防止下载完成后没有及时写入数据库
            logger.warning("媒体文件已经下载，重新记录中：key -> {}".format(redis_key))
            self.record_finished(key=redis_key, value=media_json)
            p.downloaded_time = get_time_now()
            return
        except NotFound:
            logger.error("请求链接404错误：{}".format(media.url))
            self.record_error(key=redis_key, value=media_json)
            p.download_error_num = 1 if p.download_error_num is None else p.download_error_num+1
            return
        except Exception as e:
            logger.error("请求错误：{}".format(e))
            return

        try:
            # 开启线程下载就没有详情精度条提示 只有完成精度条提示
            if self.thread:
                self._segmented_download(media, first_byte, file_size, False)
            else:
                self._segmented_download(media, first_byte, file_size, True)
        except requests.exceptions.SSLError as e:
            logger.error(e)
            self._download(media)

        # 下载完成就写入数据库
        self.record_blog_progress(p)
        self.record_finished(key=redis_key, value=media_json)
        # self.record_spider_time(uid=media.blog.id)

    def startDownload(self, medias: List[Media]):
        """
        开始下载
        :param medias:
        :return:
        """
        if not medias:
            return

        if self.thread:
            thread_pool(method=self._download, data=medias, thread_num=min(len(medias), self.workers))
        else:
            for media in medias:
                self._download(media=media)
