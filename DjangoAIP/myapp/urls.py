# encoding:utf-8
"""
@author: DYS
@file: urls.py
@time: 2018/7/13 11:20
"""
# from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'myapp'
urlpatterns = [
    # path('', views.hello),
    url(r'^index/$', views.index),
    url(r'^upload/action/$', views.upload_action, name='upload_action'),
    # url(r'^article/(?P<article_id>\d+)$', views.article_page, name='article_page'),
    # url(r'^edit/(?P<article_id>\d+)$', views.edit_page, name='edit_page'),
    # url(r'^edit/action/$', views.edit_action, name='edit_action'),
]
