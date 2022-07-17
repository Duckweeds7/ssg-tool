#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# @Time : 2022/7/12 0012 22:14
# @Author : Duckweeds7
# @Version：V 0.1
# @File : config.py
# @desc :
"""
import json
import os.path
import random
import time

config_json = json.load(open("./config/config.json", "r", encoding="utf-8"))
header_format_dict = config_json["header_format_dict"]
default_header_dict = config_json["default_header_dict"]
for k in default_header_dict.keys():
    value = default_header_dict[k]
    if value['type'] == 'datetime' and value['format']:
        default_header_dict[k] = f"{time.strftime(value['value'], time.localtime(int(time.time())))}",
    if value['type'] == 'image' and value['format']:
        default_header_dict[k] = value["value"]["url"].format(
            f"{random.randrange(int(value['value']['range_start']), int(value['value']['range_end']))}")

