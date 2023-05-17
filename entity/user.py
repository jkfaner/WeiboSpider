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

class User(object):

	def __init__(self):
		self.__id = None
		self.__idstr = None
		self.__pc_new = None
		self.__screen_name = None
		self.__profile_image_url = None
		self.__profile_url = None
		self.__verified = None
		self.__verified_type = None
		self.__domain = None
		self.__weihao = None
		self.__verified_type_ext = None
		self.__avatar_large = None
		self.__avatar_hd = None
		self.__follow_me = None
		self.__following = None
		self.__mbrank = None
		self.__mbtype = None
		self.__planet_video = None
		self.__verified_reason = None
		self.__description = None
		self.__location = None
		self.__gender = None
		self.__followers_count = None
		self.__followers_count_str = None
		self.__friends_count = None
		self.__statuses_count = None
		self.__url = None
		self.__cover_image_phone = None
		self.__icon_list = None
		self.__content1 = None
		self.__content2 = None
		self.__itemid = None
		self.__special_follow = None

	@property
	def id(self):
		return self.__id

	@id.setter
	def id(self, id):
		self.__id = id

	@property
	def idstr(self):
		return self.__idstr

	@idstr.setter
	def idstr(self, idstr):
		self.__idstr = idstr

	@property
	def pc_new(self):
		return self.__pc_new

	@pc_new.setter
	def pc_new(self, pc_new):
		self.__pc_new = pc_new

	@property
	def screen_name(self):
		return self.__screen_name

	@screen_name.setter
	def screen_name(self, screen_name):
		self.__screen_name = screen_name

	@property
	def profile_image_url(self):
		return self.__profile_image_url

	@profile_image_url.setter
	def profile_image_url(self, profile_image_url):
		self.__profile_image_url = profile_image_url

	@property
	def profile_url(self):
		return self.__profile_url

	@profile_url.setter
	def profile_url(self, profile_url):
		self.__profile_url = profile_url

	@property
	def verified(self):
		return self.__verified

	@verified.setter
	def verified(self, verified):
		self.__verified = verified

	@property
	def verified_type(self):
		return self.__verified_type

	@verified_type.setter
	def verified_type(self, verified_type):
		self.__verified_type = verified_type

	@property
	def domain(self):
		return self.__domain

	@domain.setter
	def domain(self, domain):
		self.__domain = domain

	@property
	def weihao(self):
		return self.__weihao

	@weihao.setter
	def weihao(self, weihao):
		self.__weihao = weihao

	@property
	def verified_type_ext(self):
		return self.__verified_type_ext

	@verified_type_ext.setter
	def verified_type_ext(self, verified_type_ext):
		self.__verified_type_ext = verified_type_ext

	@property
	def avatar_large(self):
		return self.__avatar_large

	@avatar_large.setter
	def avatar_large(self, avatar_large):
		self.__avatar_large = avatar_large

	@property
	def avatar_hd(self):
		return self.__avatar_hd

	@avatar_hd.setter
	def avatar_hd(self, avatar_hd):
		self.__avatar_hd = avatar_hd

	@property
	def follow_me(self):
		return self.__follow_me

	@follow_me.setter
	def follow_me(self, follow_me):
		self.__follow_me = follow_me

	@property
	def following(self):
		return self.__following

	@following.setter
	def following(self, following):
		self.__following = following

	@property
	def mbrank(self):
		return self.__mbrank

	@mbrank.setter
	def mbrank(self, mbrank):
		self.__mbrank = mbrank

	@property
	def mbtype(self):
		return self.__mbtype

	@mbtype.setter
	def mbtype(self, mbtype):
		self.__mbtype = mbtype

	@property
	def planet_video(self):
		return self.__planet_video

	@planet_video.setter
	def planet_video(self, planet_video):
		self.__planet_video = planet_video

	@property
	def verified_reason(self):
		return self.__verified_reason

	@verified_reason.setter
	def verified_reason(self, verified_reason):
		self.__verified_reason = verified_reason

	@property
	def description(self):
		return self.__description

	@description.setter
	def description(self, description):
		self.__description = description

	@property
	def location(self):
		return self.__location

	@location.setter
	def location(self, location):
		self.__location = location

	@property
	def gender(self):
		return self.__gender

	@gender.setter
	def gender(self, gender):
		self.__gender = gender

	@property
	def followers_count(self):
		return self.__followers_count

	@followers_count.setter
	def followers_count(self, followers_count):
		self.__followers_count = followers_count

	@property
	def followers_count_str(self):
		return self.__followers_count_str

	@followers_count_str.setter
	def followers_count_str(self, followers_count_str):
		self.__followers_count_str = followers_count_str

	@property
	def friends_count(self):
		return self.__friends_count

	@friends_count.setter
	def friends_count(self, friends_count):
		self.__friends_count = friends_count

	@property
	def statuses_count(self):
		return self.__statuses_count

	@statuses_count.setter
	def statuses_count(self, statuses_count):
		self.__statuses_count = statuses_count

	@property
	def url(self):
		return self.__url

	@url.setter
	def url(self, url):
		self.__url = url

	@property
	def cover_image_phone(self):
		return self.__cover_image_phone

	@cover_image_phone.setter
	def cover_image_phone(self, cover_image_phone):
		self.__cover_image_phone = cover_image_phone

	@property
	def icon_list(self):
		return self.__icon_list

	@icon_list.setter
	def icon_list(self, icon_list):
		self.__icon_list = icon_list

	@property
	def content1(self):
		return self.__content1

	@content1.setter
	def content1(self, content1):
		self.__content1 = content1

	@property
	def content2(self):
		return self.__content2

	@content2.setter
	def content2(self, content2):
		self.__content2 = content2

	@property
	def itemid(self):
		return self.__itemid

	@itemid.setter
	def itemid(self, itemid):
		self.__itemid = itemid

	@property
	def special_follow(self):
		return self.__special_follow

	@special_follow.setter
	def special_follow(self, special_follow):
		self.__special_follow = special_follow
