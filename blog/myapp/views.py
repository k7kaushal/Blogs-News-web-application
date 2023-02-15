from django.shortcuts import render, redirect
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import requests
from django.contrib.auth import authenticate, login as login_User, logout as logout_User
API = '83e6f3fa3c09418a8c5d624482df5c25'


from django.http import JsonResponse
from .models import Blog
from .serializers import BlogSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def blog_list(request, format=None):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many = True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def blogdetailser(request, blog_id=None, format=None):
    try:
        blog = Blog.objects.get(id = blog_id)
        print(blog.title)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BlogSerializer(blog, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return render(request, 'myapp/detailedblog.html')


def home(request):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        data = []
        if title:
            url = f'https://newsapi.org/v2/top-headlines?q={title}&apiKey={API}'
            response = requests.get(url)
            data = response.json()
            articles = data['articles']
        print(len(articles))
        if len(articles) == 0: 
            messages.info(request, f'No results for you search')
        context = {
            'articles' : articles,
            'count1' : articles
        }
        return render(request, 'myapp/news.html', context)
    try:
        url = f'https://newsapi.org/v2/everything?q=Apple&from=2023-02-14&sortBy=popularity&apiKey={API}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
        author = request.user
        context = {
            'articles' : articles,
            'Userblogs' : Blog.objects.filter(author = author),
        }
        return render(request, 'myapp/news.html', context)
    except:
        url = f'https://newsapi.org/v2/everything?q=Apple&from=2023-02-14&sortBy=popularity&apiKey={API}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
        context = {
            'articles' : articles,
            'blogs' : Blog.objects.all(),
        }
        return render(request, 'myapp/home.html', context)

def about(request):
    return render(request, 'myapp/about.html')

def news(request):
    url = f'https://newsapi.org/v2/everything?q=Apple&from=2023-02-14&sortBy=popularity&apiKey={API}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
            'articles' : articles,
    }
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        data = []
        if title:
            url = f'https://newsapi.org/v2/top-headlines?q={title}&apiKey={API}'
            response = requests.get(url)
            data = response.json()
            articles = data['articles']
        print(len(articles))
        if len(articles) == 0: 
            messages.info(request, f'No results for you search')
        context = {
            'articles' : articles,
            'count1' : articles
        }
        return render(request, 'myapp/news.html', context)
    return render(request, 'myapp/news.html', context)

def profile(request):
    author = request.user
    context = {
        'blogs' : Blog.objects.filter(author = author).count,
    }
    return render(request, 'myapp/profile.html', context)

def blogs(request, format=None):
    author = request.user
    context = {
        'blogs' : Blog.objects.all(),
        'Userblogs' : Blog.objects.filter(author = author),
        'Userblogssize' : Blog.objects.filter(author = author).count,
    }
    return render(request, 'myapp/blogs.html', context)

# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Accound created!')
#             return redirect('blog-home')
#     else:
#         form = UserCreationForm()

#     context = {
#         'form' : form
#     }
#     return render(request, 'myapp/register.html', context)   
# 

def register(request):
    if request.method == 'POST':

        err_lst = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        hashed_password = make_password(password1)
        # users = User.objects.all()
        if len(password1)<9:
            messages.error(request, f'Password must be atleast 8 characters long!')
            err_lst.append("Check Password length")
        if(password1 != password2):
            messages.error(request, f'Passwords not Matching!')
            err_lst.append("Passwords not Matching!")
            print("Got data1")
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Account with this Username already exist.')
            err_lst.append("Account with this Username already exist.")
            print("Got data2")
        if User.objects.filter(email=email).exists():
            messages.error(request, f'This Email is Already linked to an existing Account.')
            err_lst.append("This Email is Already linked to an existing Account.")
            print("Got data3")

        if len(err_lst) == 0:
            print("Got data4")
            u1 = User(username = username, email= email, password = hashed_password)
            u1.save()
            print("User created successfully")
            messages.success(request, f'Accound created!')
            return redirect ('blog-home')
        else:
            return render(request, 'myapp/register.html', {'err_lst': err_lst})

    else:
        return render (request, 'myapp/register.html')

    return render(request, 'myapp/register.html')   



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

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')    
        password = request.POST.get('password')
        users = User.objects.filter(username = username).first()
        if users is not None:
            username = users.username
            user =  authenticate(request, username=username, password=password)
            if user is not None:
                print("user is not none true")
                login_User(request, user)
                return redirect('blog-home')
            else:
                print("error message wala")
                messages.success(request, f'Invalid Credentials!')
                return render(request, 'myapp/login.html')
        else:
            messages.success(request, f'Invalid Credentials!')
            return render(request, 'myapp/login.html')
    else:
        return render(request, 'myapp/login.html')

def logout(request):
    logout_User(request)
    messages.success(request, f'Logged out successfully!')
    return redirect(reverse("blog-home"))

def createblog(request, format=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user

        if Blog.objects.filter(title = title).exists():
            messages.error(request, f'A Blog with this title already exists!')
            return render (request, 'myapp/createblog.html')
        else:
            messages.success(request, f'Blog Uploaded')
            b1 = Blog(author = author, title=title, content=content)
            b1.save()
            return redirect('blog-blogs')
    return render(request, 'myapp/createblog.html')

def editblog(request, slug, format=None):
    b1 = Blog.objects.get(slug = slug)
    context = {'blog' : b1}
    old_title = b1.title
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user

        if ((old_title != title) and (Blog.objects.filter(title = title).exists())):
            messages.error(request, f'A Blog with this title already exists!')
            return render (request, 'myapp/editblog.html', context)
        else:
            messages.success(request, f'Blog Uploaded')
            b1.title = title
            b1.content = content
            b1.slug = slug + 'updated'
            # b1 = Blog(author = author, title=title, content=content)
            b1.save()
            return redirect('blog-blogs')
    return render(request, 'myapp/editblog.html', context)

def blogdetail(request, slug, format=None):
    context = {
        'blog' : Blog.objects.get(slug = slug),
        'user' : request.user
    }
    return render(request, 'myapp/detailedblog.html', context)

def deleteblog(request, blog_id=None, format=None):
    b1 =  Blog.objects.get(id = blog_id)
    b1.delete()
    messages.info(request, f"Blog deleted!")
    return redirect('blog-blogs')

