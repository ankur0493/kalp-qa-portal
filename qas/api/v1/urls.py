from django.conf.urls import url

from .views import QuestionListView
urlpatterns = [
    url(r'^questions/', QuestionListView.as_view(), name="question-list"),
]
 
