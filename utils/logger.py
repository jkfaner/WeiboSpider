#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project:
@File: logger.py
@Ide: PyCharm
@Time: 2021-05-08 13:52:11
@Desc:
"""
import logging
import os
import sys
from datetime import datetime
from typing import List


class Logger:
    default_log_fmt = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
    default_log_datetime_format = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
    default_log_path = 'log'

    def __init__(self, message: str = "", index: int or List = -1, level: logging = logging.INFO, save: bool = False):
        """
        构造方法
        :param message: 输出信息
        :param index: 参数索引
        :param level: 日志等级
        :param save: 是否储存
        """
        self.message = message
        self.format_index = index
        self.level = level
        self._logger = logging.getLogger()
        if not self._logger.handlers:
            self.formatter = logging.Formatter(fmt=self.default_log_fmt, datefmt=self.default_log_datetime_format)
            # 设置终端日志模式
            self._logger.addHandler(self._get_console_handler())
            if save:
                if not os.path.exists(self.default_log_path):
                    os.makedirs(self.default_log_path)
                # 设置文件日志模式
                self._logger.addHandler(self._get_file_handler(self._get_filepath()))
            # 设置日志等级
            self._logger.setLevel(level)

    def _get_filepath(self):
        now = datetime.now().strftime(self.default_log_datetime_format)
        return os.path.join(self.default_log_path, f'log_{now}.log')  # 默认日志文件名称

    def _get_file_handler(self, filename):
        """返回一个文件日志handler"""
        file_handler = logging.FileHandler(filename=filename, encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        return file_handler

    def _get_console_handler(self):
        """返回一个输出到终端日志handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    @property
    def logger(self):
        return self._logger


logger = Logger(level=logging.INFO, save=True).logger
