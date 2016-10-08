# -*- coding:utf-8 -*-

from django.contrib import admin
from blog_old_project.models import User
from blog_old_project.models import Tag
from blog_old_project.models import Comment
from blog_old_project.models import Category
from blog_old_project.models import Article
from blog_old_project.models import Links
from blog_old_project.models import Ad
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'click_count')
    list_display_links = ('title', 'desc')
    # list_editable = ('click_count')

    fieldsets = (
        (None, {
            'fields' : ('title', 'desc', 'content', 'user', 'category', 'tag')
        }),
        ('高级设置', {
            'classes' : ('collapse', ),
            'fields' : ('click_count', 'is_recommend',)
        }),
    )

    # class Media:
    #     js = (
    #         '/static/js/kindeditor-4.1.10/kindeditor-all-min.js',
    #         '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
    #         '/static/js/kindeditor-4.1.10/config.js',
    #     )

    # class Media:
    #     js = (
    #         "/static/js/jquery.min.js",
    #         "/static/uikit/js/uikit.min.js",
    #         "/static/codemirror/lib/codemirror.js",
    #         "/static/codemirror/mode/markdown/markdown.js",
    #         "/static/codemirror/addon/mode/overlay.js",
    #         "/static/codemirror/mode/xml/xml.js",
    #         "/static/codemirror/mode/gfm/gfm.js",
    #         "/static/js/marked/marked.min.js",
    #         "/static/uikit/js/components/htmleditor.js",
    #         "/static/js/config.js",
    #     )
    #     css = {'all':(
    #         "/static/uikit/css/uikit.min.css",
    #         "/static/uikit/css/components/htmleditor.css",
    #         "/static/codemirror/lib/codemirror.css",
    #     )}



admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
