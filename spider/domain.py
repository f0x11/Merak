#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

import tornado.ioloop
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from data.models import LastDomain, Domain
from data.session_mysql import SessionCM

__author__ = 'f0x11'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
}

chars = '0123456789'
# chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

total = 0


def init_domain_info(domain):
    domain_info = []
    for c in domain:
        idx = chars.index(c)
        if idx < 0:
            logging.warning("domain error, domain=%s" % domain)
            raise Exception('domain error')

        domain_info.append(idx)

    return domain_info


def gen_domain_list(start_domain="00000"):
    """
    从前开始变化
    :param start_domain:
    """
    domain_len = len(start_domain)

    total_len = len(chars)

    # domain_info = [0] * domain_len
    domain_info = init_domain_info(start_domain)

    def gen_domain(i):
        if i >= domain_len:
            return False
        domain_info[i] += 1
        if domain_info[i] >= total_len:
            domain_info[i] = 0
            return gen_domain(i + 1)
        return True

    while True:
        global total
        total += 1
        yield ''.join([chars[d] for d in domain_info])
        con = gen_domain(0)
        if not con:
            break


@gen.coroutine
def capture_domain(domain):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch('https://www.godaddy.com/domainsapi/v1/search/exact?q={0}.com'.format(domain),
                                       headers=headers)
    if response.error:
        logging.error("Error: ", response.error)
        return

    content = json.loads(response.body.decode())

    is_available = content['ExactMatchDomain']['IsAvailable']

    with SessionCM() as db_session:
        if is_available:
            new_domain = Domain(content=domain)
            db_session.add(new_domain)
            db_session.commit()

        db_session.query(LastDomain).update({'content': domain})
        db_session.commit()


@gen.coroutine
def capture_domains():
    with SessionCM() as db_session:
        last_domain_item = db_session.query(LastDomain).first()

        if last_domain_item:
            start_domain = last_domain_item.content
        else:
            start_domain = '00000'

    for domain in gen_domain_list(start_domain):
        yield capture_domain(domain)
        yield gen.sleep(3)

    tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    # for i in gen_domain_list('11'):
    #     print(i)

    capture_domains()
    tornado.ioloop.IOLoop.instance().start()
