#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
    1、检测商品是否有货(支持省、市，默认是四川成都)；
    2、获取当前价格；
    输入值，商品 url 或者 skuid
    返回值: (time.time(), 是否有货,当前价格)
"""
import re
import time
import requests

from mylogger import get_logger

jdlog = get_logger('jd')

def run(url, provinceid=1, cityid=72):
    skuid = parse_url_for_skuid(url)
    if skuid:
        title, stock_state = check_if_in_stock(skuid, provinceid, cityid)
        price = get_current_price(skuid)
        return {"last_update": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "stock_state":stock_state, "price":price, "title":title}

def parse_url_for_skuid(url):
    if url.find('jd') != -1:
        """ url parse, get skuid """
        skuid = re.compile(r'jd.com/(\d+).html').findall(url)[0]
        return skuid
    else:
        if re.match(r'^\d+$', url):
            return url

    return None

def check_if_in_stock(skuid, provinceid, cityid):
    url = "http://item.jd.com/{skuid}.html".format(skuid=skuid)
    url_rewrite, ret = download_url(url)
    if url_rewrite:
        jdlog.warning("wrong url %s" % url)
        return (None, -1)

    if ret:
        skuidkey = str(re.compile(r'skuidkey:\'(\w+)\'').findall(ret)[0])
        title = re.compile(r'<title>(.*?)</title>').findall(ret)[0]
        url = "http://st.3.cn/gds.html?skuid={skuidkey}&provinceid={provinceid}&cityid={cityid}&isNew=1&ch=1&callback=getStockCallback".format(
                skuidkey=skuidkey, provinceid=provinceid, cityid=cityid)
        url_rewrite, ret = download_url(url)
        if ret.find(u'现货') != -1:
            return (title, 1) # in stock
        else:
            return (title, 0) # out of stock
    else:
        return (None, -1) # error happened

def get_current_price(skuid):
    url = "http://p.3.cn/prices/get?skuid=J_%s" % skuid
    url_rewrite, ret = download_url(url, ret_json=True)
    if ret:
        return float(ret[0]['p'])
    else:
        return -1

def download_url(url, ret_json=False):
    url_rewrite = False
    jdlog.info("current downloading url: %s" % url)
    try:
        r = requests.get(url, timeout=10)

        if url != str(r.url):
            url_rewrite = True

        if ret_json:
            return (url_rewrite, r.json())

        return (url_rewrite, r.text)
    except Exception as e:
        jdlog.warning('failed download : %s' % url)
        return

def test():
    print run("121988333030")

if __name__ == "__main__":
    test()

