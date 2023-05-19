#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 19:02
@Project:WeiboSpider
@File:extractor_wb.py
@Desc:微博json数据解析
"""
from typing import List

import utils.constants as constants
from entity.blog import Blog
from entity.blogType import BlogType
from entity.media import Media
from entity.user import User
from entity.video import Video
from extractor.extractor import ExtractorApi
from utils.logger import logger
from utils.tool import get_file_suffix, time_formatting, set_attr


class ExtractorUserInfo(ExtractorApi):

    def extractor_userInfo(self, resp: dict) -> List[User]:
        """
        博文中的用户
        :param resp:
        :return:
        """
        users = list()
        if not resp:
            users.append(User())
            return users

        user = self.find_first_data(resp, 'user')
        user = user if user else self.find_first_data(resp, 'users')
        if isinstance(user, list):
            for _user in user:
                users.append(set_attr(source=_user, entity=User()))
        elif isinstance(user, dict):
            users.append(set_attr(source=user, entity=User()))
        else:
            users.append(User())

        return users


class ExtractorWeibo(ExtractorUserInfo):

    def extractor_weibo(self, resp: str) -> List[BlogType]:
        """
        提取微博的微博信息
        :param resp:
        :return:
        """
        statuses_blogs = [self.__clean_info(item) for item in self.find_first_data(resp=resp, target="statuses")]
        list_blogs = [self.__clean_info(item) for item in self.find_first_data(resp=resp, target="list")]
        statuses_blogs.extend(list_blogs)
        return statuses_blogs

    def __extractor_picture(self, item) -> tuple:
        """
        提取图片
        :param item:
        :return:
        """
        large_images = list()
        videos = list()
        # 图片 pic_ids
        # 图片 pic_infos
        pic_ids = self.find_first_data(item, "pic_ids")
        pic_infos = self.find_first_data(item, "pic_infos")
        for index, _id in enumerate(pic_ids, 1):
            try:
                pic = pic_infos.get(_id)
            except AttributeError:
                continue
            if not pic:
                continue
            # 图片尺寸大小：large>mw2000>orj1080>orj960>wap360>wap180
            # 对应的对象是：largest>mw2000>original>large>bmiddle>thumbnail
            # 优先下载large尺寸的图片
            if pic.get("largest"):
                pic["largest"].update(dict(index=index))
                large_images.append(pic["largest"])

            elif pic.get("mw2000"):
                pic["mw2000"].update(dict(index=index))
                large_images.append(pic["mw2000"])

            elif pic.get("original"):
                pic["original"].update(dict(index=index))
                large_images.append(pic["original"])

            elif pic.get("large"):
                pic["large"].update(dict(index=index))
                large_images.append(pic["large"])

            elif pic.get("bmiddle"):
                pic["bmiddle"].update(dict(index=index))
                large_images.append(pic["bmiddle"])

            elif pic.get("thumbnail"):
                pic["thumbnail"].update(dict(index=index))
                large_images.append(pic["thumbnail"])

            if pic.get("Video"):
                videos.append(dict(url=pic["Video"], index=index))

        return large_images, videos

    def __extractor_video(self, item: dict) -> List[Video]:
        """
        博文中的 page_info 即视频
        :param item:
        :return:
        """
        videos = list()
        play_info_list = self.find_all_data(item, "play_info")
        for play_info in play_info_list:
            video = Video()
            for key, v in video.__dict__.items():
                targ = key.split("__")[-1]
                setattr(video, targ, play_info.get(targ))
            videos.append(video)
        return videos

    def __extractor_info(self, item: dict, is_original: bool) -> Blog:
        """
        提取信息
        :param item:
        :return:
        """
        blog = Blog()
        # 检查是否是置顶 置顶数据在筛选过程中不中断
        is_top = self.find_first_data(resp=item, target="isTop")
        if is_top and isinstance(is_top, int) and is_top == 1:
            blog.is_top = True
        else:
            blog.is_top = False

        user_queue = self.extractor_userInfo(item)
        if len(user_queue) == 1:
            created_at = self.find_first_data(item, "created_at")
            images, live_photo = self.__extractor_picture(item=item)
            videos = self.__extractor_video(item=item)
            # 获取质量最佳的视频 即第一个
            videos = videos[0] if videos else videos

            blog.blog_id = item["id"]
            blog.id = user_queue[0].id
            blog.screen_name = user_queue[0].screen_name
            blog.created_at = created_at
            blog.livephoto_video = live_photo
            blog.images = images
            blog.videos = videos
            if is_original:
                blog.image_str = constants.DOWNLOAD_PATH_IMG_ORIGINAL_STR
                blog.video_str = constants.DOWNLOAD_PATH_VIDEO_ORIGINAL_STR
            else:
                blog.image_str = constants.DOWNLOAD_PATH_IMG_FORWARD_STR
                blog.video_str = constants.DOWNLOAD_PATH_VIDEO_FORWARD_STR
        else:
            logger.warning("微博数据无法提取数据，原因：{}".format(self.find_first_data(item, "text_raw")))
        return blog

    def __clean_info(self, item: dict) -> BlogType:
        """
        提取信息
        :param item:
        :return:
        """
        blogType = BlogType()
        # 点赞 快转 出现的按钮标签 followBtnCode
        # 快转了 screen_name_suffix_new
        if "followBtnCode" in item:
            return blogType

        screen_name_suffix_new = self.find_first_data(item, "screen_name_suffix_new")
        if screen_name_suffix_new:
            if "快转了" in str(screen_name_suffix_new):
                return blogType

        promotion = self.find_first_data(item, "promotion")
        if promotion:
            if "广告" in str(promotion):
                return blogType

        if item.get("title"):
            # 很多很多 包括赞过的 评论过的。。。
            # if "赞过的微博" in media["title"].get("text"):
            #     return weiboTypeEntity
            if item["title"].get("text"):
                return blogType

        # 原创与转发分离
        # page_info包含视频内容
        # 如果是转发 即有retweeted_status对象 则page_info应该属于retweeted_status对象中
        # 如果是原创 即retweeted_status对象为空（或不存在）则的page_info应该属于weiboObj对象中
        retweeted_item = self.find_first_data(item, "retweeted_status")
        if "retweeted_status" in item:
            del item['retweeted_status']

        original_blog = self.__extractor_info(item=item, is_original=True)
        blogType.original = original_blog

        if retweeted_item:
            forward_weiboEntity = self.__extractor_info(item=retweeted_item, is_original=False)
            blogType.forward = forward_weiboEntity

        return blogType

    @staticmethod
    def extractor_media(blogs: List[Blog]) -> List[Media]:
        new_blogs = list()
        for blog in blogs:
            base_filename = "{}_{}".format(time_formatting(blog.created_at), blog.blog_id)
            # 视频
            if blog.videos:
                filename = "{}.mp4".format(base_filename)

                video_media = Media()
                video_media.blog = blog
                video_media.blog_id = blog.blog_id
                video_media.filename = filename
                video_media.folder_name = blog.video_str
                video_media.url = blog.videos.url
                new_blogs.append(video_media)
            # 图片
            for image in blog.images:
                suffix = get_file_suffix(image["url"])
                filename = "{}_{}.{}".format(base_filename, image['index'], suffix)

                image_media = Media()
                image_media.blog = blog
                image_media.blog_id = blog.blog_id
                image_media.filename = filename
                image_media.folder_name = blog.image_str
                image_media.url = image['url']
                new_blogs.append(image_media)

            # livephoto
            for livephoto in blog.livephoto_video:
                suffix = get_file_suffix(livephoto["url"])
                filename = "{}_{}.{}".format(base_filename, livephoto['index'], suffix)

                live_midia = Media()
                live_midia.blog = blog
                live_midia.blog_id = blog.blog_id
                live_midia.filename = filename
                live_midia.folder_name = blog.video_str
                live_midia.url = livephoto['url']
                new_blogs.append(live_midia)
        return new_blogs
