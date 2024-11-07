import json
from django.http import HttpRequest
from humps import camelize, decamelize


class RequestWrapper:
    def __init__(self, request: HttpRequest, modified_data: dict):
        self._request = request
        self._modified_data = modified_data

    def __getattr__(self, item):
        return getattr(self._request, item)

    @property
    def body(self):
        return json.dumps(self._modified_data).encode('utf-8')


def camel_case_middleware(get_response):

    def middleware(request):

        # snake_case incoming json data
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf8'))
            request = RequestWrapper(request, decamelize(data))

        response = get_response(request)

        # camelCase outgoing json data
        if 'application/json' in response['Content-Type']:
            data = json.loads(response.content)
            camel_cased_data = camelize(data)  # Convert data keys to camelCase
            response.content = json.dumps(camel_cased_data)

        return response

    return middleware
