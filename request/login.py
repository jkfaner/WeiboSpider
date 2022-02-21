#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/10 22:42
@Project:WeiboSpider
@File:login.py
@Desc:登录
"""
import json
import requests

from requests import Session
from requests.cookies import RequestsCookieJar

from init import mysqlPool, login_config
from login.weibo import weibo
from utils.decrypt import AESStrDecrypt
from utils.logger import logger


class Login(object):

    def __init__(self):
        self.login_password = AESStrDecrypt.encrypt(login_config.password)

    @staticmethod
    def login_by_account():
        """
        账号密码登录
        :return:
        """
        wb_login = weibo()
        login_rest, login_session = wb_login.login(
            username=login_config.username,
            password=login_config.password,
            mode=login_config.mode
        )
        return login_rest, login_session

    @staticmethod
    def select_cookies() -> dict:
        """
        查询数据库cookies信息
        :return:
        """
        sql = f"SELECT username,password,uid,cookies FROM login_cookies WHERE username = %s"
        select_result = mysqlPool.getOne(sql=sql, param=[login_config.username])
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
        sql = "INSERT INTO login_cookies (username,password,uid,cookies) VALUES (%s,%s,%s,%s)"
        mysqlPool.update(sql=sql, param=[login_config.username, self.login_password, uid, cookies])
        mysqlPool.end()

    def update_cookies(self, uid, cookies: str):
        """
        更新cookies 没有就插入 有就更新
        :param uid:
        :param cookies:
        :return:
        """
        sql = "UPDATE login_cookies SET cookies=%s WHERE uid=%s"
        mysqlPool.update(sql=sql, param=[cookies, uid])
        mysqlPool.end()

    @staticmethod
    def dict_from_cookiejar(login_session: Session) -> str:
        """
        从session中获取cookies并加密
            注：防止cookies泄露这里使用aes加密
        :param login_session:
        :return:
        """
        _cookies = requests.utils.dict_from_cookiejar(login_session.cookies)
        return AESStrDecrypt.encrypt(json.dumps(_cookies))

    @staticmethod
    def cookiejar_from_str(cookies: str) -> RequestsCookieJar:
        """
        将加密的cookies解密
        :param cookies:
        :return:
        """
        new_cookies = json.loads(AESStrDecrypt.decrypt(cookies))
        cookies_CookieJar = requests.utils.cookiejar_from_dict(new_cookies, cookiejar=None, overwrite=True)
        return cookies_CookieJar

    def set_cookies(self, session: Session, cookiejar: RequestsCookieJar):
        """
        在session中设置cookies
        :param session:
        :param cookies:
        :return:
        """
        session.cookies = cookiejar

    def is_login(self,fetch):
        """
        检查cookie是否失效
        :param fetch:
        :return: 失效返回False 否则返回True
        """
        logger.info("检查登录...")
        url = "https://weibo.com/"
        response = fetch(url=url, method="get")
        if response.url != url:
            return False
        return True

    def login_online(self,session:Session,insert:bool):
        """
        登录
        :param insert: 插入数据：True，更新数据：False
        :return:
        """
        logger.info("联网登录...")
        login_rest, login_session = self.login_by_account()
        cookies = self.dict_from_cookiejar(login_session=login_session)
        if insert:
            self.insert_cookies(uid=login_rest['uid'], cookies=cookies)
        else:
            self.update_cookies(uid=login_rest['uid'], cookies=cookies)
        cookiejar = self.cookiejar_from_str(cookies)
        self.set_cookies(session=session, cookiejar=cookiejar)

    def login_localhost(self,session:Session):
        """
        本地登录
        :param session:
        :return:
        """
        logger.info("本地登录...")
        cookies_item = self.select_cookies()
        if cookies_item:
            cookies, uid = cookies_item['cookies'], cookies_item['uid']
            cookiejar = self.cookiejar_from_str(cookies)
            self.set_cookies(session=session, cookiejar=cookiejar)
            return True
        return False
