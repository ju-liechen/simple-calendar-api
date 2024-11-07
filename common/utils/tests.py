from django.test import Client
import json


class APIClient(Client):
    """
    Extend Django test Client to
    - handle JSON data
    - add force_authenticate function

    """
    def post(self, path, data=None, **extra):
        if data is not None:
            data = json.dumps(data)
            extra['content_type'] = 'application/json'
        return super().post(path, data, **extra)

    def put(self, path, data=None, **extra):
        if data is not None:
            data = json.dumps(data)
            extra['content_type'] = 'application/json'
        return super().put(path, data, **extra)

    def patch(self, path, data=None, **extra):
        if data is not None:
            data = json.dumps(data)
            extra['content_type'] = 'application/json'
        return super().patch(path, data, **extra)

    def force_authenticate(self, user):
        '''
        Automatically include authentication header for the provided user
        If no user is provided the request will not be authenticated

        '''
        if user:
            self.defaults['HTTP_AUTHORIZATION'] = f'Bearer {user.get_or_create_access_token()}'
        else:
            del self.defaults['HTTP_AUTHORIZATION']
