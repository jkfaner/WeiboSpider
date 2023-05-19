#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/02/10 16:31:52
@Project:WeiboSpider
@File:user.py
@Desc:
'''
from entity.base import BaseEntity


class User(BaseEntity):

    def __init__(self):
        self._id = None
        self._idstr = None
        self._pc_new = None
        self._screen_name = None
        self._profile_image_url = None
        self._profile_url = None
        self._verified = None
        self._verified_type = None
        self._domain = None
        self._weihao = None
        self._verified_type_ext = None
        self._avatar_large = None
        self._avatar_hd = None
        self._follow_me = None
        self._following = None
        self._mbrank = None
        self._mbtype = None
        self._planet_video = None
        self._verified_reason = None
        self._description = None
        self._location = None
        self._gender = None
        self._followers_count = None
        self._followers_count_str = None
        self._friends_count = None
        self._statuses_count = None
        self._url = None
        self._cover_image_phone = None
        self._icon_list = None
        self._content1 = None
        self._content2 = None
        self._itemid = None
        self._special_follow = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def idstr(self):
        return self._idstr

    @idstr.setter
    def idstr(self, idstr):
        self._idstr = idstr

    @property
    def pc_new(self):
        return self._pc_new

    @pc_new.setter
    def pc_new(self, pc_new):
        self._pc_new = pc_new

    @property
    def screen_name(self):
        return self._screen_name

    @screen_name.setter
    def screen_name(self, screen_name):
        self._screen_name = screen_name

    @property
    def profile_image_url(self):
        return self._profile_image_url

    @profile_image_url.setter
    def profile_image_url(self, profile_image_url):
        self._profile_image_url = profile_image_url

    @property
    def profile_url(self):
        return self._profile_url

    @profile_url.setter
    def profile_url(self, profile_url):
        self._profile_url = profile_url

    @property
    def verified(self):
        return self._verified

    @verified.setter
    def verified(self, verified):
        self._verified = verified

    @property
    def verified_type(self):
        return self._verified_type

    @verified_type.setter
    def verified_type(self, verified_type):
        self._verified_type = verified_type

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        self._domain = domain

    @property
    def weihao(self):
        return self._weihao

    @weihao.setter
    def weihao(self, weihao):
        self._weihao = weihao

    @property
    def verified_type_ext(self):
        return self._verified_type_ext

    @verified_type_ext.setter
    def verified_type_ext(self, verified_type_ext):
        self._verified_type_ext = verified_type_ext

    @property
    def avatar_large(self):
        return self._avatar_large

    @avatar_large.setter
    def avatar_large(self, avatar_large):
        self._avatar_large = avatar_large

    @property
    def avatar_hd(self):
        return self._avatar_hd

    @avatar_hd.setter
    def avatar_hd(self, avatar_hd):
        self._avatar_hd = avatar_hd

    @property
    def follow_me(self):
        return self._follow_me

    @follow_me.setter
    def follow_me(self, follow_me):
        self._follow_me = follow_me

    @property
    def following(self):
        return self._following

    @following.setter
    def following(self, following):
        self._following = following

    @property
    def mbrank(self):
        return self._mbrank

    @mbrank.setter
    def mbrank(self, mbrank):
        self._mbrank = mbrank

    @property
    def mbtype(self):
        return self._mbtype

    @mbtype.setter
    def mbtype(self, mbtype):
        self._mbtype = mbtype

    @property
    def planet_video(self):
        return self._planet_video

    @planet_video.setter
    def planet_video(self, planet_video):
        self._planet_video = planet_video

    @property
    def verified_reason(self):
        return self._verified_reason

    @verified_reason.setter
    def verified_reason(self, verified_reason):
        self._verified_reason = verified_reason

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def followers_count(self):
        return self._followers_count

    @followers_count.setter
    def followers_count(self, followers_count):
        self._followers_count = followers_count

    @property
    def followers_count_str(self):
        return self._followers_count_str

    @followers_count_str.setter
    def followers_count_str(self, followers_count_str):
        self._followers_count_str = followers_count_str

    @property
    def friends_count(self):
        return self._friends_count

    @friends_count.setter
    def friends_count(self, friends_count):
        self._friends_count = friends_count

    @property
    def statuses_count(self):
        return self._statuses_count

    @statuses_count.setter
    def statuses_count(self, statuses_count):
        self._statuses_count = statuses_count

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def cover_image_phone(self):
        return self._cover_image_phone

    @cover_image_phone.setter
    def cover_image_phone(self, cover_image_phone):
        self._cover_image_phone = cover_image_phone

    @property
    def icon_list(self):
        return self._icon_list

    @icon_list.setter
    def icon_list(self, icon_list):
        self._icon_list = icon_list

    @property
    def content1(self):
        return self._content1

    @content1.setter
    def content1(self, content1):
        self._content1 = content1

    @property
    def content2(self):
        return self._content2

    @content2.setter
    def content2(self, content2):
        self._content2 = content2

    @property
    def itemid(self):
        return self._itemid

    @itemid.setter
    def itemid(self, itemid):
        self._itemid = itemid

    @property
    def special_follow(self):
        return self._special_follow

    @special_follow.setter
    def special_follow(self, special_follow):
        self._special_follow = special_follow

    def to_dict(self):
        obj_dict = self.__dict__
        cleaned_dict = {}
        for key, value in obj_dict.items():
            if key.startswith('_'):
                key = key[1:]
            cleaned_dict[key] = value
        return cleaned_dict

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
