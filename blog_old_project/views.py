# -*- coding:utf-8 -*-

import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from blog_old_project.models import Article
from blog_old import settings
from blog_old_project.models import Category
from blog_old_project.models import Comment
from blog_old_project.models import User
from blog_old_project.forms import CommentForm
from blog_old_project.forms import LoginForm
from blog_old_project.forms import RegisterForm
from blog_old_project.forms import ArticleForm
from blog_old_project.forms import Tag
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from blog_old_project.tools.MyPagination import JuncheePaginator


logger = logging.getLogger('blog.views')
# Create your views here.

# 站点的背景信息
def global_settings(request):
    # 站点基本信息
    # SITE_URL = settings.SITE_URL
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # action_name = request.GET.get('action', 'index')
    return locals()


# 首页列表
def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()

        #文章分页信息
        cur_page = int(request.GET.get('page', '0'))
        article_list = getPaginator(request, article_list, cur_page, )

        # 分类信息获取（导航数据）
        category_list = Category.objects.all()[:6]

        # 文章归档获取
        archive_list = Article.objects.distinct_date()

    except Exception as e:
        print e
    return render(request, 'index.html', locals())


# not ulrs : 得到分页器
def getPaginator(request, obj_list, curPage, page_size=5):
    paginator = JuncheePaginator(obj_list, page_size)
    try:
        cur_page = int(curPage)
        obj_list = paginator.page(cur_page)
    except Exception as e:
        obj_list = paginator.page(1)
    return obj_list


# 文章详情
def article(request):
    try:
        # 获取文章id
        try:
            id = request.GET.get('id', None)
            article = Article.objects.get(pk=id)
        except Exception as e:
            return render(request, 'faliure.html', {'msg' : '获取文章失败'})

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        # 获取文章评论
        try:
            # 获取评论信息
            comments = Comment.objects.filter(article=article).order_by('id')
            comment_list = []
            for comment in comments:
                for item in comment_list:
                    if not hasattr(item, 'children_comment'):
                        setattr(item, 'children_comment', [])
                    if comment.pid == item:
                        item.children_comment.append(comment)
                        break
                if comment.pid is None:
                    comment_list.append(comment)
            for comment in comment_list:
                has_more_comment = False
                if len(comment.children_comment) > 3:
                    has_more_comment = True
                    comment.children_comment = comment.children_comment[:3]
                setattr(comment, 'has_more_comment', has_more_comment)
        except Exception as e:
            return render(request, 'faliure.html', {'msg', '获取'+str(id)+'文章的评论失败'})

    except Exception as e:
        pass
    return render(request, 'info.html', locals())


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = Comment.objects.create(
                username = comment_form.cleaned_data['author'],
                email = comment_form.cleaned_data['email'],
                url = comment_form.cleaned_data['url'],
                content = comment_form.cleaned_data['comment'],
                pid=Comment.objects.get(pk=comment_form.cleaned_data["pid"]) if comment_form.cleaned_data[
                    "pid"] else None,
                article_id=comment_form.cleaned_data["article"],
                user=request.user if request.user.is_authenticated() else None,
            )
            comment.save()
        else:
            return render(request, 'failure.html', {'msg': comment_form.errors})
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 文章归档
def archive(request):
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
        article_list = getPaginator(request, article_list, 1, 5)
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'archive.html', locals())


# 文章分类
def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'msg': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPaginator(request, article_list, 1, 5)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())


# 登录
def do_login(request):
    try:
        if request.method=='POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 开始登录
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user != None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'msg': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else :
                return render(request, 'failure.html', {'msg' : '登录错误'})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


# 注册
def do_register(request):
    try:
        if request.method == "POST":
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                # 开始注册
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password']
                email = register_form.cleaned_data['email']
                url = register_form.cleaned_data['url']

                user = User.objects.create(username=username,
                                           password=make_password(password, None, 'pbkdf2_sha256'),
                                           email=email,
                                           url=url,)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'msg' : '注册失败'})
        else:
            register_form = RegisterForm()

    except Exception as e:
        logger.error(e)
    return render(request, 'register.html', locals())


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 评论回复
def reply_comment(request):
    try:
        # 得到评论id 和 文章id 和 分号码
        comment_id = request.GET.get('comment_id')
        article_id = request.GET.get('article_id')
        page = request.GET.get('page', 1)
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': article_id,
                                    'pid': comment_id} if request.user.is_authenticated() else{'article': article_id})

        # 获取评论信息
        comment = Comment.objects.get(pk=comment_id)
        comment_children_list = Comment.objects.filter(pid=comment_id)
        comment_children_list = getPaginator(request, comment_children_list, page, 8)

    except Exception as e:
        logger.error(e)
        return render(request, 'failure.html', {'msg': '获取评论信息失败'+str(e)})
    return render(request, 'reply_comment.html', locals())


def article_add(request):
    try:
        article_form = ArticleForm()
    except Exception as e:
        logger.error(e)
        return render(request, 'failure.html', {'msg': '获取评论信息失败' + str(e)})
    return render(request, 'article_add.html', locals())


def article_post(request):
    try:
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = Article.objects.create(
                title=article_form.cleaned_data['title'],
                desc=article_form.cleaned_data['desc'],
                content=article_form.cleaned_data['content'],
                user=User.objects.get(pk=article_form.cleaned_data['user']),
                category=Category.objects.get(pk=article_form.cleaned_data['category']),
                # tag=Tag.objects.get(pk=article_form.cleaned_data['tag']),
            )
            for tag in article_form.cleaned_data['tag']:
                article.tag.add(Tag.objects.get(pk=tag))
            article.save()
        else:
            return render(request, 'failure.html', {'msg': article_form.errors})
    except Exception as e:
        print e
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


def blogs(request):
    return render(request, 'newPages/blogs.html', locals())


def blog(request):
    return render(request, 'newPages/blog.html', locals())


def signin(request):
    return render(request, 'newPages/signin.html', locals())


def register(request):
    return render(request, 'newPages/register.html', locals())


def blog_edit(request):
    return render(request, 'newPages/manage_blog_edit.html', locals())


def mark(request):
    return render(request, 'newPages/mark_page.html', locals())