#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# @Time : 2022/7/12 0012 22:14
# @Author : Duckweeds7
# @Version：V 0.1
# @File : config.py
# @desc :
"""
import random
import time

header_format_dict = {
    "toml": "+"
}
default_header_dict = {
    "layout": '"blog"',
    "title": '""',
    "description": '""',
    "date": f'{time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(int(time.time())))}',
    "lastmod": f'{time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(int(time.time())))}',
    "image": f'"https://picsum.photos/{random.randrange(800, 1600)}"',
    "slug": '""',
    "tags": '[]',
    "categories": '[]',
    "series": '[]'
}
