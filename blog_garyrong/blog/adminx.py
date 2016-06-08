#coding:utf-8
from django.contrib import admin
import xadmin
from django.core import urlresolvers
from models import Post, Category, Page, Widget, Media
import datetime
import markdown2

class PostAdmin(object):
    search_fields = ('title', 'alias')
    fields = ('content', 'summary', 'title', 'alias', 'tags', 'status',
              'category', 'is_top', 'pub_time', 'image', 'attachment', 'like_times')
    list_display = ('preview', 'title', 'category', 'is_top', 'pub_time')
    list_display_links = ('title', )

    ordering = ('-pub_time', )
    list_per_page = 15
    save_on_top = True

    def preview(self, obj):
        url_edit = urlresolvers.reverse('xadmin:blog_post_change', args=(obj.id,))
        return u'''
                    <span><a href="/post/%s/" target="_blank">预览</a></span>
                    <span><a href="%s" target="_blank">编辑</a></span>
                ''' % (obj.alias, url_edit)

    preview.short_description = u'操作'
    preview.allow_tags = True

    def save_models(self):
        obj = self.new_obj
        obj.author = self.request.user
        if not obj.summary:
            obj.summary = obj.content
        obj.content_html = markdown2.markdown(obj.content, extras = ['code-color', 'footnotes', 'tables', 'wiki-tables', 'fenced-code-blocks', 'cuddled-lists'])
        obj.save()

class CategoryAdmin(object):
    search_fields = ('name', 'alias')
    list_display = ('name', 'rank', 'is_nav', 'status', 'create_time')

class PageAdmin(object):
    search_fields = ('name', 'alias')
    fields = ('title', 'alias', 'link', 'content', 'is_html', 'status', 'rank')
    list_display = ('title', 'link', 'rank', 'status', 'is_html')

    def save_models(self):
        obj = self.new_obj
        obj.author = self.request.user
        obj.save()

class WidgetAdmin(object):
    search_fields = ('name', 'alias')
    fields = ('title', 'content', 'rank', 'hide')
    list_display = ('title', 'rank', 'hide')

class PostImageInline(object):
    fields = ('image',)

xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Page, PageAdmin)
xadmin.site.register(Widget, WidgetAdmin)
xadmin.site.register(Media, PostImageInline)
