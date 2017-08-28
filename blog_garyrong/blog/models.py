# coding:utf-8
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from blog_garyrong import settings
from utils.cache import cache_decorator

STATUS = {
    0: u'正常',
    1: u'草稿',
    2: u'删除',
}

class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'名称')
    alias = models.CharField(max_length=40, verbose_name=u'英文名')

    is_nav = models.BooleanField(default=False, verbose_name=u'是否在导航位置显示')

    parent = models.ForeignKey('self', default=None, blank=True, null=True, verbose_name=u'上级分类')
    desc = models.CharField(max_length=100, blank=True, verbose_name=u'描述', help_text=u'点击分类之后显示')

    rank = models.IntegerField(default=0, verbose_name=u'展示排序')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name=u'状态')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __unicode__(self):
        if self.parent:
            return '%s:%s' % (self.parent, self.name)
        else:
            return '%s' % (self.name)

    @classmethod
    @cache_decorator(1*60)
    def available_list(cls):
        return cls.objects.filter(status=0)

    class Meta:
        ordering = ['rank', '-create_time']
        verbose_name_plural = verbose_name = u"分类"

    def related_post_number(self):
        return len(self.p_category.all())

    def get_absolute_url(self):
        return "/category/%s/" % self.alias


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name=u'作者')
    category = models.ForeignKey(Category, verbose_name=u'分类', related_name = 'p_category')

    title = models.CharField(max_length=100, verbose_name=u'标题')
    alias = models.CharField(max_length=100, db_index=True, blank=True, null=True, verbose_name=u'英文标题', help_text=u'做伪静态url用', unique = True)
    is_top = models.BooleanField(default=False, verbose_name=u'置顶')

    summary = models.TextField(verbose_name=u'摘要')
    # TODO convert to markdown format
    content = models.TextField(verbose_name = u'正文', help_text = markdown_allowed())
    content_html = models.TextField(verbose_name=u'文章正文html')

    view_times = models.IntegerField(default = 1)
    like_times = models.IntegerField(default = 0)
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'标签', help_text=u'用英文逗号分割')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name=u'状态')

    pub_time = models.DateTimeField(default=datetime.now, verbose_name=u'发布时间')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    image = models.ImageField(upload_to = "images/", blank = True, verbose_name = u"标题图")
    attachment = models.FileField(upload_to = "attachments/", blank = True, verbose_name = u"附件")


    def __unicode__(self):
        return self.title

    def tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip() != '']

    def get_absolute_url(self):
        return '%s/post/%s/' % (settings.DOMAIN, self.alias)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


    @cached_property
    def next_post(self):
        # 下一篇
        return Post.objects.filter(id__gt=self.id, status=0).order_by('id').first()

    @cached_property
    def prev_post(self):
        # 前一篇
        return Post.objects.filter(id__lt=self.id, status=0).first()

    @classmethod
    @cache_decorator(1*60)
    def get_recently_posts(cls, num):
        return cls.objects\
            .filter(status=0).order_by('-create_time')[:num]

    @classmethod
    @cache_decorator(1*60)
    def gather_tags(cls, num = None):
        posts = cls.objects.filter(status = 0)
        tags_list = []
        for post in posts:
            tags_list = tags_list + [t for t in post.tags_list() if t not in tags_list]
        if num is None:
            return tags_list
        return tags_list[:num]

    @classmethod
    @cache_decorator(1*60)
    def get_hots_posts(cls, num):
        return cls.objects\
            .filter(status=0).order_by('-view_times')[:num]

    @classmethod
    @cache_decorator(1*60)
    def get_most_like_posts(cls, num):
        return cls.objects\
                .filter(status = 0).order_by('-like_times')[:num]

    # TODO more precision
    @cache_decorator(3*60)
    def related_posts(self):
        related_posts_list = None
        try:
            related_posts_list = Post.objects.filter(tags__icontains=self.tags_list()[0]).\
                exclude(id=self.id)[:10]
        except IndexError:
            pass

        if not related_posts_list:
            related_posts_list = Post.objects.filter(category=self.category).\
                exclude(id=self.id)[:10]

        return related_posts_list

    class Meta:
        ordering = ['-is_top', '-pub_time', '-create_time']
        verbose_name_plural = verbose_name = u"文章"


class Page(models.Model):
    author = models.ForeignKey(User, verbose_name=u'作者')
    title = models.CharField(max_length=100, verbose_name=u'标题')

    alias = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'英文标题', help_text=u'做伪静态url用')
    content = models.TextField(verbose_name=u'page正文')
    content_html = models.TextField(verbose_name = u'page正文html')
    is_html = models.BooleanField(default=False, verbose_name=u'html代码')

    link = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'链接', help_text=u'该链接存在时其它内容无效')

    rank = models.IntegerField(default=1, verbose_name=u'排序', help_text=u'从右到左的顺序')
    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name=u'状态')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-rank', '-create_time']
        verbose_name_plural = verbose_name = u"页面"


class Widget(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')

    content = models.TextField(verbose_name=u'widget内容', help_text=u'html代码不会被转义')
    hide = models.BooleanField(default=False, verbose_name=u'隐藏')

    rank = models.IntegerField(default=0, verbose_name=u'展示排序')

    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    def __unicode__(self):
        return self.title

    @classmethod
    @cache_decorator(1*60)
    def available_list(cls):
        return cls.objects.filter(hide=False)

    class Meta:
        ordering = ['rank', '-create_time']
        verbose_name_plural = verbose_name = u"侧栏组件"

class Media(models.Model):
    image = models.ImageField(upload_to = 'media/')

    def __unicode__(self):
        return self.image.name
    class Meta:
        verbose_name_plural = verbose_name = u"资源文件"
