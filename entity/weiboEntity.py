#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/02/10 14:12:42
@Project:WeiboSpider
@File:weiboEntity.py
@Desc:
'''


class WeiboEntity(object):

    def __init__(self):
        self.__is_top = None
        self.__created_at = None
        self.__images = None
        self.__livephoto_video = None
        self.__videos = None
        self.__screen_name = None
        self.__id = None
        self.__blog_id = None
        self.__image_str = None
        self.__video_str = None

    @property
    def is_top(self):
        return self.__is_top

    @is_top.setter
    def is_top(self, is_top):
        self.__is_top = is_top

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def image_str(self):
        return self.__image_str

    @image_str.setter
    def image_str(self, image_str):
        self.__image_str = image_str

    @property
    def video_str(self):
        return self.__video_str

    @video_str.setter
    def video_str(self, video_str):
        self.__video_str = video_str

    @property
    def blog_id(self):
        return self.__blog_id

    @blog_id.setter
    def blog_id(self, blog_id):
        self.__blog_id = blog_id

    @property
    def livephoto_video(self):
        return self.__livephoto_video

    @livephoto_video.setter
    def livephoto_video(self, livephoto_video):
        self.__livephoto_video = livephoto_video

    @property
    def videos(self):
        return self.__videos

    @videos.setter
    def videos(self, videos):
        self.__videos = videos

    @property
    def screen_name(self):
        return self.__screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        self.__screen_name = screen_name

    @property
    def images(self):
        return self.__images

    @images.setter
    def images(self, images):
        self.__images = images
    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at