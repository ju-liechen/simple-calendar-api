from django.contrib.auth import get_user_model
from ninja import Schema
from project.api import api
from pydantic import field_validator, EmailStr, SecretStr


PATH = '/public/user/signup'
NAME = 'public-signup'


class SignupIn(Schema):
    email: EmailStr
    password: SecretStr

    @field_validator('email')
    def validate_email(cls, email):
        email = email.lower().strip()
        if get_user_model().objects.filter(email=email).exists():
            raise ValueError('User with this email already exists')
        return email


class SignupOut(Schema):
    token: str


@api.post(PATH, url_name=f'{NAME}-post', auth=None, response=SignupOut)
def signup(request, data: SignupIn):
    user = get_user_model().objects.create_user(email=data.email)
    user.set_password(data.password.get_secret_value())
    user.save()
    return SignupOut(token=user.get_or_create_access_token())
