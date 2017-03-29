from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .models import BlogPost, Tag


def register_user(cleaned_data):
    username = cleaned_data.get('username')
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')
    user = User.objects.create_user(username, email, password)
    user.is_active = True
    return user


def create_post(request, cleaned_data):
    user = get_user(request)
    title = cleaned_data.get('title')
    content = cleaned_data.get('content')
    tags = cleaned_data.get('tags')
    post = BlogPost(title=title, content=content, author=user)
    post.save()
    post = BlogPost.objects.get(title=title)
    for tag in tags:
        post.tags.add(tag)
    return post
