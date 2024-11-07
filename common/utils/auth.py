from django.contrib.auth import get_user_model
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token:
            user = get_user_model().objects.filter(access_token=token).first()
            if user:
                request.user = user
                return True
        return False
