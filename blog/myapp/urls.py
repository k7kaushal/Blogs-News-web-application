from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    
    path('', views.home, name="blog-home"),
    path('blogserial/',views.blog_list),
    path('about/', views.about, name="blog-about"),
    path('news/', views.news, name="blog-news"),
    path('blogs/', views.blogs, name="blog-blogs"),
    path('register/', views.register, name="blog-register"),
    # path('login/', views.login, name="blog-login"),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),   
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='registration/passwordResetForm.html'), name = 'password_reset'),
    path('passwordResetDone/', auth_views.PasswordResetDoneView.as_view(template_name='registration/passwordResetDone.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/passwordResetConfirm.html'), name = 'password_reset_confirm'),
    path('resetDone/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/passwordResetComplete.html'), name = 'password_reset_complete'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('createblog/',views.createblog , name = 'createblog'),
    # re_path(r'^blog/(?P<pk>\d+)$', views.blogdetail, name='blogdetail'),
    path('<slug:slug>/', views.blogdetail, name='blogdetail'),
    path('blogs/<blog_id>/', views.blogdetailser, name='blog-detail'),
    path('editblog/<slug:slug>/', views.editblog, name='editblog'),
    path('delete/<blog_id>/', views.deleteblog, name='delete'),
    # path(r'^blogdetail/(?P<pk>\d+)$', views.blogdetail, name='blogdetail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)