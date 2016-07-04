"""hungryapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import viewsets
from django.contrib import admin
from rest_framework.authtoken import views



urlpatterns = [
    url(r'^$', viewsets.api_root),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/$', viewsets.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', viewsets.UserDetail.as_view(), name='user-detail'),
    url(r'^groups/$', viewsets.GroupList.as_view(), name='group-list'),
    url(r'^groups/(?P<pk>[0-9]+)/$', viewsets.GroupDetail.as_view(), name='group-detail'),   
    url(r'^mentions/$', viewsets.MentionList.as_view(), name='mention-list'),
    url(r'^mentions/(?P<pk>[0-9]+)/$', viewsets.MentionDetail.as_view()),
    url(r'^reputations/$', viewsets.ReputationList.as_view(), name='reputation-list'),
    url(r'^reputations/(?P<pk>[0-9]+)/$', viewsets.ReputationDetail.as_view()),
    url(r'^favorites/$', viewsets.FavoriteList.as_view(), name='favorite-list'),
    url(r'^favorites/(?P<pk>[0-9]+)/$', viewsets.FavoriteDetail.as_view()),        
    url(r'^friends/$', viewsets.FriendList.as_view(), name='friend-list'),
    url(r'^friends/(?P<pk>[0-9]+)/$', viewsets.FriendDetail.as_view()),
    url(r'^places/$', viewsets.PlaceList.as_view(), name='place-list'),
    url(r'^places/(?P<pk>[0-9]+)/$', viewsets.PlaceDetail.as_view()),    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^tokens/$', viewsets.TokenList.as_view(), name='token-list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)