"""blog_garyrong URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import settings
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

from blog.views import (IndexView, PostDetailView, CategoryListView,
                        TagsListView, rate_handler)

urlpatterns = [
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^$', IndexView.as_view(), name='homepage'),
    url(r'^post/(?P<slug>[\w|\-|\d|\W]+?)/$', PostDetailView.as_view()),
    url(r'^category/(?P<alias>\w+)/', CategoryListView.as_view()),
    url(r'^tag/(?P<tag>[\w|\.|\-]+)/$', TagsListView.as_view()),
    url(r'^rate_url/$', rate_handler),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
