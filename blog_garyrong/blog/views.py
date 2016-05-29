# coding:utf-8
import logging
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from django.db.models import F
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from blog_garyrong.settings import PAGE_NUM, RECENTLY_NUM, HOT_NUM, LIKE_MOST_NUM
from models import Post, Page, Category, Widget
from ipware.ip import get_real_ip, get_ip
from utils.cache import cache
import json
logger = logging.getLogger(__name__)


class BaseMixin(object):

    def get_context_data(self, *args, **kwargs):
        if 'object' in kwargs or 'query' in kwargs:
            context = super(BaseMixin, self).get_context_data(**kwargs)
        else:
            context = {}

        try:
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(RECENTLY_NUM)
            context['hot_posts'] = Post.get_hots_posts(HOT_NUM)
            context['tag_lists'] = Post.gather_tags()
            context['like_most_posts'] = Post.get_most_like_posts(LIKE_MOST_NUM)
            context['pages'] = Page.objects.filter(status=0)
        except Exception as e:
            logger.exception(u'加载基本信息出错[%s]！', e)

        return context

class IndexView(BaseMixin, ListView):
    query = None
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        '''A base view for displaying a list of objects'''
        try:
            self.cur_page = int(request.GET.get('page', 1))
        except TypeError:
            self.cur_page = 1
        if self.cur_page <= 0:
            self.cur_page = 1
        # will call get_queryset and get_context_data functions in sequence
        return super(IndexView, self).get(request, *args, **kwargs)
    def get_queryset(self):
        """
            Get the list of items for this view. This must be an iterable, and may
            be a queryset (in which qs-specific behavior will be enabled).
        """
        self.query = self.request.GET.get('s') # obtain search keywords
        if self.query:
            query_set = (
                Q(title__icontains = self.query) |
                Q(content__icontains = self.query)
            )
            posts = Post.objects.defer('content').filter(query_set, status = 0)
            # TODO make search keywords marked
        else:
            # defer load the content
            posts = Post.objects.defer('content').filter(status = 0)
        return posts
    def get_context_data(self, **kwargs):
        """
            Get the context for this view
        """
        paginator = Paginator(self.object_list, PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        return super(IndexView, self).get_context_data(**kwargs)

class CategoryListView(IndexView):
    def get_queryset(self):
        alias = self.kwargs.get('alias')
        try:
            self.category = Category.objects.get(alias = alias)
        except Category.DoesNotExist:
            return []

        self.query = self.request.GET.get('s')
        if self.query:
            query_set = (
                Q(content__icontains = self.query) |
                Q(title__icontains = self.query)
            )
            posts = self.category.p_category.defer('content').\
                    filter(query_set, status = 0)
        else:
            posts = self.category.p_category.defer('content').filter(status = 0)
        return posts

    def get_context_data(self, **kwargs):
        """
            Get the context for this view
        """
        if hasattr(self, 'category'):
            kwargs['title'] = ' | ' + self.category.name
        return super(CategoryListView, self).get_context_data(**kwargs)

class TagsListView(IndexView):
    def get_queryset(self):
        self.tag = self.kwargs.get('tag')
        self.query = self.request.GET.get('s')
        if self.query:
            query_set = (
                Q(title__icontains = self.query) |
                Q(content__icontains = self.query)
            )
            posts = Post.objects.defer('content').filter(query_set,tags__icontains = self.tag, status = 0)
        else:
            posts = Post.objects.defer('content').filter(tags__icontains = self.tag, status = 0)
        return posts
    def get_context_data(self, **kwargs):
        if hasattr(self, 'tag'):
            kwargs['title'] = ' | ' + self.tag
        return super(TagsListView, self).get_context_data(**kwargs)


class PostDetailView(BaseMixin, DetailView):
    object = None
    template_name = "post_detail.html"
    queryset = Post.objects.filter(status = 0)
    slug_field = 'alias'
    def get(self, request, *args, **kwargs):
        """
            A base view for displaying a single object
        """
        alias = self.kwargs.get('slug').replace(' ', '')
        try:
            self.object = self.queryset.get(alias = alias)
        except Post.DoesNotExist:
            referer = request.META.get("HTTP_REFERER")
            logger.error(u'ref[%s]访问不存在的文章：[%s]', referer, alias)
            context = super(PostDetailView, self).get_context_data(**kwargs)
            return render(request, '404.html', context)
        ip = get_real_ip(request)
        if ip is None:
            ip = get_ip(request)
        visited_ips = cache.get(self.object.id, [])
        if ip not in visited_ips:
            Post.objects.filter(id=self.object.id).update(view_times = F('view_times') + 1)
            visited_ips.append(ip)
            # set timeout a hour
            cache.set(self.object.id, visited_ips, 24 * 60)

        context = self.get_context_data(object = self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context

def rate_handler(request):
    if request.method == 'GET' and request.is_ajax():
        pid = request.GET.get('pid', None)
        incre = request.GET.get('incre')
        if pid:
            try:
                post = Post.objects.get(pk=int(pid))
                if incre == 'true':
                    post.like_times = post.like_times + 1
                else:
                    post.like_times = post.like_times - 1
                post.save()
                return HttpResponse(json.dumps({'status':200, 'like_times' : post.like_times}))
            except Post.DoesNotExist:
                return HttpResponse(json.dumps({'status': 404}))
    return HttpResponse(json.dumps({'status': 403}))


