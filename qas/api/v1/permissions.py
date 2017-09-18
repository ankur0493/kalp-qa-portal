from rest_framework import permissions

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from qas.models import Tenant


class TentantAPIKeyPermission(permissions.BasePermission):

    API_KEY_HEADER = 'X-Api-Key'

    def header_canonical(self, header_name):
        """Translate HTTP headers to Django header names."""
        # Translate as stated in the docs:
        # https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest.META
        return 'HTTP_%s' % header_name.replace('-', '_').upper()

    def fetch_user_data(self, api_key):
        try:
            return Tenant.objects.get(api_key=api_key)
        except Tenant.DoesNotExist:
            return None

    def has_permission(self, request, view):
        # Check for API key header.
        api_key_header = self.header_canonical(self.API_KEY_HEADER)
        api_key = request.META.get(api_key_header)
        if not api_key:
            return False

        # Fetch credentials for API key from the data store.
        try:
            user = self.fetch_user_data(api_key)
            if user:
                return True
        except TypeError:
            return False
        return False
