#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
# @Time : 2022/7/12 0012 22:27
# @Author : Duckweeds7
# @Version：V 0.1
# @File : main.py
# @desc :
"""
import os
import re
import shutil
import time
from os.path import basename
from loguru import logger
from slugify import slugify

from ssgtool.config import default_header_dict, header_format_dict
from ssgtool.helper import get_post_content, safe_filename, set_double_quote, recursion_dir_all_file, make_dir


def get_new_file_name(_old_file_name: str):
    return safe_filename(_old_file_name)


def check_the_format(_content: str):
    """

    :param _content:
    :return:
    """
    if _content[:3] == '+++':
        return 'toml'
    elif _content[:3] == '~~~':
        return 'yaml'
    else:
        return None


def get_post_header(_content, header_format):
    format_value = header_format_dict[header_format]
    re_pattern = "(\{}{3})([\s\S]*)(\{}{3})".replace("{}", format_value)
    _header = re.search(re_pattern, _content).group(2)
    return _header


def format_post_header(_header_dict: dict):
    _default_header_dict = default_header_dict
    for k, v in _header_dict.items():
        if k == 'image':
            continue
        _default_header_dict[k] = v
    if not _default_header_dict['slug'] or _default_header_dict['slug'] == '""':
        _default_header_dict['slug'] = '"' + slugify(_default_header_dict['title']) + '"'
    return _default_header_dict


def split_header_str(h_list: list, sep: str = "="):
    h_dict = {}
    for h in h_list:
        key, value = h.split(sep, 1)
        h_dict[key.strip()] = value.strip()
    return h_dict


def generate_new_header_str(_header_dict: dict, sep: str = " = ", _header_format: str = "toml", add_format=False):
    if add_format:
        _new_header_str = f'{header_format_dict[_header_format] * 3}\n'
    else:
        _new_header_str = '\n'
    for k, v in _header_dict.items():
        _new_header_str += f"{k}{sep}{set_double_quote(v) if k in ['title', 'layout', 'image', 'slug'] else v}\n"
    if add_format:
        _new_header_str += f'{header_format_dict[_header_format] * 3}'
    return _new_header_str


def generate_default_post(_title: str):
    _default_header_dict = default_header_dict
    _default_header_dict['title'] = _title
    _default_header_dict['slug'] = slugify(_title)

    with open(f"{safe_filename(_title)}.md", 'w', encoding='utf-8') as f:
        f.write(generate_new_header_str(_default_header_dict, add_format=True))


def catalogue_by_date(src_dir: str, src_data_key: str, src_date_format: str, target_date_format: str,
                      target_dir: str = None):
    if not target_dir:
        target_dir = src_dir
    move_count = 0
    file_count = 0
    source_dir_files = recursion_dir_all_file(src_dir)
    for file in source_dir_files:
        if file[-3:] != '.md':
            continue
        file_count += 1
        try:
            file_dir, content, header, header_list, header_dict = get_post_header_dict(file)
            src_date_str = header_dict[src_data_key]
            target_date_str = time.strftime(target_date_format, time.strptime(src_date_str, src_date_format))
            target_dir_path = os.path.join(target_dir, target_date_str)
            make_dir(target_dir_path)
            target_file_path = os.path.join(target_dir_path, basename(file))
            shutil.move(file, target_file_path)
            logger.info(f"move {file} to {target_file_path} succeed!")
            move_count += 1
        except Exception as e:
            logger.error(f"catalogue_by_date raise a {e} error")
    logger.info(f"catalogue finish: file_count:{file_count} move_count:{move_count}")


def get_post_header_dict(file_path: str):
    file_dir = os.path.dirname(file_path)
    content = get_post_content(file_path)
    header = get_post_header(content, check_the_format(content))
    header_list = list(filter(None, header.split("\n")))
    header_dict = split_header_str(header_list)
    return file_dir, content, header, header_list, header_dict


def format_post(file_path: str):
    file_dir, content, header, header_list, header_dict = get_post_header_dict(file_path)
    new_header_dict = format_post_header(header_dict)
    new_header_str = generate_new_header_str(new_header_dict)
    new_content = content.replace(header, new_header_str)
    new_file_path = os.path.join(file_dir, f"{get_new_file_name(new_header_dict['title'])}.md")
    with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    if new_file_path != file_path:
        os.remove(file_path)


if __name__ == '__main__':
    # format_post(r"D:\self\duckweeds7-blog\content\post\No module named 'scrapy.conf'报错解决方案\index.md")
    # generate_default_post("generate_test")
    catalogue_by_date("D:\self\duckweeds7-blog\content\post","date","%Y-%m-%dT%H:%M:%S","%Y-%m-%d")
# print(default_header_dict)
