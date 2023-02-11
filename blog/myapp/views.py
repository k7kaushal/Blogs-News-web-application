from django.shortcuts import render, redirect
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login as login_User, logout as logout_User

def home(request):
    return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')

def news(request):
    return render(request, 'myapp/news.html')

def profile(request):
    return render(request, 'myapp/profile.html')

def blogs(request):
    context = {
        'blogs' : Blog.objects.all()
    }
    return render(request, 'myapp/blogs.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Accound created!')
            return redirect('blog-home')
    else:
        form = UserCreationForm()

    context = {
        'form' : form
    }
    return render(request, 'myapp/register.html', context)    

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']    
#         password = request.POST['password']
#         users = User.objects.filter(username=username).first()
#         if users is not None:
#             username = users.username
#             user =  authenticate(request, username=username, password=password)
#             if user is not None:
#                 login_User(request, user)
#                 return redirect("blog-home")
#             else:
#                 return render(request, 'myapp/home.html', {'message': "Invalid Credentials!"})
#         else:
#             return render(request, 'myapp/home.html', {'message': "Invalid Credentials!"})
#     return render(request, 'myapp/login.html')    

def logout(request):
    logout_User(request)
    messages.success(request, f'Logged out successfully!')
    return redirect(reverse("blog-home"))
