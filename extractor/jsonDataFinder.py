#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 18:59
@Project:WeiboSpider
@File:jsonDataFinder.py
@Desc:json数据查找
"""
from copy import deepcopy

from extractor.jsonPathFinder import JsonPathFinder


class JsonDataFinder(JsonPathFinder):

    def find_first_data(self, target: str):
        """
        获得第一条数据
        :param target:
        :return:
        """
        target_path = self.find_first(target)
        return self.join_path(target_path)

    def find_last_data(self, target: str):
        """
        获得第一条数据
        :param target:
        :return:
        """
        target_path = self.find_last(target)
        return self.join_path(target_path)

    def find_assign_data(self, target: str, index: int):
        """
        获取指定索引的数据
        :param target:
        :param index:
        :return:
        """
        target_path = self.find_first(target)
        target_path.append(index)
        return self.join_path(target_path)

    def find_all_data(self, target: str):
        """
        获得所有数据
        :param target:
        :return:
        """
        target_path = self.find_all(target)
        return self.join_path(target_path)

    def find_all_last_data(self, target: str):
        """
        提取target下 的父级target值 或叫做 所有单个列表中最后一个target值
        :param target:
        :return:
        """
        target_path = self.find_all(target)
        _target_path = [i for i in target_path if len(i) == 2]
        return self.join_path(_target_path)

    def find_all_same_level_data(self, target: str):
        """
        获得所有同级数据
        :param target:
        :return:
        """
        target_path = self.find_all(target)
        new_target_path = [path[:-1] for path in target_path]
        return self.join_path(new_target_path)

    def split_all_data(self, target: str):
        """
        分离所有target数据
            删除某key-value键值对
        :param target:
        :return:
        """
        data = deepcopy(self.data)
        for path in self.find_all(target=target):
            self.del_data(path, data)
        return data
