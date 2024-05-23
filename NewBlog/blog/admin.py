from django.contrib import admin
from .models import Blog, BlogComment, BlogCategory


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'pub_time', 'category', 'author']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'author', 'content', 'pub_time']


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)
