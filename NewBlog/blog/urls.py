from django.urls import path, include
from . import views
from django.contrib import admin

app_name = 'blog'

urlpatterns = [
    path('blog/detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('blog/pub', views.pub_blog, name='pub_blog'),
    path('', views.index, name='index'),
    path('auth/', include('igauth.urls')),
    path('admin/', admin.site.urls),
    path('blog/comment/pub',views.pub_comment,name='pub_comment'),
    path('search',views.search,name='search'),
]
