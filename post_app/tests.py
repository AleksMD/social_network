from django.db.utils import IntegrityError
from django.test import TestCase, Client, tag
from user_app.models import User, UserProfile
from post_app.models import Post
import json
from datetime import date


class TestPostAPIViews(TestCase):
    db_many = True

    def setUp(self):
        self.client = Client()
        self.test_user_1 = User.objects.create_user(
            **{'username': 'test_username_1',
               'password': 'test_password',
               'email': 'test_1@gmail.com'})
        UserProfile.objects.create(user=self.test_user_1,
                                   email=self.test_user_1.email,
                                   first_name='test_1_first',
                                   last_name='test_1_last',
                                   date_of_birth=date.fromisoformat(
                                       '1990-01-01'))
        self.test_user_2 = User.objects.create_user(
            **{'username': 'test_username_2',
               'password': 'test_password',
               'email': 'test_2@gmail.com'})
        self.test_post_1 = Post.objects.create(author=self.test_user_1,
                                               title='Test post 1',
                                               content='Some test content 1')
        self.test_post_2 = Post.objects.create(author=self.test_user_1,
                                               title='Test post 2',
                                               content='Some test content 2')
        self.post_template = {'title': 'Test post template',
                              'content': 'Test post draft content'}

    @tag('post_list_auth')
    def test_post_list_view_auth(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                                 {'username': username,
                                                  'password': 'test_password'}
                                                       ),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        self.assertIn('access', resp_to_get_token.data)
        access_token = resp_to_get_token.data.get('access')
        response = self.client.get('/posts/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.json()[0]['title'],
                         self.test_post_1.title)
        self.assertEqual(response.json()[1]['title'],
                         self.test_post_2.title)
        self.assertEqual(response.json()[0]['author'],
                         self.test_post_1.author.username)
        self.assertEqual(response.json()[1]['author'],
                         self.test_post_2.author.username)
        self.assertEqual(response.json()[0]['content'],
                         self.test_post_1.content)
        self.assertEqual(response.json()[1]['content'],
                         self.test_post_2.content)

    @tag('post_list_unauth')
    def test_post_list_view_unauth(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIsNotNone(response.data['detail'])

    @tag('post_list_badjwt')
    def test_post_list_view_badjwt(self):
        access_token = 'some_invalid_custom_token'
        response = self.client.get('/posts/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
        self.assertIn('messages', response.data)

    @tag('post_detail_auth')
    def test_post_detail_view_auth(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                                 {'username': username,
                                                  'password': 'test_password'}
                                                       ),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        self.assertIn('access', resp_to_get_token.data)
        self.assertIn('refresh', resp_to_get_token.data)
        access_token = resp_to_get_token.data.get('access')
        response = self.client.get(f'/posts/{self.test_post_2.id}/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        title_from_resp = response.json().get('title')
        author_from_resp = response.json().get('author')
        content_from_resp = response.json().get('content')

        self.assertIsNotNone(title_from_resp)
        self.assertIsNotNone(author_from_resp)
        self.assertIsNotNone(content_from_resp)

        self.assertEqual(author_from_resp, self.test_post_2.author.username)
        self.assertEqual(title_from_resp, self.test_post_2.title)
        self.assertEqual(content_from_resp, self.test_post_2.content)

    @tag('post_detail_unauth')
    def test_post_detail_view_unauth(self):
        response = self.client.get('/posts/2/')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIsNotNone(response.data['detail'])

    @tag('post_detail_badjwt')
    def test_post_detail_view_badjwt(self):
        access_token = 'some_invalid_custom_token'
        response = self.client.get('/posts/2/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
        self.assertIn('messages', response.data)

    @tag('post_create_auth')
    def test_create_post_auth(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                                 {'username': username,
                                                  'password': 'test_password'}
                                                       ),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        self.assertIn('access', resp_to_get_token.data)
        self.assertIn('refresh', resp_to_get_token.data)
        acc_token = resp_to_get_token.data.get('access')
        response = self.client.post('/create_new_post/',
                                    self.post_template,
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 201)

    @tag('post_create_unauth')
    def test_create_post_unauth(self):
        response = self.client.post('/create_new_post/',
                                    self.post_template,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIsNotNone(response.data['detail'])

    @tag('post_without_author')
    def test_create_post_without_author(self):
        with self.assertRaises(IntegrityError):
            Post.objects.create(**self.post_template)

    @tag('user_likes_unlikes_post')
    def test_user_likes_post(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                                 {'username': username,
                                                  'password': 'test_password'}
                                                       ),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        acc_token = resp_to_get_token.data.get('access')
        post_list_resp = self.client.get(
            '/posts/', HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        post_id_1 = post_list_resp.json()[0]['url'].split('/')[-2]
        post_id_2 = post_list_resp.json()[1]['url'].split('/')[-2]
        response = self.client.get(f'/like/user/post/{post_id_1}/',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/like/user/post/{post_id_2}/',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 200)
        post_likes_1 = Post.objects.filter(
            id=post_id_1).first().users_likes.all()
        self.assertIsNotNone(post_likes_1)
        self.assertEqual(len(post_likes_1), 1)
        post_likes_2 = Post.objects.filter(
            id=post_id_2).first().users_likes.all()
        self.assertIsNotNone(post_likes_2)
        self.assertEqual(len(post_likes_2), 1)
        user_like_posts = User.objects.filter(
            username='test_username_1').first().user_profile.like_it.all()
        self.assertIsNotNone(user_like_posts)
        self.assertEqual(len(user_like_posts), 2)

        # In order ot avoid duplication both "like" and "unlike" features
        # are combined in one test. The following part checks "unlike" feature

        response = self.client.get(f'/unlike/user/post/{post_id_1}/',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/unlike/user/post/{post_id_2}/',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 200)
        post_likes_1 = Post.objects.filter(
            id=post_id_1).first().users_likes.all()
        self.assertIsNotNone(post_likes_1)
        self.assertEqual(len(post_likes_1), 0)
        post_likes_2 = Post.objects.filter(
            id=post_id_2).first().users_likes.all()
        self.assertIsNotNone(post_likes_2)
        self.assertEqual(len(post_likes_2), 0)
        user_like_posts = User.objects.filter(
            username='test_username_1').first().user_profile.like_it.all()
        self.assertIsNotNone(user_like_posts)
        self.assertEqual(len(user_like_posts), 0)
