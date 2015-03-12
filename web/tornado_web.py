#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
    tornado web 开发模板程序
"""
import tornado.web
import tornado.httpserver
import tornado.options
import torndb
import os
import sys
import tornado.log
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from tornado.options import define, options

sys.path.append('..')
import watch_jd

reload(sys)
sys.setdefaultencoding('utf-8')

define("port", default=9123, type=int, help="使用端口 --port=9876")

class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/add', AddHandler),
            (r'/login', LoginHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="nvvFPjUTTxKh309Kb8V0opSxA8l4a9D6h0bN5Hd3L+s=",
            xsrf_cookies=True,
            login_url="/login",
            gzip=True,
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(20)

    def get_current_user(self):
        user = self.get_secure_cookie("username")
        return user if user == "demo" else None

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/add')

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/add")

class AddHandler(BaseHandler):
    def get(self):
        self.render('add.html')

    @run_on_executor
    def post(self):
        jdurl = self.get_argument('jdurl')
        if jdurl:
            watch_jd.watch_item(jdurl)
            self.render('add_ok.html', jdurl=jdurl)

def check_price():
    watch_jd.watch_item()

def main():
    tornado.options.parse_command_line()
    app = App()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(options.port)
    tornado.ioloop.PeriodicCallback(check_price, 60*10*1000).start()  # checked every 10 mins
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
