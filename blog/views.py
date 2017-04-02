from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.models import BlogPost, Comment, Tag
from blog.forms import CreatePostForm, CreateCommentForm, LoginForm, RegisterForm
from .services import register_user, create_post

# Create your views here.


def index_view(request, *args, **kwargs):
    if request.method == 'GET':
        all_tags = Tag.objects.all()
        if request.user.is_active:
            all_posts = BlogPost.objects.all()
        else:
            all_posts = BlogPost.objects.get_public_posts()
        return render(request, 'index.html', locals())
    else:
        return HttpResponse(status=403)


@login_required(login_url=reverse_lazy('blog:login'))
def create_post_view(request, *args, **kwargs):
    if request.method == 'GET':
        form = CreatePostForm()
    else:
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = create_post(request, form.cleaned_data)
            return redirect('blog:post-detail', id=post.id)
    return render(request, 'create_post.html', locals())


def post_detail_view(request, *args, **kwargs):
    pk = int(kwargs.get('id'))
    if request.method == 'GET':
        form = CreateCommentForm()
        post = BlogPost.objects.get(id=pk)
        comments = post.comments.all()
        tags = post.tags.all()
        return render(request, 'post_detail.html', locals())


def add_comment_view(request, *args, **kwargs):
    post_id = int(kwargs.get('id'))
    post = BlogPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            form.cleaned_data['post'] = post
            form.save()
    else:
        form = CreateCommentForm()
    return redirect('blog:post-detail', id=post_id)


def register_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                user = register_user(form.cleaned_data)
                return redirect('blog:login')
        except Exception as e:
            errors = "User already exists"
    else:
        form = RegisterForm()
    return render(request, 'register.html', locals())


def login_view(request, *args, **kwargs):
    if request.user.is_active is True:
        return redirect('blog:profile')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_authenticated():
                login(request, user)
                return redirect('blog:profile')
            else:
                return redirect('blog:login')
    else:
        form = LoginForm()
    return render(request, 'login.html', locals())


@login_required(login_url=reverse_lazy('blog:login'))
def profile_view(request, *args, **kwargs):
    user = request.user
    return render(request, 'profile.html', locals())


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('blog:login')
