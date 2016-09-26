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

    class Media:
        js = (
            '/static/js/kindeditor-master/kindeditor-all-min.js',
            '/static/js/kindeditor-master/lang/zh_CN.js',
            '/static/js/kindeditor-master/config.js',
        )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
