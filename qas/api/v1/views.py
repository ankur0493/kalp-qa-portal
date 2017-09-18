from rest_framework import generics

from qas.models import Question
from .permissions import TentantAPIKeyPermission
from .serializers import QuestionSerializer
from .throttling import TenantRateThrottle

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (TentantAPIKeyPermission, )
    throttle_classes = (TenantRateThrottle, )
    queryset = Question.objects.exclude(private=True)

    def get_queryset(self):
        queryset = Question.objects.exclude(private=True)
        query = self.request.query_params.get("q", "")
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
