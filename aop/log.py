#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/18 17:18
@Project:WeiboSpider
@File:log.py
@Desc:
"""
import logging
import sys
from typing import List

from utils.logger import Logger


class LoggerAOP(Logger):

    @staticmethod
    def format_str(message: str, index: int or List, *args, **kwargs):
        dict_count = message.count("{}")
        index_len = index
        if isinstance(index, list):
            index_len = len(index)
        if dict_count != index_len and index == -1:
            sys.exit("ERROR: LoggerAOP.format_str")
        if isinstance(index, int):
            return message.format(args[index])
        format_list = list()
        if isinstance(index, list):
            for i in index:
                format_list.append(eval(i))
        return message.format(*format_list)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            message = self.message
            if "{}" in message:
                message = self.format_str(message, self.format_index, *args, **kwargs)
            if self.level == logging.INFO:
                self.logger.info(message)
            elif self.level == logging.DEBUG:
                self.logger.debug(message)
            elif self.level == logging.WARNING:
                self.logger.warning(message)
            elif self.level == logging.ERROR:
                self.logger.error(message)
            elif self.level == logging.CRITICAL:
                self.logger.critical(message)
            else:
                raise "日志类型设置错误"
            return func(*args, **kwargs)

        return wrapper