#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import etc
from handlers.base import BaseHandler

__author__ = 'f0x11'


class DomainHandler(BaseHandler):
    def get(self):
        self.render('domain.html')

    def post(self):
        pwd = self.get_argument('pwd')

        if pwd == etc.user_cookie:
            self.set_secure_cookie(etc.user_cookie)

        self.write(json.dumps({'code': 0, 'msg': 'ok'}))
