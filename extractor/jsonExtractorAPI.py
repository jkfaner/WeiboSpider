#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 19:01
@Project:WeiboSpider
@File:jsonExtractorAPI.py
@Desc:json数据解析接口
"""
from extractor.jsonDataFinder import JsonDataFinder


class ExtractorApi(object):
    """
    数据提取器接口
    """

    def finder(self, resp):
        finder = JsonDataFinder(resp)
        return finder

    def find_exists(self, resp, target: str) -> bool:
        """
        检查是否存在
        :return:
        """
        finder = self.finder(resp)
        exists = finder.find_first(target)
        if exists:
            return True
        return False

    def find_all_data(self, resp, target: str):
        """
        提取target下所有数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        if not target_list:
            return []
        if not isinstance(target_list, list):
            target_list = [target_list]
        return target_list

    def find_all_last_data(self, resp, target: str):
        """
        提取target下 的父级target值 或叫做 所有单个列表中最后一个target值
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_last_data(target)
        return target_list

    def find_first_data(self, resp, target: str):
        """
        提取target下第一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_first_data(target)
        return first_target

    def find_last_data(self, resp, target: str):
        """
        提取target下第最后一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_last_data(target)
        return first_target

    def find_assign_data(self, resp, target: str, index: int):
        """
        提取target下第index个数据
        :param resp:
        :param target:
        :param index:
        :return:
        """
        finder = self.finder(resp)
        assign_target = finder.find_assign_data(target, index)
        return assign_target

    def find_all_same_level_data(self, resp, target: str):
        finder = self.finder(resp)
        target_list = finder.find_all_same_level_data(target)
        return target_list

    def find_effective_data(self, resp, target: str):
        """
        获取有效数据
        推特有效数据默认排除最后两个
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        return target_list[:-2]

    def split_all_data(self, resp, target: str):
        """
        分离所有target数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        return finder.split_all_data(target)
