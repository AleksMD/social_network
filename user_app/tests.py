from django.test import TestCase, Client, tag
from user_app.models import User, UserProfile
import json
from datetime import date
from django.core import serializers


class TestUserAPIViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user_1 = User.objects.create_user(
            **{'username': 'test_username_1',
               'password': 'test_password',
               'email': 'test_1@gmail.com'})
        self.test_user_2 = User.objects.create_user(
            **{'username': 'test_username_2',
               'password': 'test_password',
               'email': 'test_2@gmail.com'})
        self.test_user_3 = {'username': 'test_username_3',
                            'password': 'test_password',
                            'email': 'test_3@gmail.com'}

    @tag('signup_valid')
    def test_user_signup_valid(self):
        response = self.client.post('/signup/',
                                    self.test_user_3,
                                    content_type='application/json')
        message = 'You have been successfully registered'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('success'), 'True')
        self.assertEqual(response.data.get('message'), message)

    @tag('signup_invalid')
    def test_user_signup_invalid(self):
        self.test_user_3.pop('password')
        response = self.client.post('/signup/',
                                    self.test_user_3,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @tag('login_valid')
    def test_user_login_valid(self):
        response = self.client.post('/login/',
                                    {'username': self.test_user_1.username,
                                     'password': self.test_user_1.password},
                                    content_type='application/json')
        message = 'You have been successfully logged in'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('success'), 'True')
        self.assertEqual(response.data.get('message'), message)

    @tag('login_invalid')
    def test_user_login_invalid(self):
        response = self.client.post('/login/',
                                    {'username': self.test_user_3['username'],
                                     'password': self.test_user_3['password']},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])

    @tag('user_list_auth')
    def test_user_list_view_auth(self):
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
        UserProfile.objects.create(user=self.test_user_2,
                                   email=self.test_user_2.email,
                                   first_name='test_2_first',
                                   last_name='test_2_last',
                                   date_of_birth=date.fromisoformat(
                                       '1980-02-03'))
        UserProfile.objects.create(user=self.test_user_1,
                                   email=self.test_user_1.email,
                                   first_name='test_1_first',
                                   last_name='test_1_last',
                                   date_of_birth=date.fromisoformat(
                                       '1990-01-01'))
        response = self.client.get('/users/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    @tag('user_list_unauth')
    def test_users_list_view_unauth(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIsNotNone(response.data['detail'])

    @tag('user_list_badjwt')
    def test_user_list_view_badjwt(self):
        access_token = 'some_invalid_custom_token'
        UserProfile.objects.create(user=self.test_user_2,
                                   email=self.test_user_2.email,
                                   first_name='test_2_first',
                                   last_name='test_2_last',
                                   date_of_birth=date.fromisoformat(
                                       '1980-02-03'))
        UserProfile.objects.create(user=self.test_user_1,
                                   email=self.test_user_1.email,
                                   first_name='test_1_first',
                                   last_name='test_1_last',
                                   date_of_birth=date.fromisoformat(
                                       '1990-01-01'))
        response = self.client.get('/users/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
        self.assertIn('messages', response.data)

    @tag('user_detail_auth')
    def test_user_detail_view_auth(self):
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
        UserProfile.objects.create(user=self.test_user_2,
                                   email=self.test_user_2.email,
                                   first_name='test_2_first',
                                   last_name='test_2_last',
                                   date_of_birth=date.fromisoformat(
                                       '1980-02-03'))
        UserProfile.objects.create(user=self.test_user_1,
                                   email=self.test_user_1.email,
                                   first_name='test_1_first',
                                   last_name='test_1_last',
                                   date_of_birth=date.fromisoformat(
                                       '1990-01-01'))
        user_list_resp = self.client.get(
            '/users/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        user_id_2 = user_list_resp.json()[1]['url'].split('/')[-2]

        response = self.client.get(f'/users/{user_id_2}/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 200)

        email_from_resp = response.json().get('email')
        first_name_from_resp = response.json().get('first_name')
        last_name_from_resp = response.json().get('last_name')

        profile_1 = UserProfile.objects.filter(user=self.test_user_2).first()
        profile_1_json = json.loads(serializers.serialize('json', [profile_1]))
        email_from_db_profile = profile_1_json[0]['fields']['email']
        first_name_from_db_profile = profile_1_json[0]['fields']['first_name']
        last_name_from_db_profile = profile_1_json[0]['fields']['last_name']

        self.assertIsNotNone(email_from_resp)
        self.assertIsNotNone(first_name_from_resp)
        self.assertIsNotNone(last_name_from_resp)

        self.assertEqual(email_from_resp, email_from_db_profile)
        self.assertEqual(first_name_from_resp, first_name_from_db_profile)
        self.assertEqual(last_name_from_resp, last_name_from_db_profile)

    @tag('user_detail_unauth')
    def test_user_detail_view_unauth(self):
        response = self.client.get('/users/2/')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIsNotNone(response.data['detail'])

    @tag('user_detail_badjwt')
    def test_user_detail_view_badjwt(self):
        access_token = 'some_invalid_custom_token'
        response = self.client.get('/users/2/',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
        self.assertIn('messages', response.data)
