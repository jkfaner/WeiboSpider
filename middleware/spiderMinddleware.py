#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 17:08
@Project:WeiboSpiderStation
@File:spiderMinddleware.py
@Desc:爬虫中间件
"""
from typing import List, Tuple

import utils.businessConstants as constants
from entity.spiderConfigEntity import SpiderCrawlItemConfig
from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from entity.weiboTypeEntity import WeiboTypeEntity
from extractor.weiboJsonExtractor import ExtractorWeibo
from init import spider_config
from utils.exception import ParameterError, DateError
from utils.logger import logger
from utils.tool import match_date, EntityToJson, time_formatting


class ParseUser(object):
    """解析用户"""
    extractorWeibo = ExtractorWeibo()

    def extractor_user(self, response) -> List[UserEntity]:
        """
        提取用户
        :param response: json str or dict
        :return:
        """
        users = self.extractorWeibo.extractor_userInfo(resp=response)
        for index, user in enumerate(users, 1):
            logger.info(f"[{index}/{len(users)}]提取用户:{user.idstr}->{user.screen_name}")
        return users

    def filter_user(self, users: List[UserEntity]) -> List[Tuple[UserEntity, SpiderCrawlItemConfig]]:
        """
        筛选用户
        :param response:
        :return:
        """

        new_users = list()
        s = SpiderCrawlItemConfig()
        for index, user in enumerate(users):
            # 开启只爬开关
            if spider_config.onlyCrawl_switch:

                if spider_config.onlyCrawl_item:
                    for user_crawl in spider_config.onlyCrawl_item:

                        if user.screen_name == user_crawl.screen_name:
                            new_users.append((user, user_crawl))
                        if user.idstr == user_crawl.uid:
                            new_users.append((user, user_crawl))
            # 开启排除开关
            if spider_config.excludeCrawl_switch:

                if spider_config.excludeCrawl_item:
                    for user_crawl in spider_config.excludeCrawl_item:

                        if user.screen_name in user_crawl.screen_name:
                            if user in new_users:
                                logger.info(f"[{index}/{len(users)}]删除用户:{user.idstr}->{user.screen_name}")
                                new_users.remove((user, user_crawl))
                        if user.idstr in user_crawl.uid:
                            if user in new_users:
                                logger.info(f"[{index}/{len(users)}]删除用户:{user.idstr}->{user.screen_name}")
                                new_users.remove((user, user_crawl))
            # 关闭只爬和排除开关
            if not spider_config.onlyCrawl_switch and not spider_config.excludeCrawl_switch:
                new_users.append((user, s))

        new_users = list(set(new_users))
        for index, (new_user, user_crawl) in enumerate(new_users, 1):
            logger.info(f"[{index}/{len(users)}]筛选用户:{new_user.idstr}->{new_user.screen_name}")

        return new_users


class FilterBlog(ParseUser):
    """解析微博"""

    def extractor_blog(self, response, user: UserEntity) -> List[WeiboTypeEntity]:
        """
        提取博客
        :param response:
        :return:
        """
        blogs = self.extractorWeibo.extractor_weibo(resp=response)
        logger.info(f"[{len(blogs)}]提取博客:{user.idstr}->{user.screen_name}")
        return blogs

    def filter_blogByFilter(self, blogs: List[WeiboTypeEntity], user: UserEntity, user_crawl:SpiderCrawlItemConfig) -> List[WeiboEntity]:
        """
        通过筛选条件筛选博客
        原创 or 转发 or 原创+转发
        :param blogs:
        :param user:
        :param user_crawl:
        :return:
        """
        new_blogs = list()
        for blog in blogs:
            # 筛选爬取规则
            if user_crawl.filter == constants.BLOG_FILTER_ORIGINAL:
                # 获取原创
                if blog.original:
                    new_blogs.append(blog.original)
            elif user_crawl.filter == constants.BLOG_FILTER_FORWARD:
                # 获取转发
                if blog.forward:
                    new_blogs.append(blog.forward)
            elif user_crawl.filter == constants.BLOG_FILTER_ALL:
                # 原创+转发
                if blog.original:
                    new_blogs.append(blog.original)
                if blog.forward:
                    new_blogs.append(blog.forward)
            else:
                raise ParameterError("筛选爬取规则参数错误")
        len_blogs = len(new_blogs)
        for index, new_blog in enumerate(new_blogs):
            msg1 = "[{index}/{len_blogs}]".format(index=index,len_blogs=len_blogs)
            msg2 = "[原创|转发|所有]"
            msg3 = f"筛选博客:{user.idstr}->{user.screen_name} ->> {new_blog.blog_id}"
            logger.info(msg1+msg2+msg3)
        return new_blogs

    def filter_blogByDate(self, blogs: List[WeiboEntity], user: UserEntity,user_crawl:SpiderCrawlItemConfig) -> List[WeiboEntity]:
        """
        通过设置的日期筛选博客
        :param blogs:
        :param user:
        :return:
        """
        new_blogs = list()
        for blog in blogs:
            # 筛选爬取时间
            if not blog.is_top and not match_date(create_time=blog.created_at, filter_date=user_crawl.date):
                # 不符合时间&不是置顶数据 抛出异常 捕获异常后需要中断爬取
                create_time = time_formatting(blog.created_at, usefilename=False, strftime=True)
                logger.warning(f"[{user_crawl.date}]筛选的博客不在配置的下载时间之后:{create_time}")
                raise DateError("筛选的博客不在配置的下载时间内", new_blogs)
            else:
                new_blogs.append(blog)

        len_blogs = len(new_blogs)
        for index, new_blog in enumerate(new_blogs, 1):
            user_msg = f"{user.idstr}->{user.screen_name}"
            blog_msg = f"{new_blog.blog_id}->{time_formatting(created_at=new_blog.created_at, usefilename=False, strftime=True)}"
            msg = f"[{index}/{len_blogs}]通过日期[{user_crawl.date}]筛选博客:{user_msg} -->> {blog_msg}"
            logger.info(msg)

        return new_blogs


class SpiderMinddleware(FilterBlog):

    def __init__(self):
        logger.info(f"\n爬虫中间件：\t{EntityToJson(spider_config)}")

    def parse_user(self, response) -> List[Tuple[UserEntity, SpiderCrawlItemConfig]]:
        """
        解析用户（提取+筛选）
        :param response:
        :return:
        """
        return self.filter_user(self.extractor_user(response))

    def filter_blog(self, response, user: UserEntity, user_crawl: SpiderCrawlItemConfig):
        """
        筛选博客
        :param response:
        :param user:
        :return:
        """
        blogs = self.extractor_blog(response=response, user=user)
        blogs = self.filter_blogByFilter(blogs=blogs, user=user, user_crawl=user_crawl)
        return self.filter_blogByDate(blogs=blogs, user=user,user_crawl=user_crawl)
