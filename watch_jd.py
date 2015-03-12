#!/usr/bin/env python
#-*-coding:utf-*-
"""
    关注京东的某个商品是否降价
    如果降价，就发短信通知机主，否则继续监视
    关注的商品的 skuid 存放在 skuid.txt 文本中
    skuid.txt format:
    {skuid:{price:12, stock_state: 1, last_update:time.time()}}
"""
import jd
import notify
import time
import simplejson as json

def get_skuid(file=None):
    if not file:
        file = "/tmp/skuid.txt"
    try:
        with open(file, 'r') as f:
            all_skuid = json.load(f)
    except Exception as e:
        jd.jdlog.warning(e)
        return {}

    return all_skuid

def save_skuid(all_skuid, file=None):
    if not file:
        file = "/tmp/skuid.txt"

    with open(file, 'w') as f:
        f.write(json.dumps(all_skuid))

def watch_item(url=None, send_msg=True, phone_num=None, phone_pwd=None):
    all_skuid = get_skuid()
    if url:
        skuid = jd.parse_url_for_skuid(url)
        if not skuid:
            return
        data = all_skuid.get(skuid, None)
        if data:
            """ update check price """
            ret = jd.run(skuid)
            if ret['price'] > 0 and ret['price'] < data['price'] and ret['stock_state'] == 1:
                """ goods on sale, notify user """
                send_title = skuid + ret['title']
                send_msg = str(ret['price'])
                notify.fetion(send_title, send_msg)

                del ret['title']
                all_skuid[skuid] = ret
        else:
            """ new item, save into txt """
            ret = jd.run(skuid)
            if ret['price'] > 0:
                """ insert into file """
                del ret['title']
                all_skuid[skuid] = ret

    else:
        """ traverse all_skuid to check price """
        skuids = all_skuid.keys()
        for skuid in skuids:
            ret = jd.run(skuid)
            if ret['price'] > 0 and ret['price'] < all_skuid[skuid]['price'] and ret['stock_state'] == 1:
                """ goods on sale, notify user """
                send_title = skuid + ret['title']
                send_msg = str(ret['price'])
                notify.fetion(send_title, send_msg)

                del ret['title']
                all_skuid[skuid] = ret

    save_skuid(all_skuid)

def remove_watch_item(url):
    all_skuid = get_skuid()

    if url:
        skuid = jd.parse_url_for_skuid(url)
        if not skuid:
            return

        del all_skuid[skuid]
        save_skuid(all_skuid)

def run_forever():
    while True:
        watch_item()
        time.sleep(60)

if __name__ == "__main__":
    #watch_item("http://item.jd.com/1217505.html")
    #watch_item()
    run_forever()
