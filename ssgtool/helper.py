#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# @Time : 2022/7/12 0012 22:14
# @Author : Duckweeds7
# @Version：V 0.1
# @File : helper.py
# @desc :
"""
import os
import re


def safe_filename(filename, replace=''):
    """
    set the filename be verified
    :param filename:
    :param replace:
    :return:
    """
    return re.sub(re.compile(
        '[/\\\:*?"<>|]')
        , replace,
        filename
    )

def get_post_content(file_name):
    _content = open(file_name, 'r', encoding='utf-8').read()
    return _content

def set_double_quote(_value: str):
    _value = _value.replace('"', "'")
    if _value[0] == "'":
        _value = list(_value)
        _value[0] = '"'
        _value = "".join(_value)
    if _value[-1] == "'":
        _value = list(_value)
        _value[-1] = '"'
        _value = "".join(_value)
    if _value[0] != '"':
        _value = '"' + _value
    if _value[-1] != '"':
        _value += '"'
    return _value

def recursion_dir_all_file(path):
    '''
    :param path: 文件夹目录
    '''
    file_list = []
    for dir_path, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(dir_path, file)
            if "\\" in file_path:
                file_path = file_path.replace('\\', '/')
            file_list.append(file_path)
        for dir in dirs:
            file_list.extend(recursion_dir_all_file(os.path.join(dir_path, dir)))
    return file_list

def make_dir(_path):
    if not os.path.exists(_path):
        os.makedirs(_path)
