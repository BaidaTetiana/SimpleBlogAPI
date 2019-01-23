# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Post(models.Model):
	name = models.TextField(null=False, default='')
	full_text = models.TextField(null=False, default='')
	picture = models.TextField(null=False, default='')
	added_url= models.TextField(null=False, default='')
	created_at = models.DateTimeField(null=False, auto_now_add=True, blank=True)
	user_id = models.ForeignKey(User, null=False, default=1)
	likes = models.IntegerField(null=False, default=0)

	class Meta:
		db_table = u'posts'
