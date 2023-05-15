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
import time
from concurrent import futures
from urllib.parse import urlencode
from tqdm import tqdm


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
    url = url + "?" + urlencode(removeNoneDict(params))
    return url


def removeNoneDict(item: dict):
    """
    删除空值的键值对
    :param item:
    :return:
    """
    for key in list(item.keys()):
        if item.get(key) is None:
            del item[key]
    return item


def is_valid_date(strdate):
    '''判断是否是一个有效的日期字符串'''
    try:
        if ":" in strdate:
            time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(strdate, "%Y-%m-%d")
        return True
    except:
        return False


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


def match_date(create_time: str, filter_date: str) -> bool:
    """
    符合时间
    :param create_time:
    :param filter_date:约定的时间
    :return:
    """

    created_at = datetime.datetime.strptime(time_formatting(create_time, usefilename=False), '%Y-%m-%d').date()
    setting_created_at = datetime.datetime.strptime(filter_date, '%Y-%m-%d').date()
    if created_at > setting_created_at:
        return True
    return False


def compare_date(stime, etime):
    """
    时间比较
    :param stime: Mon Apr 17 14:54:10 +0800 2023
    :param etime: 2022-01-01 00:00:00
    :return: 最临近的时间-True
    """
    t = time_formatting(stime, usefilename=False, strftime=True)
    s_time = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    e_time = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
    if s_time.date() > e_time.date():
        return True
    else:
        if s_time.time() > s_time.time():
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
    return get_str_md5(str_data=str_data)


def get_str_md5(str_data):
    """
    获取字符串md5值
    :param str_data:
    :return:
    """
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


def EntityToJson(entity):
    """
    Entity实体类转json
    :param entity:
    :return:
    """
    return json.dumps(entity, default=lambda o: {k.split("__")[-1]: v for k, v in o.__dict__.items()}, sort_keys=True,
                      ensure_ascii=False, indent=2)
