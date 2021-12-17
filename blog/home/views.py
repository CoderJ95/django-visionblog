from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.core.paginator import Paginator
# Create your vipaews here.


def home(request):
    return render(request, 'home.html')

def user_register(request): 
    if request.user.is_authenticated:
        return redirect('add_blog')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            email = request.POST.get('email')
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('repassword')
            if pass1 != pass2:
                messages.warning(request, 'password does not match')
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.warning(request, 'username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'email already taken')
                return redirect('register')
            else:    
                user = User.objects.create_user(username=name, email=email, password=pass1,)
                user.save()
                messages.success(request, 'User has been Registered successfully')
                return redirect('login')
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            return redirect('add_blog')
        else:
            messages.info(request, 'Username OR Password is incorrect')
            return redirect('login')

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')




def blog(request):
    blogs = BlogModel.objects.all()
    p = Paginator(blogs, 3)
    page = request.GET.get('page')
    pages = p.get_page(page) 

    context = {'blogs':blogs, 'pages': pages }
    return render(request, 'blog.html', context)


def blog_details(request, slug):
    try:
        blog_obj = BlogModel.objects.get(slug=slug) 
        comments = Comments.objects.filter(post=blog_obj)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comments(name=form.cleaned_data['name'],comment=form.cleaned_data['comment'],post=blog_obj)
                comment.save()
                return redirect('blog_details' + blog_obj.slug )
        else:
            form = CommentForm()        
    except Exception as e:
        print(e) 

    context = {'blog_obj' : blog_obj, 'form': form,  'comments': comments}    
    return render(request, 'blog_details.html', context)


@login_required(login_url='login')
def add_blog(request):
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            user = request.user
            if form.is_valid():
                content = form.cleaned_data['content']
                title = form.cleaned_data['title']
                image = form.cleaned_data['image']
            BlogModel.objects.create(user = user, title=title, content=content, image=image)
            messages.success(request, 'Your Blog Posted Successfully')
            return redirect('add_blog')
    except Exception as e:
        print(e)   

    context = {'form': BlogForm}         
    return render(request, 'add_blog.html', context)


@login_required(login_url='login')
def see_blog(request):
    context= {}
    try:
        blog_obj = BlogModel.objects.filter(user = request.user)
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e) 
    return render(request, 'see_blog.html',context)


def blog_delete(request, id):
    blog_obj = BlogModel.objects.get(id = id)
    if blog_obj.user == request.user:
        blog_obj.delete()
    return redirect('see_blog')


def blog_update(request, slug):
    blog_obj = get_object_or_404(BlogModel, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST,instance=blog_obj)
        if form.is_valid():
            form.save()
            return redirect('see_blog')
    else:
        form = BlogForm(instance=blog_obj)

    return render(request,'blog_update.html', {'form':form})