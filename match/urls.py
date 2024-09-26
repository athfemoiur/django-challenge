from django.urls import path

from match.views import StadiumCreateView, MatchCreateView, StadiumSeatsView, \
    MatchSeatsView, ReserveSeatView

urlpatterns = [
    path('stadiums/', StadiumCreateView.as_view(), name='stadium-create'),
    path('stadiums/<int:stadium_id>/seats/', StadiumSeatsView.as_view(), name='stadium-seats'),
    path('matches/', MatchCreateView.as_view(), name='match-create'),
    path('matches/<int:match_id>/seats/', MatchSeatsView.as_view(), name='match-seats'),
    path('matches/<int:match_id>/reserve/', ReserveSeatView.as_view(),
         name='reserve-seats'),
]
