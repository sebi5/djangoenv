# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from mongoengine import *

# Create your models here.

class Userdata(models.Model):
    user_id = models.TextField(max_length=600)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
