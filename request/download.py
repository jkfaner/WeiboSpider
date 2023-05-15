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

import utils.constants as constants
from entity.downloadEntity import DownloadEntity
from middleware.downloadMiddleware import DownloadMiddleware
from utils.exception import NOTContentLengthError, FinishedError, NotFound
from utils.logger import logger
from utils.tool import getRedisKey, thread_pool, EntityToJson


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
    def __segmented_download(item: DownloadEntity, first_byte, file_size, bar=True):
        """
        分段下载
        :param item: dict{url=url, filepath=filepath}
        :param first_byte:
        :param file_size:
        :param bar:是否显示进度条
        :return:
        """
        logger.info("下载链接：{}".format(item.url))
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
        redis_key = getRedisKey(blog_id=item.blog_id, url=item.url, filepath=item.filepath)
        redis_value = EntityToJson(item)
        try:
            first_byte, file_size = self.__get_file_size(url=item.url, filepath=item.filepath)
        except FinishedError:
            # 再次写入数据库 防止下载完成后没有及时写入数据库
            logger.warning("已经下载完成，但是上次没有写入redis，本次写入：key:{}".format(redis_key))
            self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=redis_key, value=redis_value)
            return
        except NotFound:
            logger.error("请求链接404错误：{}".format(item.url))
            self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=redis_key, value=redis_value)
            return
        except Exception as e:
            logger.error("请求错误：{}".format(e))
            return

        # 开启线程下载就没有详情精度条提示 只有完成精度条提示
        if self.thread:
            self.__segmented_download(item, first_byte, file_size, False)
        else:
            self.__segmented_download(item, first_byte, file_size, True)

        # 下载完成就写入数据库
        self.redis_client.hset(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=redis_key, value=redis_value)

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
