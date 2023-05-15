#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/10 22:42
@Project:WeiboSpider
@File:login.py
@Desc:登录
"""
import json
import requests
from DecryptLogin.core import weibo

from requests import Session
from requests.cookies import RequestsCookieJar

from loader import ProjectLoader
from aop import LoggerAOP
from utils.constants import REDIS_LOGIN_NAME


class LoginLoader(object):
    _sql_dict = ProjectLoader.getDatabaseConfig()["mysql"]["sql"]["login"]
    _login_user = ProjectLoader.getSpiderConfig()["login"]
    _mysql_client = ProjectLoader.getMysqlClient()
    _redis_client = ProjectLoader.getRedisClient()

    def __init__(self):
        self.sql_dict = self._sql_dict
        self.login_user = self._login_user
        self.mysql_client = self._mysql_client
        self.redis_client = self._redis_client


class LoginMysql(LoginLoader):

    def select_cookies(self) -> dict:
        """
        查询数据库cookies信息
        :return:
        """
        sql = self.sql_dict.get("select_cookies")
        select_result = self.mysql_client.getOne(sql=sql, param=[self.login_user.get("uid")])
        if not select_result:
            return {}
        s_cookies = select_result.get("cookies").decode("utf-8")
        uid = select_result.get("uid").decode("utf-8")
        return dict(cookies=s_cookies, uid=uid)

    def insert_cookies(self, uid, cookies: str):
        """
        插入cookies
        :param uid:
        :param cookies:
        :return:
        """
        sql = self.sql_dict.get("insert_cookies")
        self.mysql_client.update(sql=sql, param=[uid, cookies])
        self.mysql_client.end()

    def update_cookies(self, uid, cookies: str):
        """
        更新cookies 没有就插入 有就更新
        :param uid:
        :param cookies:
        :return:
        """
        sql = self.sql_dict.get("update_cookies")
        self.mysql_client.update(sql=sql, param=[cookies, uid])
        self.mysql_client.end()

    @staticmethod
    def dict_from_cookiejar(login_session: Session) -> str:
        """
        :param login_session:
        :return:
        """
        _cookies = requests.utils.dict_from_cookiejar(login_session.cookies)
        return json.dumps(_cookies)

    @staticmethod
    def cookiejar_from_str(cookies: str) -> RequestsCookieJar:
        """
        :param cookies:
        :return:
        """
        new_cookies = json.loads(cookies)
        return requests.utils.cookiejar_from_dict(new_cookies, cookiejar=None, overwrite=True)

    @staticmethod
    def set_cookies(session: Session, cookiejar: RequestsCookieJar):
        """
        在session中设置cookies
        :param cookiejar:
        :param session:
        :return:
        """
        session.cookies = cookiejar

    @staticmethod
    @LoggerAOP(message="检查登录...")
    def is_login(fetch):
        """
        检查cookie是否失效
        :param fetch:
        :return: 失效返回False 否则返回True
        """
        url = "https://weibo.com/"
        response = fetch(url=url, method="get")
        if response.url != url:
            return False
        return True

    @LoggerAOP(message="联网登录...")
    def login_online(self, session: Session, insert: bool):
        """
        登录
        :param session:
        :param insert: 插入数据：True，更新数据：False
        :return:
        """
        login_rest, login_session = weibo().login()
        uid = login_rest['uid']
        cookies = self.dict_from_cookiejar(login_session=login_session)
        if insert:
            self.insert_cookies(uid=uid, cookies=cookies)
        else:
            self.update_cookies(uid=uid, cookies=cookies)
        cookiejar = self.cookiejar_from_str(cookies)
        self.set_cookies(session=session, cookiejar=cookiejar)

    @LoggerAOP(message="本地登录...")
    def login_localhost(self, session: Session):
        """
        本地登录
        :param session:
        :return:
        """
        cookies_item = self.select_cookies()
        if cookies_item:
            cookies, uid = cookies_item['cookies'], cookies_item['uid']
            cookiejar = self.cookiejar_from_str(cookies)
            self.set_cookies(session=session, cookiejar=cookiejar)
            return True
        return False


class LoginRedis(LoginMysql):

    def select_cookies(self) -> dict:
        """
        查询数据库cookies信息
        :return:
        """
        uid = self.login_user.get("uid")
        cookies = self.redis_client.hget(REDIS_LOGIN_NAME, uid)
        if not cookies:
            return {}
        cookies = json.loads(cookies)
        return dict(cookies=cookies, uid=uid)

    def insert_cookies(self, uid, cookies: str):
        """
        插入cookies
        :param uid:
        :param cookies:
        :return:
        """
        self.redis_client.hset(REDIS_LOGIN_NAME, uid, cookies)

    def update_cookies(self, uid, cookies: str):
        """
        更新cookies 没有就插入 有就更新
        :param uid:
        :param cookies:
        :return:
        """
        self.insert_cookies(uid, cookies)

    @staticmethod
    def cookiejar_from_str(cookies: dict) -> RequestsCookieJar:
        """
        :param cookies:
        :return:
        """
        return requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)

    @LoggerAOP(message="联网登录...")
    def login_online(self, session: Session, insert: bool):
        """
        登录
        :param session:
        :param insert: 插入数据：True，更新数据：False
        :return:
        """
        login_rest, login_session = weibo().login()
        uid = login_rest['uid']
        cookies = self.dict_from_cookiejar(login_session=login_session)
        if insert:
            self.insert_cookies(uid=uid, cookies=cookies)
        else:
            self.update_cookies(uid=uid, cookies=cookies)
        cookiejar = self.cookiejar_from_str(cookies)
        self.set_cookies(session=session, cookiejar=cookiejar)

    @LoggerAOP(message="本地登录...")
    def login_localhost(self, session: Session):
        """
        本地登录
        :param session:
        :return:
        """
        cookies_item = self.select_cookies()
        if cookies_item:
            cookies, uid = cookies_item['cookies'], cookies_item['uid']
            cookiejar = self.cookiejar_from_str(cookies)
            self.set_cookies(session=session, cookiejar=cookiejar)
            return True
        return False


class Login(LoginRedis):
    pass
