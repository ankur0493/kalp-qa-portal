from rest_framework import generics

from qas.models import Question
from .permissions import TentantAPIKeyPermission
from .serializers import QuestionSerializer


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (TentantAPIKeyPermission, )
    queryset = Question.objects.exclude(private=True)
