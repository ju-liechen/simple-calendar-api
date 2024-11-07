from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
import uuid
from ninja.errors import ValidationError
from ninja import Schema
from pydantic import SecretStr

from project.api import api


PATH = '/public/user/forgot-password-step-2'
NAME = 'public-user-forgot-password-step-2'


class ForgotPasswordStep2In(Schema):
    token: SecretStr
    password: SecretStr
    user_id: uuid.UUID


class ForgotPasswordStep2Out(Schema):
    pass


@api.post(
    PATH,
    auth=None,
    url_name=f'{NAME}-post',
    response=ForgotPasswordStep2Out
)
def public_user_forgot_password_step_2_post(request, data: ForgotPasswordStep2In):
    user = get_user_model().objects.get(id=data.user_id)
    if not default_token_generator.check_token(user, data.token.get_secret_value()):
        raise ValidationError('Invalid token')

    user.set_password(data.password.get_secret_value())
    user.save()
    return {}
