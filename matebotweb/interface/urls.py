'''
Created on 18/12/2015

@author: zuao
'''
from django.conf.urls import patterns, url
from interface import views

urlpatterns = patterns('',
        url(r'^$', views.main_page),
)