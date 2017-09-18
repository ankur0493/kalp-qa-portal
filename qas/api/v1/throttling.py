from rest_framework import throttling
from django.conf import settings


class TenantRateThrottle(throttling.SimpleRateThrottle):
    """
    A simple cache implementation that throttles the API access by a tenant to
    a specified rate after the tenant has achieved unthrottled API access for a
    specified rate.
    """
    cache_format = 'throttle_%(ident)s'
    cache_throttled_access_format = 'throttled_access_%(ident)s'
    THROTTLED_ACCESS_DURATIONS = settings.DEFAULT_THROTTLED_ACCESS_DURATIONS
    scope = 'tenant'

    def get_cache_key(self, request, view, access_type='full'):
        ident = request.TENANT.api_key
        return (self.cache_format % {'ident': ident} if access_type=='full'
                else self.cache_throttled_access_format % {'ident': ident})

    def get_throttled_access_duration(self, request):
        return self.THROTTLED_ACCESS_DURATIONS[self.scope]

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.
        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view, access_type='full')
        if self.key is None:
            return True

        self.throttled_access_key = self.get_cache_key(request, view, access_type='throttled')

        self.history = self.cache.get(self.key, [])
        self.throttled_access_history = self.cache.get(self.throttled_access_key, [])
        self.now = self.timer()
        self.throttled_access_duration = self.get_throttled_access_duration(request)
        print(self.throttled_access_history)
        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        while self.throttled_access_history and self.throttled_access_history[-1] <= self.now - self.throttled_access_duration:
            self.throttled_access_history.pop()

        if len(self.history) >= self.num_requests:
            if self.throttled_access_history and self.throttled_access_history[-1] >= self.now - self.throttled_access_duration:
                return self.throttle_failure()
            return self.throttle_success(access_type='throttled')
        return self.throttle_success(access_type='full')

    def throttle_success(self, access_type='full'):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        if access_type=='full':
            history = self.history
            key = self.key
            duration = self.duration
        else:
            history = self.throttled_access_history
            key = self.throttled_access_key
            duration = self.throttled_access_duration
        history.insert(0, self.now)
        self.cache.set(key, history, duration)
        return True

    def wait(self):
        """
        Returns the recommended next request time in seconds.
        """
        if self.throttled_access_history:
            remaining_duration = self.throttled_access_duration - (self.now - self.throttled_access_history[-1])
        else:
            remaining_duration = self.throttled_access_duration

        available_requests = self.num_requests - len(self.throttled_access_history) + 1
        if available_requests <= 0:
            return None

        return remaining_duration / float(available_requests)
