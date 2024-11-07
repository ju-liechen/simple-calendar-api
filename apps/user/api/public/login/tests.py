from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from common.utils.tests import APIClient


class TestPublicLogin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = mixer.faker.password()
        self.user = mixer.blend(get_user_model())
        self.user.set_password(self.password)  # mixer.blend doesnt set password
        self.user.save()

    def test_valid_public_login(self):
        resp = self.client.post(reverse("api:public-login-post"), data={
            "email": self.user.email,
            "password": self.password
        })
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual('', data['token'])
