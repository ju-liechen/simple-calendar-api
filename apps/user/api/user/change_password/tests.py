from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from common.utils.tests import APIClient


class TestUserChangePassword(TestCase):
    def setUp(self):
        self.user = mixer.blend(get_user_model())
        self.password = mixer.faker.password()
        self.user.set_password(self.password)
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.url_name = reverse("api:user-change-password-post")

    def test_valid_post_user_change_password(self):
        new_password = mixer.faker.password()
        resp = self.client.post(self.url_name, data={
            'password': self.password,
            'new_password': new_password,
        })
        self.assertEqual(resp.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.check_password(new_password), True)
