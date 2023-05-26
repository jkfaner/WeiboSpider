#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/17 22:10
@Project:WeiboSpiderStation
@File:tool.py
@Desc:
"""
import datetime
import hashlib
import json
import os.path
import sys
from concurrent import futures
from typing import List
from urllib.parse import urlencode

from tqdm import tqdm

from entity.base import BaseEntity


def set_attr(source: dict, entity: BaseEntity):
    """
    entity对象赋值
    :param entity:
    :param source:
    :return:
    """
    for k, v in entity.to_dict().items():
        setattr(entity, k, source.get(k))
    return entity


def load_json(path: str) -> dict:
    filepath, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)
    if ext != ".json":
        sys.exit("{}:不是json文件类型".format(path))
    with open(path, 'r') as f:
        json_str = f.read()
    if not is_json(json_str):
        sys.exit("非法的json数据")
    return json.loads(json_str)


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def join_url(url: str, params: dict):
    """
    合并url
    :param url:url
    :param params:参数
    :return:
    """
    # 删除空值的键值对
    for key in list(params.keys()):
        if params.get(key) is None:
            del params[key]

    url = url + "?" + urlencode(params)
    return url


def time_formatting(created_at, usefilename: bool = True, strftime: bool = None):
    """
    时间格式化
    :param created_at: 'Fri Dec 24 03:49:03 +0800 2021'
    :param usefilename: 启用文件名格式：20211224
    :param strftime: 含有时分秒格式 2021-12-24 3:49:03
    :return:
    """
    dt_obj = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
    if usefilename:
        strftime = '%Y%m%d'
    elif strftime:
        strftime = '%Y-%m-%d %H:%M:%S'
    else:
        strftime = '%Y-%m-%d'
    return dt_obj.astimezone(tz=None).strftime(strftime)


def compare_date(stime, etime):
    """
    时间比较
    :param stime: Mon Apr 17 14:54:10 +0800 2023
    :param etime: 2022-01-01 00:00:00
    :return: 最临近的时间-True
    """
    stime = time_formatting(stime, usefilename=False, strftime=True)
    s_time = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
    e_time = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
    if s_time.date() > e_time.date():
        return True
    elif s_time.date() == e_time.date():
        if s_time.time() > e_time.time():
            return True
    return False


def get_time_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getRedisKey(uid, url, filepath):
    """
    获取redis key
    :param uid:
    :param url:
    :param filepath:
    :return:
    """
    if "?" in url:
        url = url.split("?")[0]
    str_data = f"{uid}&{url}&{filepath}"
    md5 = hashlib.md5()
    md5.update(str_data.encode('utf-8'))
    return md5.hexdigest()


def thread_pool(method, data, **kwargs):
    """
    多线程任务
    :param method: 函数
    :param data: 可遍历列表数据
    :param kwargs:
    :return:
    """
    if isinstance(kwargs, dict):
        thread_num = kwargs.get('thread_num', 1)
        prompt = kwargs.get('prompt', '多线程任务->[线程数:%s]' % thread_num)
    else:
        raise Exception('kwargs is not dict')

    ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prompt = '[%s] 多线程任务 [线程数:%s]-> %s ->' % (ctime, thread_num, prompt)
    with futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
        res = tqdm(executor.map(method, data), total=len(data))
        res.set_description(prompt)
        return len(list(res))


def process_pool(method, data, **kwargs):
    """
    多进程任务
    :param method: 函数
    :param data: 可遍历列表数据
    :param kwargs:
    :return:
    """
    if isinstance(kwargs, dict):
        process_num = kwargs.get('process_num', 1)
        prompt = kwargs.get('prompt', '多进程任务->[线程数:%s]' % process_num)
    else:
        raise Exception('kwargs is not dict')

    ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prompt = '[%s] 多进程任务 [进程数:%s]-> %s ->' % (ctime, process_num, prompt)
    with futures.ProcessPoolExecutor(max_workers=process_num) as executor:
        res = tqdm(executor.map(method, data), total=len(data))
        res.set_description(prompt)
        return len(list(res))


def parse_user(users: List) -> List:
    return [user.split("/")[-1] for user in users]


def get_file_suffix(url):
    """
    通过url确定文件后缀
    # url = "https://xxx.xxx.cn/xx/xx.jpg?KID=xxx&referer=xxx.com"
    # url = "https://xxx.xxx.cn/xx/xx.jpg"
    # url = "https://xxx.xxx.com/xx/xx?livephoto=xxx.mov"
    :param url: url
    :return:
    """
    http_path = os.path.split(url)
    filename = http_path[1].split("?")[0]
    if "." in filename:
        suffix = filename.split(".")[-1]
    else:
        livephoto_path = http_path[1].split("?")[1]
        suffix = livephoto_path.split(".")[-1]
    return suffix
