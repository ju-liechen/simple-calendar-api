from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from mixer.backend.django import mixer

from common.utils.tests import APIClient
from common.utils.encode import base64_to_dict


class TestPublicUserForgotPasswordStep1(TestCase):
    def setUp(self):
        self.email = mixer.faker.email()
        self.user = mixer.blend(get_user_model(), email=self.email)
        self.client = APIClient()
        self.url = reverse("api:public-user-forgot-password-step-1-post")
        self.url_step2 = reverse("api:public-user-forgot-password-step-2-post")

    @patch('apps.mail.models.Mail.send')
    def test_user_can_reset_password(self, mock_send):
        new_password = 'whatever'
        response = self.client.post(self.url, data={'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, 200)

        email_values = mock_send.mock_calls[0]
        data = base64_to_dict(email_values[-1]['reset_url'].split('?state=')[-1])
        token = data['token']

        response = self.client.post(
            self.url_step2,
            data={'token': token, 'user_id': str(self.user.id), 'password': new_password},
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(new_password))

    @patch('apps.mail.models.Mail.send')
    def test_user_can_request_password_icase(self, mock_send):
        create_email = 'USER@example.com'
        reset_email = 'user@EXAMPLE.com'
        get_user_model().objects.create_user(email=create_email, password='secret')
        response = self.client.post(self.url, data={'email': reset_email})
        self.assertEqual(response.status_code, 200)
