from django.db import models


class BlogPostQuerySet(models.QuerySet):

    def get_public_posts(self):
        return self.filter(is_private=False)
 
