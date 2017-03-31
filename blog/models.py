from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .querysets import BlogPostQuerySet

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField()
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag,
                                  related_name='posts',
                                  blank=True)
    is_private = models.BooleanField(default=False)

    objects = BlogPostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_updated_at = timezone.now()
        super().save(self, *args, **kwargs)


class Comment(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    post = models.ForeignKey(BlogPost, related_name='comments')

    def __str__(self):
        return 'Comment on post {} by {}'.format(self.post.id, self.email)
