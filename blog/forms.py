from django import forms
from blog.models import BlogPost, Comment, Tag


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('created_at', 'last_updated_at', 'author')

    def save(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        tags = self.cleaned_data.get('tags')
        author = kwargs.get('author')
        BlogPost.objects.create(title=title,
                                content=content,
                                tags=tags,
                                author=author)


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('created_at', 'post')

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        post = self.cleaned_data.get('post')
        content = self.cleaned_data.get('content')
        Comment.objects.create(email=email, content=content, post=post)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128)
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
