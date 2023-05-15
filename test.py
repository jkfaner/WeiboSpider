#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2023/5/15 16:21
@Project:WeiboSpider
@File:test.py
@Desc:
"""
import sys
from typing import List


def format_str(message: str, index: int or List):
    dict_count = message.count("{}")
    index_len = index
    if isinstance(index, list):
        index_len = len(index)
    if dict_count != index_len:
        sys.exit("!!!")
    return message.format(*index)


if __name__ == '__main__':
    format_str("{} + {} = {}", [1, 1, 4])
