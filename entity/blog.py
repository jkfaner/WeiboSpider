#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/02/10 14:12:42
@Project:WeiboSpider
@File:blog.py
@Desc:
'''
import json

from entity.base import BaseEntity

class Blog(BaseEntity):

    def __init__(self):
        self._is_top = None
        self._created_at = None
        self._images = None
        self._livephoto_video = None
        self._videos = None
        self._screen_name = None
        self._id = None
        self._blog_id = None
        self._image_str = None
        self._video_str = None

    @property
    def is_top(self):
        return self._is_top

    @is_top.setter
    def is_top(self, is_top):
        self._is_top = is_top

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def image_str(self):
        return self._image_str

    @image_str.setter
    def image_str(self, image_str):
        self._image_str = image_str

    @property
    def video_str(self):
        return self._video_str

    @video_str.setter
    def video_str(self, video_str):
        self._video_str = video_str

    @property
    def blog_id(self):
        return self._blog_id

    @blog_id.setter
    def blog_id(self, blog_id):
        self._blog_id = blog_id

    @property
    def livephoto_video(self):
        return self._livephoto_video

    @livephoto_video.setter
    def livephoto_video(self, livephoto_video):
        self._livephoto_video = livephoto_video

    @property
    def videos(self):
        return self._videos

    @videos.setter
    def videos(self, videos):
        self._videos = videos

    @property
    def screen_name(self):
        return self._screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        self._screen_name = screen_name

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images
    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    def to_dict(self):
        obj_dict = self.__dict__
        cleaned_dict = {}
        for key, value in obj_dict.items():
            if key.startswith('_'):
                key = key[1:]
            cleaned_dict[key] = value
        return cleaned_dict

    def to_json(self):
        return json.dumps(self.to_dict(),ensure_ascii=False)