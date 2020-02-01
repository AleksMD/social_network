from django.test import TestCase, Client, tag, override_settings
from user_app.models import User
import json


class TestEmailHunterApi(TestCase):

    def setUp(self):
        self.client = Client()
        self.email_with_acc_domain = 'test@close.io'
        self.test_user_1 = User.objects.create_user(
            **{'username': 'test_username_1',
               'password': 'test_password',
               'email': 'test_1@gmail.com'})

    @tag('send_valid_api_key')
    def test_email_with_valid_credentials(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                               {'username': username,
                                                'password': 'test_password'}),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        self.assertIn('access', resp_to_get_token.data)
        acc_token = resp_to_get_token.data.get('access')
        response = self.client.get('/verify_email/',
                                   {'email': self.email_with_acc_domain},
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = response.json().get('data')
        self.assertIsNotNone(data)
        self.assertIsNotNone(response.json().get('meta'))
        self.assertIn('email', data)
        self.assertIn('result', data)
        self.assertIn('score', data)
        self.assertIn('regexp', data)
        self.assertIn('gibberish', data)
        self.assertIn('disposable', data)
        self.assertIn('webmail', data)
        self.assertIn('mx_records', data)

    @tag('send_invalid_api_key')
    @override_settings(EMAILHUNTER_API_KEY='invalid_api_key')
    def test_email_with_invalid_credentials(self):
        username = self.test_user_1.username
        resp_to_get_token = self.client.post('/api/token/',
                                             json.dumps(
                                               {'username': username,
                                                'password': 'test_password'}),
                                             content_type='application/json')
        self.assertEqual(resp_to_get_token.status_code, 200)
        self.assertIn('access', resp_to_get_token.data)
        acc_token = resp_to_get_token.data.get('access')
        response = self.client.get('/verify_email/',
                                   {'email': self.email_with_acc_domain},
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {acc_token}')
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn('errors', data)
        self.assertEqual(len(data['errors']), 1)
        errors_descr = data['errors'][0]
        self.assertEqual(errors_descr['id'], 'authentication_failed')
        self.assertEqual(errors_descr['details'],
                         'No user found for the API key supplied')
        self.assertEqual(errors_descr['code'], 401)
