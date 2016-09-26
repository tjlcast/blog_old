# -*- coding:utf-8 -*-
from django import template
register = template.Library()

# 定义一个将日期中的月份转换为大写的过滤器，如8转为八
# @register.filter
# @register.filter(name='month_to_upper')
def month_to_upper(key):
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'][key.month - 1]


def list_empty(l):
    if len(l) == 0:
        return True
    return False


def content_slice(content, begin='0', length='100'):
    begin = int(begin)
    length = min(int(length), len(content))
    return content[begin:length]


def generate_range(page):
    return range(page.start_index(), page.end_index()+1)


register.filter('month_to_upper', month_to_upper)
register.filter('list_empty', list_empty)
register.filter('content_slice', content_slice)