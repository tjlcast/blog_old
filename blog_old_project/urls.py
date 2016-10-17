"""blog_old URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from blog_old_project.views import article
from blog_old_project.views import comment_post
from blog_old_project.views import category
from blog_old_project.views import do_login
from blog_old_project.views import do_register
from blog_old_project.views import do_logout
from blog_old_project.views import archive
from blog_old_project.views import blog
from blog_old_project.views import blogs
from blog_old_project.views import signin
from blog_old_project.views import register
from blog_old_project.views import blog_edit
from blog_old_project.views import mark
from blog_old_project.views import reply_comment
from blog_old_project.views import article_add
from blog_old_project.views import article_post
from blog_old_project.upload import upload_image


urlpatterns = [
    url(r'^article/$', article, name='article'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'category/$', category, name='category'),
    url(r'login/$', do_login, name='login'),
    url(r'register/$', do_register, name='register'),
    url(r'logout/$', do_logout, name='logout'),
    url(r'archive/$', archive, name='archive'),
    url(r'mark/$', mark, name='mark'),
    url(r'reply_comment/$', reply_comment, name='reply_comment'),
    url(r'article_add/$', article_add, name='article_add'),
    url(r'article_post/$', article_post, name='article_post'),
    url(r'upload_image/', upload_image, name='upload_image'),
]
