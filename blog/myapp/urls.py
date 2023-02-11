from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('news/', views.news, name="blog-news"),
    path('blogs/', views.blogs, name="blog-blogs"),
    path('register/', views.register, name="blog-register"),
    # path('login/', views.login, name="blog-login"),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
