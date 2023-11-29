from transliterate import translit
from django.db import models
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from taggit.models import TagBase, ItemBase
from taggit.managers import TaggableManager
from autoslug import AutoSlugField
from unidecode import unidecode


class Like(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Dislike(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='dislikes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Mark(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='marks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        """Класс для хранения состояния статуса поста"""
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    tags = TaggableManager()
    title = models.CharField(max_length=250)
    slug = AutoSlugField(max_length=50, populate_from='title', unique=True)
    body = models.TextField()
    # photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_post')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PUBLISHED)
    likes = GenericRelation(Like)
    dislikes = GenericRelation(Dislike)
    marks = GenericRelation(Mark)

    class Meta:
        ordering = ['-publish']   # сортировка в обратном порядке
        indexes = [
            models.Index(fields=['-publish']),   # добавляем индексацию
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_slug': self.slug})

    def show_comments(self):
        return reverse('comments', kwargs={'post_id': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        ordering = ['created']

    indexes = [
        models.Index(fields=['created']),
    ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'





