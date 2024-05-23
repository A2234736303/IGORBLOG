from django.urls import path,include
from . import views


urlpatterns = [
    path('login', views.iglogin, name='login'),
    path('logout', views.iglogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
]
