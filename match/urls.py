from django.urls import path

from match.views import StadiumCreateView, MatchCreateView, AddSeatsToStadiumView

urlpatterns = [
    path('stadiums/', StadiumCreateView.as_view(), name='stadium-create'),
    path('stadiums/<int:stadium_id>/seats/', AddSeatsToStadiumView.as_view(), name='add-seats'),
    path('matches/', MatchCreateView.as_view(), name='match-create'),
]
