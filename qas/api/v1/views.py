from rest_framework import generics

from qas.models import Question
from .serializers import QuestionSerializer


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.exclude(private=True)
