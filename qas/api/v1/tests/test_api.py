from __future__ import absolute_import, unicode_literals, print_function

import json
import time

from django.core.management import call_command

from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from qas.models import Question, Answer, Tenant, User


class QuestionAPITestCase(APITestCase):
    def setUp(self):
        super(QuestionAPITestCase, self).setUp()
        call_command('loaddata', 'questions', 'answers', 'user', 'tenant', verbosity=0)
        self.questions_url = reverse("questions-list")
        self.tenant = Tenant.objects.all()[0]
        headers = {'HTTP_X_API_KEY': self.tenant.api_key}
        self.client.credentials(**headers)


    def test_throttle(self):
        """
        API requests should be throttled to 1 request per 10 seconds after first 100 requests of the day
        """
        for i in range(101):
            response = self.client.get(self.questions_url) 
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        time.sleep(10)
        response = self.client.get(self.questions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized(self):
        client = APIClient()
        response = client.get(self.questions_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_api_response(self):
        self.assertTrue( Question.objects.count() > 0 )
        self.assertTrue( Answer.objects.count() > 0 )

        response = self.client.get(self.questions_url)
        related_keys = [f.get_accessor_name() for f in Question._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete]
        resp = json.loads(response.content)

        page_number_pagination_keys = ('count', 'next', 'previous', 'results')
        self.assertEqual(set(resp.keys()), set(page_number_pagination_keys))

        nitems = Question.objects.exclude(private=True).count()
        self.assertEqual( resp.get('count', 0), nitems )

        results = resp.get('results', [])
        self.assertEqual(len(results), nitems)

        for question_data in results:
             question_id = question_data['id']
             question = Question.objects.get(id=question_id)
             self._compare_api_response(question_data, question, related_keys)
             for k, v in question_data.iteritems():
                 if k in related_keys:
                     for related_data in v:
                         related_id = related_data['id']
                         obj = getattr(question, k).get(id=related_id)
                         self._compare_api_response(related_data, obj, related_keys, related=True)

    def _compare_api_response(self, data, obj, related_keys={}, related=False):
       for k, v in data.iteritems():
           if not related and k in related_keys:
               continue
           val = getattr(obj, k, None)
           if k == 'user_name':
               val = getattr(obj.user, 'first_name', '') + getattr(obj.user, 'last_name', '')
           elif k in ('user_id', ):
               v = int(v)
           self.assertEqual(v, val)

