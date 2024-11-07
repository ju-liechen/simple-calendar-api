from functools import wraps
from ninja.errors import AuthenticationError


def permissions(*permission_checks):
    '''
    Use this as a decorator on a view to add permission checks
    eg.

    @api.get('/admin-only')
    @permissions(is_admin)
    def admin_only(request):
        return {'foo': 'bar'}

    If the check fails, a 401 will be returned.

    You can include as many permission checks as you want.

    args given to permissions should be functions that expect a request as the only
    argument, and they should return True if the request is allowed, and False if not.
    '''

    def decorator(func):
        @wraps(func)
        def newfunc(request, *args, **kwargs):
            for check in permission_checks:
                if not check(request):
                    raise AuthenticationError()
            return func(request, *args, **kwargs)
        return newfunc

    return decorator


def is_admin(request):
    user = getattr(request, 'user', None)
    if not user:
        return False
    return user.is_superuser
