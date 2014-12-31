# -*- coding: utf-8 -*-
from django.db import models


class Task(models.Model):
    """Task that needs to be done."""
    description = models.CharField('What needs to be done?', max_length=255)
    is_checked = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_done = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.description
