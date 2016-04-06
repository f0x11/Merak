#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import tornado.web
from handlers.hot_word import HotWordHandler

__author__ = 'f0x11'

CONFIG = [
    (r"/", HotWordHandler),
]


def config_logger():
    debug = application.settings['debug']

    if debug:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    logging.basicConfig(filename='merak.log', filemode='w', level=level)


if __name__ == "__main__":
    application = tornado.web.Application(
        CONFIG,
        template_path='templates',
        static_path='static',
        debug=True)
    application.listen(7777, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()
