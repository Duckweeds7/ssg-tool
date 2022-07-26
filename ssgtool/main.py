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
from typing import Optional

from loguru import logger
from slugify import slugify

from ssgtool.config import default_header_dict, header_format_dict
from ssgtool.helper import get_post_content, safe_filename, set_double_quote, recursion_dir_all_file, make_dir


def get_new_file_name(_old_file_name: str) -> str:
    return safe_filename(_old_file_name)


def check_the_format(_content: str) -> Optional[str]:
    """
    check the post header format
    :param _content:
    :return:
    """
    if _content[:3] == '+++':
        return 'toml'
    elif _content[:3] == '---':
        return 'yaml'
    else:
        return None


def get_post_header(_content: str, header_format: str) -> str:
    """

    :param _content:
    :param header_format:
    :return:
    """
    format_value = header_format_dict[header_format]
    re_pattern = "(\{}{3})([\s\S]*)(\{}{3})".replace("{}", format_value)
    _header = re.search(re_pattern, _content).group(2)
    return _header


def format_post_header(_header_dict: dict) -> dict:
    """

    :param _header_dict:
    :return:
    """
    _default_header_dict = default_header_dict
    for k, v in _header_dict.items():
        if k == 'image':
            continue
        _default_header_dict[k] = v
    if not _default_header_dict['slug'] or _default_header_dict['slug'] == '""':
        _default_header_dict['slug'] = '"' + slugify(_default_header_dict['title']) + '"'
    return _default_header_dict


def split_header_str(header_list: list, sep: str = "=") -> dict:
    """
    split value in list by sep
    :param header_list:
    :param sep:
    :return:
    """
    header_dict = {}
    for h in header_list:
        key, value = h.split(sep, 1)
        header_dict[key.strip()] = value.strip()
    return header_dict


def generate_new_header_str(header_dict: dict, sep: str = " = ", header_format: str = "toml", add_format=False) -> str:
    """

    :param header_dict:
    :param sep:
    :param header_format:
    :param add_format:
    :return:
    """
    if add_format:
        new_header_str = f'{header_format_dict[header_format] * 3}\n'
    else:
        new_header_str = '\n'
    for k, v in header_dict.items():
        new_header_str += f"{k}{sep}{set_double_quote(v) if k in ['title', 'layout', 'image', 'slug'] else v}\n"
    if add_format:
        new_header_str += f'{header_format_dict[header_format] * 3}'
    return new_header_str


def generate_default_post(_title: str):
    """
    generate a new post by default way
    :param _title:
    :return:
    """
    _default_header_dict = default_header_dict
    _default_header_dict['title'] = _title
    _default_header_dict['slug'] = slugify(_title)

    with open(f"{safe_filename(_title)}.md", 'w', encoding='utf-8') as f:
        f.write(generate_new_header_str(_default_header_dict, add_format=True))


def catalogue_by_date(src_dir: str, src_data_key: str, src_date_format: str, target_date_format: str,
                      target_dir: str = None, is_recursion: bool = True) -> bool:
    """
    Batch categorize blogs in a specified time format
    :param is_recursion: optional
    :param src_dir:
    :param src_data_key:
    :param src_date_format:  eg:%Y-%m-%d
    :param target_date_format: eg:%Y-%m-%d
    :param target_dir: optional
    :return:
    """
    if not target_dir:
        target_dir = src_dir
    move_count = 0
    file_count = 0
    source_dir_files = recursion_dir_all_file(src_dir, is_recursion)
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
    return True


def get_post_header_dict(file_path: str) -> tuple:
    """
    :param file_path:
    :return:
    """
    file_dir = os.path.dirname(file_path)
    content = get_post_content(file_path)
    header = get_post_header(content, check_the_format(content))
    header_list = list(filter(None, header.split("\n")))
    header_dict = split_header_str(header_list)
    return file_dir, content, header, header_list, header_dict


def format_post(file_path: str) -> bool:
    """

    :param file_path: posts path
    :return:
    """
    try:
        file_dir, content, header, header_list, header_dict = get_post_header_dict(file_path)
        new_header_dict = format_post_header(header_dict)
        new_header_str = generate_new_header_str(new_header_dict)
        new_content = content.replace(header, new_header_str)
        new_file_path = os.path.join(file_dir, f"{get_new_file_name(new_header_dict['title'])}.md")
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        if new_file_path != file_path:
            os.remove(file_path)
    except Exception as e:
        logger.warning(f"format_post raise a {e} error")
        return False
    return True


if __name__ == '__main__':
    # format_post(r"D:\self\duckweeds7-blog\content\post\No module named 'scrapy.conf'报错解决方案\index.md")
    # generate_default_post("利用代理池产生的日志生产威胁情报")
    catalogue_by_date("D:\self\duckweeds7-blog\content\post", "date", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d",
                      is_recursion=False)
# print(default_header_dict)
