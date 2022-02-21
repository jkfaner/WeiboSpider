#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/21 17:52
@Project:WeiboSpider
@File:downloadMiddleware.py
@Desc:下载中间件
"""
import os
from typing import List

from entity.downloadEntity import DownloadEntity
from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from init import redisPool, mysqlPool, download_config
from utils.logger import logger
from utils.tool import getRedisKey, time_formatting
import utils.businessConstants as constants


class DownloadMiddleware(object):

    def __init__(self):
        # 创建weibo专属路径
        self.rootPath = os.path.join(download_config.root, "weibo")
        if not os.path.exists(self.rootPath):
            os.makedirs(self.rootPath)

    def distribute_data(self, blogs: List[WeiboEntity], user: UserEntity) -> List[DownloadEntity]:
        """
        数据分发
        :param blogs:
        :param user:
        :return:
        """
        logger.info("[{}]博客数据分发中:{}".format(user.screen_name, len(blogs)))
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
                suffix = os.path.split(image['url'])[-1].split(".")[-1]
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
                suffix = os.path.split(livephoto['url'])[-1].split(".")[-1]
                filename = "{}_{}.{}".format(base_filename, livephoto['index'], suffix)

                livephoto_download_entity = DownloadEntity()
                livephoto_download_entity.blog = blog
                livephoto_download_entity.blog_id = blog.blog_id
                livephoto_download_entity.filename = filename
                livephoto_download_entity.folder_name = blog.video_str
                livephoto_download_entity.url = livephoto['url']
                new_blogs.append(livephoto_download_entity)

        return new_blogs

    @staticmethod
    def select_weibo_user(uid: str):
        """
        查询数据库微博用户
        :param uid:
        :return:
        """
        sql = "SELECT weibo_id,screen_name FROM weibo_user WHERE weibo_id=%s"
        result = mysqlPool.getOne(sql=sql, param=[uid])
        return result

    @staticmethod
    def update_weibo_user(uid: str, screen_name: str):
        """
        插入数据&更新数据 数据库有数据就写入 没数据就跟行 weibo_id为唯一索引
        :param uid:
        :param screen_name:
        :return:
        """
        sql = "INSERT INTO weibo_user (weibo_id,screen_name) VALUES (%s,%s)  ON DUPLICATE KEY UPDATE screen_name=%s"
        mysqlPool.insert(sql=sql, param=[uid, screen_name, screen_name])
        mysqlPool.end()

    def update_folder(self, download_data: DownloadEntity) -> tuple:
        """
        更新文件夹
        :param download_data:
        :return:
        """
        uid = download_data.blog.id
        screen_name = download_data.blog.screen_name
        folder_name = download_data.folder_name

        result = self.select_weibo_user(uid=uid)
        if not result:
            # 创建文件夹
            path = os.path.join(os.path.join(self.rootPath, screen_name), folder_name)
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info("文件夹创建成功：{}".format(path))
            self.update_weibo_user(uid=uid, screen_name=screen_name)
        else:
            # 数据库有数据
            # 修改本地文件夹
            _screen_name = str(result.get("screen_name"), encoding="utf-8")
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

        filepath = os.path.join(path, download_data.filename)
        return path, filepath

    @staticmethod
    def finish_download(blog_id, url, filepath):
        """
        是否已经下载
        包含下载完成的以及404错误
        :param id:
        :param url:
        :param filepath:
        :return:
        """
        key = getRedisKey(blog_id=blog_id, url=url, filepath=filepath)
        finished = redisPool.hexists(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=key)
        error_404 = redisPool.hexists(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=key)
        if finished or error_404:
            return True
        return False

    def filter_blogByDownloaded(self,download_datas:List[DownloadEntity]) -> List[DownloadEntity]:
        """
        通过已下载和404筛选
        :return:
        """
        new_download_datas = list()
        for download_data in download_datas:
            path,filepath = self.update_folder(download_data)
            # 是否已经下载 包含下载完成的以及404错误的
            if not self.finish_download(blog_id=download_data.blog_id, url=download_data.url, filepath=filepath):
                download_data.filepath = filepath
                new_download_datas.append(download_data)
        return new_download_datas

    def filter_download(self,blogs: List[WeiboEntity], user: UserEntity):
        """
        筛选下载数据
        :param blogs:
        :param user:
        :return:
        """
        download_datas = self.distribute_data(blogs=blogs,user=user)
        return self.filter_blogByDownloaded(download_datas=download_datas)
