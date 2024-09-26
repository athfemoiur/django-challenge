from django.urls import path

from match.views import StadiumCreateView, MatchCreateView

urlpatterns = [
    path('stadiums/', StadiumCreateView.as_view(), name='stadium-create'),
    path('matches/', MatchCreateView.as_view(), name='match-create'),
]
