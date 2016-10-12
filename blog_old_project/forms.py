# -*- coding:utf-8 -*-
from django import forms
from blog_old_project.models import Tag
from blog_old_project.models import Category
from blog_old_project.models import User

user_choices = ((user.pk, user.username) for user in User.objects.all())
tag_choices = ((tag.pk, tag.name) for tag in Tag.objects.all())
category_choices = ((cat.pk, cat.name) for cat in Category.objects.all())


class ArticleForm(forms.Form):
    '''
    文章表单
    '''
    title = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),
                              max_length=50,error_messages={"required":"title不能为空",})
    desc = forms.CharField(widget=forms.TextInput(attrs={"id": "desc", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),
                              max_length=50,error_messages={"required":"desc不能为空",})
    content = forms.CharField(widget=forms.Textarea(attrs={"id":"content","class": "input-text",
                                                           "required": "required", "cols": "75",
                                                           "rows": "5", "tabindex": "4",
                                                           "data-uk-htmleditor":"{markdown:true, mode:'split', maxsplitsize:600}"}),
                                                    error_messages={"required":"article不能为空",})

    user = forms.ChoiceField(required=True,
        widget=forms.Select(attrs={"id":"user"}),
        choices=user_choices)

    category = forms.ChoiceField(required=True,
        widget=forms.Select(attrs={"id":"category"}),
        choices=category_choices)

    tag = forms.MultipleChoiceField(
        required=True,
        widget=forms.SelectMultiple(attrs={"id":"tag"}),
        choices=tag_choices)



class CommentForm(forms.Form):
    '''
    评论表单
    '''
    author = forms.CharField(widget=forms.TextInput(attrs={"id": "author", "class": "comment_input",
                                                           "required": "required","size": "25", "tabindex": "1"}),
                              max_length=50,error_messages={"required":"username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
                                                           "required":"required","size":"25", "tabindex":"2"}),
                                 max_length=50, error_messages={"required":"email不能为空",})
    url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                              max_length=100, required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "input-text",
                                                           "required": "required", "cols": "75",
                                                           "rows": "5", "tabindex": "4",
                                                           "data-uk-htmleditor":"{markdown:true, mode:'split', maxsplitsize:600, toolbar:[ 'bold', 'italic', 'strike', 'link', 'blockquote', 'listUl', 'listOl' ]}"}),
                                                    error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())

    pid = forms.CharField(widget=forms.HiddenInput(), required=False)


class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})


class RegisterForm(forms.Form):
    '''
    注册
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required", }),
                               max_length=50, error_messages={"required": "username不能为空", })
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required", }),
                             max_length=50, error_messages={"required": "email不能为空", })
    url = forms.URLField(widget=forms.TextInput(attrs={"placeholder": "Url", }),
                         max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "password不能为空", })