from django.contrib import admin
from .models import BlogModel, Comments

# Register your models here.

admin.site.register((BlogModel, Comments))