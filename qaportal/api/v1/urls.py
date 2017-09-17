from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('qas.api.v1.urls')),
]

