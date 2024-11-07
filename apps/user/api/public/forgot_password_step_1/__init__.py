from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from ninja import Schema
from pydantic import EmailStr
from project.api import api
from apps.user import mail


PATH = "/public/user/forgot-password-step-1"
NAME = "public-user-forgot-password-step-1"


class ForgotPasswordStep1In(Schema):
    email: EmailStr


class ForgotPasswordStep1Out(Schema):
    pass


@api.post(PATH, auth=None, url_name=f'{NAME}-post', response=ForgotPasswordStep1Out)
def public_user_forgot_password_step_1_post(request, data: ForgotPasswordStep1In):
    try:
        user = get_user_model().objects.get(email=data.email)
    except get_user_model().DoesNotExist:
        return {}

    reset_token = default_token_generator.make_token(user)
    mail.send_forgot_password_email(user, reset_token=reset_token)

    return {}
