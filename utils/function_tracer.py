#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: weibo-crawler
@File: function_tracer.py
@Ide: PyCharm
@Time: 2021-11-13 19:47:27
@Desc:
"""
import functools

from utils.logger import logger


class Tracer:

    def tracer(func):
        """
        方法次数跟踪装饰器
        :return:
        """
        tracer_item = dict()

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            func_name = str(func.__name__)
            if func_name not in tracer_item:
                tracer_item[func_name] = 0 if func_name == "login" else dict()
            # 调用login方法限制器
            if func_name == "login":
                tracer_item[func_name] += 1
                # logger.info(f'调用login方法限制器: [{tracer_item[func_name]}次]')
                kwargs.update(tracer_item)
                return func(self, *args, **kwargs)
            return func(self, *args, **kwargs)

        return new_func

    def log(func):
        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            logger.info("Request URL：{}".format(args[0]))
            return func(self, *args, **kwargs)

        return new_func
