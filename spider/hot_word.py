#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from bs4 import BeautifulSoup
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from data.models import HotWord
from data.session_mysql import SessionCM

__author__ = 'f0x11'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
}


@gen.coroutine
def capture_hot_words():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch('http://weixin.sogou.com/', headers=headers)
    if response.error:
        logging.error("Error: ", response.error)
        return

    content = response.body
    soup = BeautifulSoup(content, "html.parser")
    top_number_list = soup.find_all(attrs={'class': 'top-num'})

    with SessionCM() as db_session:
        for top_number in top_number_list:
            hot_item = HotWord(number=int(top_number.string),
                               word=top_number.parent.attrs['title'])

            try:
                db_session.add(hot_item)
                db_session.commit()
            except Exception as e:
                print('hot_word error:%s' % e)


if __name__ == '__main__':
    capture_hot_words()
