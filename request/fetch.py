#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project:
@File: fetch.py
@Ide: PyCharm
@Time: 2021-05-29 13:53:43
@Desc: request请求
"""
from random import choice

import requests
from requests import Response
from retrying import retry

from loader import ProjectLoader
from utils.logger import logger

retry_max_number = 10
retry_min_random_wait = 1000
retry_max_random_wait = 30000
fetch_timeout = 30000


class SessionLoader(object):
    _user_agents = ProjectLoader.getSystemConfig()["user-agent-list"]

    def __init__(self):
        self.user_agent = self._user_agents


class Session(SessionLoader):

    def __init__(self):
        super(Session, self).__init__()
        self.session = requests.session()

    @staticmethod
    def __need_retry(exception):
        result = isinstance(exception, (requests.ConnectionError, requests.ReadTimeout))
        if result:
            logger.warning(f'Exception: {type(exception)} occurred, retrying...')
        return result

    def __init_request_headers(self, session, **kwargs):
        session.headers.update({'User-Agent': choice(self.user_agent)})
        return session, kwargs

    def __fetch(self, session, url, method='get', check_code=True, **kwargs):

        @retry(stop_max_attempt_number=retry_max_number, wait_random_min=retry_min_random_wait,
               wait_random_max=retry_max_random_wait, retry_on_exception=self.__need_retry)
        def _fetch(session, url, check_code, **kwargs) -> Response:
            response = session.post(url, **kwargs) if method == 'post' else session.get(url, **kwargs)
            if check_code:
                if response.status_code == 401:
                    raise requests.ConnectionError("414 Request-URI Too Large")
                elif response.status_code != 200:
                    error_info = f'Expected status code 200, but got {response.status_code}.'
                    raise requests.ConnectionError(error_info)
            return response

        try:
            session, kwargs = self.__init_request_headers(session, **kwargs)
            resp = _fetch(session, url, check_code, **kwargs)
            return resp
        except Exception as e:
            error_info = 'Something got wrong, error msg:{}'.format(e)
            raise Exception(error_info)

    def fetch(self, url, headers=None, method='get', session=None, **kwargs):
        session = self.session if session is None else session
        resp = self.__fetch(session=session, url=url, method=method, headers=headers, **kwargs)
        return resp
