from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from common.utils.tests import APIClient


class TestPublicSignup(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_public_signup(self):
        email = mixer.faker.email()
        resp = self.client.post(reverse("api:public-signup-post"), data={
            "email": email,
            "password": "password"
        })
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual('', data['token'])
