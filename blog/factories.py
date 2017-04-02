import factory
from faker import Factory
from .models import BlogPost, Tag, Comment
from django.contrib.auth.models import User

faker = Factory.create()


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda _: faker.word())


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    password = 'cabbage'
    username = factory.LazyAttribute(lambda _: faker.word())
    email = factory.Sequence(lambda n: '{}@test.com'.format(faker.word()))


class BlogPostFactory(factory.DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.LazyAttribute(lambda _: faker.word())
    content = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=20))
    author = factory.Iterator(User.objects.all())

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    email = factory.Sequence(lambda n: '{}@test.com'.format(faker.word()))
    content = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=20))
    post = factory.Iterator(BlogPost.objects.all())
