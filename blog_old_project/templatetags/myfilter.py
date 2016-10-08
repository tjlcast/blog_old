# -*- coding:utf-8 -*-

from django import template
# from markdown import markdown
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
# import markdown2
import blog_old_project.markdown2
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


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


def my_markdown(value):
    # value = text2html(value)
    value =  blog_old_project.markdown2.markdown(value)
    return value


register.filter('my_markdown', my_markdown)
register.filter('month_to_upper', month_to_upper)
register.filter('list_empty', list_empty)
register.filter('content_slice', content_slice)