from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.urls import reverse
from .helpers import *
from django.utils.timezone import now

# Create your models here.


class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content= FroalaField(null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='blog', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogModel, self).save(*args, **kwargs)   

    def get_absolute_url(self):
        return reverse('home', kwargs={'slug' : self.slug})


class Comments(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(BlogModel, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField('comment') 
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"comment by : { self.name}"