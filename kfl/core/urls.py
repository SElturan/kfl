from django.urls import path
from django.urls.conf import include
from .views import TeamsModelViewSet, StandingsListView, TeamMatchesView, MatchListView, MatchEventsListView, PlayerDetailView, \
SiteDataAPIView, NewsListView, NewsDetailView, MatchLineupListView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'teams', TeamsModelViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/standings/', StandingsListView.as_view(), name='standings-list'),
    path('api/matches/', MatchListView.as_view(), name='matches-list'),
    path('api/matches/team/<int:team_id>/', TeamMatchesView.as_view(), name='matches-by-team'),
    path('api/matches/<int:match_id>/events/', MatchEventsListView.as_view(), name='match-events'),
    path("api/players/<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("api/site/", SiteDataAPIView.as_view(), name="site-data"),
    path("api/news/", NewsListView.as_view(), name="news-list"),
    path("api/news/<int:pk>/", NewsDetailView.as_view(), name="news-detail"),
    path("api/matches/<int:match_id>/lineup/", MatchLineupListView.as_view(), name="match-lineup")

]
