from django.conf import settings
from django.contrib import admin
from django.urls import path

from .api import api


admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_HEADER


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
