"""scc URL Configuration

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
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    #url(r'^(?P<motion_id>[0-9]+)/$', views.m_detail, name='m_detail'),
    # ex: /polls/5/results/
    url(r'^motion/$', views.m, name='m'),
    # ex: /polls/5/vote/
    url(r'^door/$', views.d, name='d'),
    
    url(r'^motion/(?P<motion_id>[0-9]+)/$', views.m_detail, name='m_detail'),
    # ex: /polls/5/vote/
    url(r'^door/(?P<door_id>[0-9]+)/$', views.d_detail, name='d_detail'),
    ]

