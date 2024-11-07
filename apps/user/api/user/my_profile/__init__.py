from django.contrib.auth import get_user_model
from ninja import Schema
from typing import Optional
from pydantic import EmailStr, field_validator
from uuid import UUID

from project.api import api

PATH = '/user/my-profile'
NAME = 'user-my-profile'


class MyProfileOut(Schema):
    id: UUID
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool


class MyProfileIn(Schema):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('email')
    def validate_email(cls, email):
        if get_user_model().objects.filter(email__iexact=email.lower()).exists():
            raise ValueError("User with email already exists")
        return email.lower()


@api.get(PATH, url_name=f"{NAME}-get", response=MyProfileOut)
def user_my_profile_get(request):
    return request.user


@api.patch(PATH, url_name=f"{NAME}-patch", response=MyProfileOut)
def user_my_profile_patch(request, data: MyProfileIn):
    user = request.user
    for (key, value) in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    user.save()
    return user
