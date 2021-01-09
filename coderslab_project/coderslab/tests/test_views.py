from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestView(TestCase):

    def test_register(self):
        path = reverse('register')
        response = self.client.post(path, {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password1': 'oknbji8(',
            'password2': 'oknbji8('
        })

        user1 = User.objects.get(username='user1')
        print(user1)
        assert user1.email == 'user1@gmail.com'

    def test_pipe_configurator_unauthenticated(self):
        path = reverse('coderslab-pipe_configurator')
        response = self.client.get(path)
        assert response.status_code == 302

    def test_pipe_configurator_authenticated(self):
        user = User.objects.create(
            username='testuser',
            password='qwerty1@'
        )
        self.client.force_login(user)
        response = self.client.get(reverse('coderslab-pipe_configurator'))
        assert response.status_code == 200
