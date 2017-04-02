from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from faker import Factory
from .models import BlogPost, Tag, Comment
from .factories import UserFactory, BlogPostFactory
from .services import register_user
faker = Factory.create()

# Create your tests here.


class TestIndexView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_method(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(200, response.status_code)

    def test_post_method(self):
        response = self.client.post(reverse('blog:index'))
        self.assertEqual(403, response.status_code)


class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_method(self):
        response = self.client.get(reverse('blog:login'))
        self.assertEqual(200, response.status_code)

    def test_login_with_unregistered_user(self):
        url = reverse('blog:login')
        response = self.client.post(url, data={'username': 'foo', 'password': 'bar'})
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('blog:login'), response.url)

    def test_login_with_registered_user(self):
        user = User.objects.create_user(username=faker.word(), password='cabbage')
        url = reverse('blog:login')
        username = user.username
        password = 'cabbage'
        response = self.client.post(url, data={'username': username,
                                               'password': password})
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('blog:profile'), response.url)

    def test_login_with_logged_user(self):
        user = User.objects.create_user(username=faker.word(), password='cabbage')
        url = reverse('blog:login')
        username = user.username
        password = 'cabbage'
        self.client.login(username=username, password=password)
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('blog:profile'), response.url)


class TestRegisterView(TestCase):

    def setUp(self):
        self.url = reverse('blog:register')
        self.client = Client()

    def test_get_method(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_register_with_registered_user(self):
        user = register_user({'username': faker.word(),
                              'password': 'cabbage'})
        username = user.username
        password = 'cabbage'
        response = self.client.post(self.url, data={'username': username,
                                                    'password': 'cabbage',
                                                    'email': 'foo@bar.com'})

        self.assertInHTML("<span>User already exists</span>", response.content.decode('utf-8'))

    def test_register_with_unregistered_user(self):
        count = User.objects.count()
        username = faker.word()
        password = 'cabbage'
        response = self.client.post(self.url, data={'username': username,
                                                    'password': 'cabbage',
                                                    'email': 'foo@bar.com'})

        self.assertEqual(count+1, User.objects.count())


class TestCreatePostView(TestCase):

    def setUp(self):
        self.url = reverse('blog:create-post')
        self.client = Client()
        self.username = faker.word()
        self.password = 'cabbage'

    def test_get_method_without_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_method_with_login(self):
        register_user({'username': self.username,
                       'password': self.password})
        self.client.login(username=self.username,
                          password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        register_user({'username': self.username,
                       'password': self.password})
        self.client.login(username=self.username,
                          password=self.password)
        response = self.client.post(self.url,
                                    data={'title': faker.word(),
                                          'content': faker.text(max_nb_chars=20)})
        post = BlogPost.objects.last()
        self.assertRedirects(response,
                             expected_url=reverse('blog:post-detail',
                                                  kwargs={'id': post.id}))


class TestCreateCommentView(TestCase):

    def setUp(self):
        self.username = faker.word()
        self.password = 'cabbage'
        self.user = register_user({'username': self.username,
                                   'password': self.password})
        self.post = BlogPostFactory(author=self.user)
        self.client = Client()
        self.url = reverse('blog:add-comment', kwargs={'id': self.post.id})

    def test_get_method(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('blog:post-detail', kwargs={'id': self.post.id}))

    def test_post_method(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data={'email': 'foo@bar.com',
                                                    'content': faker.text(max_nb_chars=20)})
        self.assertRedirects(response, reverse('blog:post-detail', kwargs={'id': self.post.id}))
