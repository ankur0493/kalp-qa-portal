from rest_framework import generics, pagination

from qas.models import Question
from .permissions import TentantAPIKeyPermission
from .serializers import QuestionSerializer
from .throttling import TenantRateThrottle

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (TentantAPIKeyPermission, )
    throttle_classes = (TenantRateThrottle, )
    queryset = Question.objects.exclude(private=True)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Question.objects.exclude(private=True).order_by('id')
        query = self.request.query_params.get("q", "")
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
