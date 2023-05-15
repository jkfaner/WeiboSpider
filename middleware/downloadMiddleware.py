#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
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
from loader import ProjectLoader
from middleware.aop import FilterAOP
from utils.logger import logger
from utils.tool import getRedisKey, time_formatting
import utils.constants as constants


class DownloadLoader(object):
    _spider_config = ProjectLoader.getSpiderConfig()
    _database_config = ProjectLoader.getDatabaseConfig()
    _mysql_client = ProjectLoader.getMysqlClient()
    _redis_client = ProjectLoader.getRedisClient()

    def __init__(self):
        self.root_path = self._spider_config["download"]["root"]
        self.spider_sql_dict = self._database_config["mysql"]["sql"]["spider"]
        self.mysql_client = self._mysql_client
        self.redis_client = self._redis_client
        self.thread = self._spider_config["download"]["thread"]
        self.workers = self._spider_config["download"]["workers"]


class DownloadMiddleware(DownloadLoader):

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

    def select_weibo_user(self, uid: str):
        """
        查询数据库微博用户
        :param uid:
        :return:
        """
        sql = self.spider_sql_dict.get("select_weibo_user")
        result = self.mysql_client.getOne(sql=sql, param=[uid])
        return result

    def update_weibo_user(self, uid: str, screen_name: str):
        """
        插入数据&更新数据 数据库有数据就写入 没数据就跟行 weibo_id为唯一索引
        :param uid:
        :param screen_name:
        :return:
        """
        sql = self.spider_sql_dict.get("update_weibo_user")
        self.mysql_client.insert(sql=sql, param=[uid, screen_name, screen_name])
        self.mysql_client.end()

    def update_folder(self, uid: str, screen_name: str, folder_name: str, filename: str) -> tuple:
        """
        更新文件夹
        :param uid:
        :param filename:
        :param folder_name:
        :param screen_name:
        :return:
        """
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

        filepath = os.path.join(path, filename)
        return path, filepath

    def finish_download(self, blog_id, url, filepath):
        """
        是否已经下载
        包含下载完成的以及404错误
        # 注意：如果文件被删除且提示redis数库中已经存在 那么文件将继续下载！！！
        # 注意：图片下载地址为静态地址 视频下载地址为动态地址！存在重复写入同文件数据！！！
        :param blog_id:
        :param url:
        :param filepath:
        :return:
        """
        key = getRedisKey(blog_id=blog_id, url=url, filepath=filepath)
        # 检查文件是否存在 存在分为两种情况：完整数据文件 非完整数据文件（该类数据会继续下载）
        file_in_path = os.path.exists(filepath)
        finished = self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FINISH_NAME, key=key)
        error_404 = self.redis_client.hexists(name=constants.REDIS_DOWNLOAD_FAIL_NAME, key=key)
        if error_404:
            return True
        if not file_in_path:
            if finished:
                return True
            return False
        else:
            if finished:
                return True
        return False
