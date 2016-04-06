#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import tornado.web
from data.models import HotWord
from data.session_mysql import SessionCM
from spider.hot_word import capture_hot_words

__author__ = 'f0x11'


class HotWordHandler(tornado.web.RequestHandler):
    def get(self):
        with SessionCM() as db_session:
            hot_word_list = db_session.query(HotWord)\
                .order_by(HotWord.created_time.desc()).all()

            self.render("index.html", hot_word_list=hot_word_list)

    def post(self):
        capture_hot_words()
        self.write(json.dumps({'code': 0, 'msg': 'ok'}))
