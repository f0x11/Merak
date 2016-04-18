#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import tornado.web

import etc

__author__ = 'f0x11'


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")
        if user_cookie == etc.user_cookie:
            return user_cookie
        else:
            raise tornado.web.HTTPError(401)


def user_auth(func):
    @functools.wraps(func)
    def wrapper(handler, *args, **kwargs):
        if not handler.current_user:
            raise tornado.web.HTTPError(401)
    return wrapper
