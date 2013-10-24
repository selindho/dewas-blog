from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class EditBlogLoggedOutTest(TestCase):

    def test_logged_out_action(self):
        c = Client()
        response = c.get('/editblog/1/')
        self.assertEqual(response.status_code, 302)


class EditBlogLoggedInTest(TestCase):

    def setUp(self):
        User.objects.create_user('test_user', 'test_email@test.com', 'test_password')

    def test_logged_in_action(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.get('/editblog/1/')
        self.assertEqual(response.status_code, 200)