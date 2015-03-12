#!/usr/bin/python
#-*-coding: utf-8 -*-
""" from https://github.com/aec4d/ScriptLet/tree/master/onlinestatistics """
import requests
from jd import jdlog

def fetion(title, msg, phone=PHONE_NUM, pwd=PWD):
    jdlog.info("sending msg: [%s:%s] %s %s" % (phone, pwd, title, msg))
    url_space_login = 'http://f.10086.cn/huc/user/space/login.do'
    url_login = 'http://f.10086.cn/im/login/cklogin.action'
    url_sendmsg = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'

    post_data = {
        'mobilenum': phone,
        'password': pwd,
        "m": "submit",
        "fr": "space",
        "backurl": "http://f.10086.cn/"
    }

    _session = requests.Session()
    _session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Connection': 'close'
    })

    _session.post(url_space_login, data=post_data)
    _session.get(url_login)
    send = _session.post(url_sendmsg, data={'msg': title + " " + msg})

    if u"成功" in send.text:
        return (True, send.text)
    return (False, send.text)

if __name__ == '__main__':
    fetion('商品名', '价格，降价')
