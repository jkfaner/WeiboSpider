#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 18:58
@Project:WeiboSpider
@File:extractor.py
@Desc:json提取器
"""
import json
from typing import List
from copy import deepcopy

class JsonPathFinder:
    """json数据路径查找"""

    def __init__(self, json_str, mode='key'):
        if isinstance(json_str, dict) or isinstance(json_str, list):
            self.data = json_str
        elif isinstance(json_str, str):
            self.data = json.loads(json_str)
        else:
            raise Exception(f"数据类型错误, The type is {type(json_str)}")
        self.mode = mode

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if self.mode == 'key':
                check = key
            else:
                check = value
            if check == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    def join_path(self, target_path):
        """
        通过路径查找数据
        :param target_path:
        :return:
        """
        if not target_path:
            return []
        if isinstance(target_path[0], list):
            new_data = list()
            for targets in target_path:
                data = self.data
                for target in targets:
                    data = data[target]
                new_data.append(data)
            if len(new_data) == 1:
                return new_data[0]
            return new_data

        data = self.data
        for target in target_path:
            data = data[target]
        return data

    def del_data(self, target_path: List[list], data):
        """
        通过路径删除数据
        :param target_path:
        :return:
        """
        if not target_path:
            return False
        if isinstance(target_path[0], list):
            for targets in target_path:
                for n, target in enumerate(targets):
                    if n + 1 == len(target_path):
                        del data[target]
                    else:
                        data = data[target]
        else:
            for n, target in enumerate(target_path):
                if n + 1 == len(target_path):
                    del data[target]
                else:
                    data = data[target]

    def find_first(self, target: str) -> list:
        """
        获取第一个路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        for path in path_iter:
            return path
        return []

    def find_last(self, target: str) -> list:
        """
        获取最后一个路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        if path_iter:
            new_path_iter = list(path_iter)
            if new_path_iter:
                return new_path_iter[-1]
        return []

    def find_all(self, target) -> List[list]:
        """
        获取所有路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        return list(path_iter)


class JsonDataFinder(JsonPathFinder):
    """json数据提取器"""

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


class ExtractorApi(object):
    """数据提取器接口"""

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