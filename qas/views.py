from __future__ import unicode_literals

from django.core.cache import cache
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import User, Question, Answer, Tenant

class IndexView(TemplateView):

    template_name = "qas/index.html"
    cache_format = 'throttle_%(ident)s'
    cache_throttled_access_format = 'throttled_access_%(ident)s'

    def get_cache_key(self, api_key, access_type='full'):
        ident = api_key
        return (self.cache_format % {'ident': ident} if access_type=='full'
                else self.cache_throttled_access_format % {'ident': ident})

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['num_users'] = User.objects.all().count()
        context['num_questions'] = Question.objects.all().count()
        context['num_answers'] = Answer.objects.all().count()
        tenant_api_access_count = {}
        for tenant in Tenant.objects.all():
            key = self.get_cache_key(tenant.api_key, access_type='full')
            throttled_access_key = self.get_cache_key(tenant.api_key, access_type='throttled')
 
            history = cache.get(key, [])
            throttled_access_history = cache.get(throttled_access_key, [])
            tenant_api_access_count[tenant.name] = len(history) + len(throttled_access_history)
        context['tenant_api_access_count'] = tenant_api_access_count
        return context

