#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/10 18:15
@Project:WeiboSpider
@File:sessionMiddleware.py
@Desc:session中间件
"""
from request.fetch import Session
from request.login import Login
from utils.function_tracer import Tracer
from utils.logger import logger


class SessionMiddleware(Session):
    loginObj = Login()
    login_times = 1

    @Tracer.log
    def fetch(self, url, headers=None, method='get', session=None, **kwargs):
        # 首次必须登录
        if self.login_times == 1:
            logger.info("开始第{}登录...".format(self.login_times))
            if self.loginObj.login_localhost(session=self.session):
                if not self.loginObj.is_login(fetch=super(SessionMiddleware, self).fetch):
                    self.loginObj.login_online(session=self.session,insert=False)
            else:
                self.loginObj.login_online(session=self.session,insert=True)
            self.login_times += 1
        response = super(SessionMiddleware, self).fetch(url, headers, method, session, **kwargs)
        if response.url != url:
            self.loginObj.login_online(session=self.session,insert=False)
            return self.fetch(url, headers, method, session, **kwargs)
        return response

    def fetch_json(self, url, headers=None, method='get', session=None, **kwargs):
        return self.fetch(url, headers, method, session, **kwargs).json()


