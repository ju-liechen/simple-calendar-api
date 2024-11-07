from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from common.utils.tests import APIClient


class TestUserMyProfile(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email=mixer.faker.email())
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url_name = reverse("api:user-my-profile-get")

    def test_valid_get_user_my_profile(self):
        resp = self.client.get(self.url_name)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['id'], str(self.user.id))

    def test_valid_patch_user_my_profile(self):
        resp = self.client.patch(self.url_name, data={})
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        resp = self.client.patch(self.url_name, data={'email': 'changed@example.com'})
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['email'], 'changed@example.com')
