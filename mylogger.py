#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
#=============================================================================
# FileName:     mylogger.py
# Desc:         python logger support zip log file
# Author:       leyle
# Email:        leyle@leyle.com
# HomePage:     http://www.leyle.com/
# Git_page:     https://github.com/leyle
# Version:      0.1.2
# LastChange:   2015-03-10 11:09:59
#=============================================================================
'''
import logging
import logging.handlers
import sys
import os

LOGGING_MSG_FORMAT = "%(name)s %(levelname)s %(asctime)s: %(message)s"
LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(logfile, path="logs/", level=logging.DEBUG, max_byte=1024*1024*50, backup_count=10):
    root_logger = logging.getLogger(logfile)
    if len(root_logger.handlers) == 0:
        if path.startswith('/'):
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except OSError as e:
                    print e
                    sys.exit(1)
            else:
                if not os.access(path, os.R_OK|os.W_OK):
                    print path, "without read/write permission"
                    sys.exit(1)
        else:
            """ create new log file path, pwd+path """
            path = os.path.join(sys.path[0], path)
            if not os.path.isdir(path):
                os.makedirs(path)

        if not path.endswith('/'):
            path = path + '/'

        handler = logging.handlers.RotatingFileHandler(
                    path + logfile + ".log",
                    mode = "a",
                    maxBytes = max_byte,
                    backupCount = backup_count,
                    encoding = "utf-8"
                    )

        fmter = logging.Formatter(LOGGING_MSG_FORMAT, LOGGING_DATE_FORMAT)
        handler.setFormatter(fmter)
        root_logger.addHandler(handler)
        root_logger.setLevel(level)

    return logging.getLogger(logfile)



def test():
    #get_logger(logfile, path="logs/", level=logging.DEBUG, max_byte=1024*1024*50, backup_count=10):
    mylog = get_logger("log_name", "abc/def", max_byte=100)
    for i in range(0, 10000):
        mylog.info("%d" % i)

if __name__ == "__main__":
    test()
