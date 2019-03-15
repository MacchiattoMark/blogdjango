# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name='文章标题')
    body = models.TextField(verbose_name='文章正文')
    create_time = models.DateTimeField(verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='文章摘要')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类id')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签id')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-create_time']
