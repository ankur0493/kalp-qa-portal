from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('qaportal.api.v1.urls')),
]

