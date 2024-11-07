from ninja import Schema
from pydantic import field_validator, SecretStr
from project.api import api


PATH = '/user/change-password'
NAME = 'user-change-password'


class ChangePasswordIn(Schema):
    password: SecretStr
    new_password: SecretStr

    @field_validator('password')
    def validate_password(cls, password, info):
        user = info.context['request'].user
        if user.check_password(password.get_secret_value()):
            return password
        raise ValueError('Incorrect password')


class ChangePasswordOut(Schema):
    pass


@api.post(PATH, url_name=f"{NAME}-post", response=ChangePasswordOut)
def user_change_password_post(request, data: ChangePasswordIn):
    request.user.set_password(data.new_password.get_secret_value())
    request.user.save()
    return {}
