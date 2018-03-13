# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class BBS(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    summury = models.CharField(max_length=256, blank=True, null=True)
    category = models.ForeignKey('Category')
    author = models.ForeignKey('BBS_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    ranking = models.IntegerField()
    view_count=  models.IntegerField()

    def __unicode__(self):
        return self.category.name

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    administrator = models.ForeignKey('BBS_user')

    def __unicode__(self):
        return self.name

class BBS_user(models.Model):
    user = models.OneToOneField(User)
    signature = models.CharField(max_length=128, default='This guy is too lazy to levave anything here.')
    potho = models.ImageField(upload_to='', default='', null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Profile(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pictures')

    def __unicode__(self):
        return self.name


# Create your models here.
