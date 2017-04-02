from django.core.management.base import BaseCommand
from ...factories import TagFactory, BlogPostFactory, UserFactory, CommentFactory


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Generating tags")
        tags = []
        for i in range(5):
            tag = TagFactory()
            tags.append(tag)
            print('.')

        print("Generating users")
        for i in range(3):
            UserFactory()
            print('.')

        print("Generating posts")
        for i in range(10):
            BlogPostFactory(tags=tags)
            print('.')

        print("Generating comments")
        for i in range(20):
            CommentFactory()
            print('.')

        print("Seeding complete")
