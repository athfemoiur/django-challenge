from django.urls import path

from match.views import StadiumCreateView

urlpatterns = [
    path('stadiums/', StadiumCreateView.as_view(), name='stadium-create'),
]
