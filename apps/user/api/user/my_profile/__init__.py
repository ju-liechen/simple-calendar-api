import uuid
from ninja import Schema
from typing import Optional
from pydantic import EmailStr

from project.api import api


PATH = '/user/my-profile'
NAME = 'user-my-profile'


class MyProfileOut(Schema):
    id: uuid.UUID
    email: EmailStr


class MyProfileIn(Schema):
    email: EmailStr


class MyProfileUpdateIn(Schema):
    email: Optional[str] = None


@api.get(PATH, url_name=f"{NAME}-get", response=MyProfileOut)
def user_my_profile_get(request):
    return request.user


@api.patch(PATH, url_name=f"{NAME}-patch", response=MyProfileOut)
def user_my_profile_patch(request, data: MyProfileUpdateIn):
    user = request.user
    for (key, value) in data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    user.save()
    return user
