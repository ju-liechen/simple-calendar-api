from django.contrib.auth import authenticate
from ninja import Schema
from ninja.errors import ValidationError
from project.api import api
from pydantic import field_validator, EmailStr, SecretStr


PATH = '/public/user/login'
NAME = 'public-login'


class LoginIn(Schema):
    email: EmailStr
    password: SecretStr

    @field_validator('email')
    def clean_email(cls, email):
        return email.lower().strip()


class LoginOut(Schema):
    token: str


@api.post(PATH, url_name=f'{NAME}-post', auth=None, response=LoginOut)
def login_(request, data: LoginIn):
    user = authenticate(username=data.email, password=data.password.get_secret_value())

    if user:
        return LoginOut(token=user.get_or_create_access_token())

    raise ValidationError("Invalid credentials")
