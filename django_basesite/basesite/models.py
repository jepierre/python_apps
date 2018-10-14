#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'),
            ('published', 'Published'),
            )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.localtime(timezone.now()))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # the default manager
    published = PublishedManager() # my custom manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # for some reason, this was displayed in UTC, change it to localtime
        self.publish = localtime(self.publish)
        return reverse('basesite:post_detail', kwargs={'year': self.publish.year,
            'month':self.publish.month, 'day':self.publish.day, 'slug':self.slug})
