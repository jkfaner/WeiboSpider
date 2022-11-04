#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 19:02
@Project:WeiboSpider
@File:weiboJsonExtractor.py
@Desc:微博json数据解析
"""
from typing import List

from entity.playInfoEntity import PlayInfoEntity
from entity.userEntity import UserEntity
from entity.weiboEntity import WeiboEntity
from entity.weiboTypeEntity import WeiboTypeEntity
from extractor.jsonExtractorAPI import ExtractorApi
import utils.businessConstants as constants
from utils.logger import logger
from utils.queue import Queue


class ExtractorUserInfo(ExtractorApi):

    def __extractor_userInfo(self, user: dict or list) -> UserEntity:
        """
        获取博主信息
        :param user:
        :return:
        """
        userEntityObj = UserEntity()
        for k, v in userEntityObj.__dict__.items():
            targ = k.split("__")[-1]
            setattr(userEntityObj, targ, user.get(targ))
        return userEntityObj

    def extractor_userInfo(self, resp: dict) -> List[UserEntity]:
        """
        博文中的用户
        :param resp:
        :return:
        """
        queue = Queue()
        if not resp:
            # 提高效率 无数据 直接返回
            queue.enqueue(UserEntity())
            return queue.get_all()
        user = self.find_first_data(resp, 'user')
        user = user if user else self.find_first_data(resp, 'users')
        if isinstance(user, list):
            for __user in user:
                queue.enqueue(self.__extractor_userInfo(__user))
        elif isinstance(user, dict):
            queue.enqueue(self.__extractor_userInfo(user))
        return queue.get_all()


class ExtractorWeibo(ExtractorUserInfo):

    def extractor_weibo(self, resp: str) -> List[WeiboTypeEntity]:
        """
        提取微博的微博信息
        :param resp:
        :return:
        """
        queue = Queue()
        statuses = self.find_first_data(resp=resp, target="statuses")
        for item in statuses:
            queue.enqueue(self.__clean_info(item))
        lists = self.find_first_data(resp=resp, target="list")
        for item in lists:
            queue.enqueue(self.__clean_info(item))
        return queue.get_all()

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
        for index, id in enumerate(pic_ids, 1):
            pic = pic_infos.get(id)
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

            if pic.get("video"):
                videos.append(dict(url=pic["video"], index=index))

        return large_images, videos

    def __extractor_video(self, item: dict) -> List[PlayInfoEntity]:
        """
        博文中的 page_info 即视频
        :param item:
        :return:
        """
        videos = list()
        play_info_list = self.find_all_data(item, "play_info")
        for play_info in play_info_list:
            playInfoObj = PlayInfoEntity()
            for key, v in playInfoObj.__dict__.items():
                targ = key.split("__")[-1]
                setattr(playInfoObj, targ, play_info.get(targ))
            videos.append(playInfoObj)

        return videos

    def __extractor_info(self, item: dict, is_original: bool) -> WeiboEntity:
        """
        提取信息
        :param item:
        :return:
        """
        weiboEntity = WeiboEntity()
        # 检查是否是置顶 置顶数据在筛选过程中不中断
        is_top = self.find_first_data(resp=item, target="isTop")
        if is_top and isinstance(is_top, int) and is_top == 1:
            weiboEntity.is_top = True
        else:
            weiboEntity.is_top = False

        user_queue = self.extractor_userInfo(item)
        if len(user_queue) == 1:
            created_at = self.find_first_data(item, "created_at")
            images, livephoto_video = self.__extractor_picture(item=item)
            videos = self.__extractor_video(item=item)
            # 获取质量最佳的视频 即第一个
            videos = videos[0] if videos else videos

            weiboEntity.blog_id = item["id"]
            weiboEntity.id = user_queue[0].id
            weiboEntity.screen_name = user_queue[0].screen_name
            weiboEntity.created_at = created_at
            weiboEntity.livephoto_video = livephoto_video
            weiboEntity.images = images
            weiboEntity.videos = videos
            if is_original:
                weiboEntity.image_str = constants.DOWNLOAD_PATH_IMG_ORIGINAL_STR
                weiboEntity.video_str = constants.DOWNLOAD_PATH_VIDEO_ORIGINAL_STR
            else:
                weiboEntity.image_str = constants.DOWNLOAD_PATH_IMG_FORWARD_STR
                weiboEntity.video_str = constants.DOWNLOAD_PATH_VIDEO_FORWARD_STR
        else:
            logger.warning("微博数据无法提取数据，原因：{}".format(self.find_first_data(item, "text_raw")))
        return weiboEntity

    def __clean_info(self, item: dict) -> WeiboTypeEntity:
        """
        提取信息
        :param item:
        :return:
        """
        weiboTypeEntity = WeiboTypeEntity()
        # 点赞 快转 出现的按钮标签 followBtnCode
        # 快转了 screen_name_suffix_new
        if "followBtnCode" in item:
            return weiboTypeEntity

        screen_name_suffix_new = self.find_first_data(item, "screen_name_suffix_new")
        if screen_name_suffix_new:
            if "快转了" in str(screen_name_suffix_new):
                return weiboTypeEntity

        promotion = self.find_first_data(item, "promotion")
        if promotion:
            if "广告" in str(promotion):
                return weiboTypeEntity

        if item.get("title"):
            if "赞过的微博" in item["title"].get("text"):
                return weiboTypeEntity

        # 原创与转发分离
        # page_info包含视频内容
        # 如果是转发 即有retweeted_status对象 则page_info应该属于retweeted_status对象中
        # 如果是原创 即retweeted_status对象为空（或不存在）则的page_info应该属于weiboObj对象中
        retweeted_item = self.find_first_data(item, "retweeted_status")
        if "retweeted_status" in item:
            del item['retweeted_status']

        original_weiboEntity = self.__extractor_info(item=item, is_original=True)
        weiboTypeEntity.original = original_weiboEntity

        if retweeted_item:
            forward_weiboEntity = self.__extractor_info(item=retweeted_item, is_original=False)
            weiboTypeEntity.forward = forward_weiboEntity

        return weiboTypeEntity
