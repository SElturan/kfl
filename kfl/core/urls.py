from django.urls import path
from .views import TeamsListView, TeamPlayersView, StandingsListView, MatchesByTeamView, MatchesListView, MatchEventsListView, PlayerDetailView, \
SiteDataAPIView, NewsListView, NewsDetailView

urlpatterns = [
    path('api/teams/', TeamsListView.as_view(), name='teams-list'),
    path('api/team/<int:team_id>/players/', TeamPlayersView.as_view(), name='team-players'),
    path('api/standings/', StandingsListView.as_view(), name='standings-list'),
    path('api/matches/', MatchesListView.as_view(), name='matches-list'),
    path('api/matches/team/<int:team_id>/', MatchesByTeamView.as_view(), name='matches-by-team'),
    path('api/matches/<int:match_id>/events/', MatchEventsListView.as_view(), name='match-events'),
    path("api/players/<int:pk>/", PlayerDetailView.as_view(), name="player-detail"),
    path("api/site/", SiteDataAPIView.as_view(), name="site-data"),
    path("api/news/", NewsListView.as_view(), name="news-list"),
    path("api/news/<int:pk>/", NewsDetailView.as_view(), name="news-detail"),

]
