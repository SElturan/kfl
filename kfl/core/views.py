from rest_framework.response import Response
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Teams, Players, Standings, Matches, EventsMathes, SiteSettings, News, BestMoments
from django.db.models import Q, Case, When, Value, IntegerField
from .serializers import TeamsSerializer, PlayersSerializer, StandingsSerializer, PlayerDetailSerializer, MatchesSerializer, EventsMathesSerializer, SiteSettingsSerializer, NewsSerializer, BestMomentsSerializer


class TeamsListView(ListAPIView):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer


class TeamPlayersView(APIView):
    def get(self, request, team_id):
        team = get_object_or_404(Teams, id=team_id)
        players = Players.objects.filter(team=team)

        # Разделение игроков по позициям
        grouped_players = {
            "forwards": PlayersSerializer(players.filter(position__icontains="Нападающий"), many=True).data,
            "midfielders": PlayersSerializer(players.filter(position__icontains="Полузащитник"), many=True).data,
            "defenders": PlayersSerializer(players.filter(position__icontains="Защитник"), many=True).data,
            "goalkeepers": PlayersSerializer(players.filter(position__icontains="Вратарь"), many=True).data
        }

        response_data = {
            "team": TeamsSerializer(team).data,
            "players": grouped_players
        }

        return Response(response_data)


class StandingsListView(ListAPIView):
    serializer_class = StandingsSerializer

    def get_queryset(self):
        season = self.request.query_params.get('season', None)
        queryset = Standings.objects.all()

        if season:
            queryset = queryset.filter(season=season)

        return queryset.order_by('-points', '-goals_scored')

class MatchesByTeamView(ListAPIView):
    serializer_class = MatchesSerializer

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')  # Получаем ID команды из URL
        return Matches.objects.filter(Q(home_team_id=team_id) | Q(away_team_id=team_id)).order_by('-date_match')



class MatchesListView(ListAPIView):
    serializer_class = MatchesSerializer

    def get_queryset(self):
        return Matches.objects.all().order_by(
            Case(
                When(date_match__gte=timezone.now().date(), then=Value(0)),  # Будущие матчи
                default=Value(1),
                output_field=IntegerField(),
            ),
            "date_match",
        )

class MatchEventsListView(ListAPIView):
    serializer_class = EventsMathesSerializer

    def get_queryset(self):
        match_id = self.kwargs.get('match_id')
        return EventsMathes.objects.filter(match_id=match_id).order_by('time')

class PlayerDetailView(RetrieveAPIView):
    queryset = Players.objects.all()
    serializer_class = PlayerDetailSerializer


class SiteDataAPIView(APIView):
    def get(self, request):
        # Получаем настройки сайта (должна быть 1 запись)
        site_settings = SiteSettings.objects.first()
        site_data = SiteSettingsSerializer(site_settings).data if site_settings else {}

        # Последние 20 новостей
        latest_news = News.objects.order_by('-date')[:20]
        news_data = NewsSerializer(latest_news, many=True).data

        # Последние 5 лучших моментов
        latest_moments = BestMoments.objects.order_by('-date')[:5]
        moments_data = BestMomentsSerializer(latest_moments, many=True).data

        # 10 ближайших матчей (которые ещё не начались)
        upcoming_matches = Matches.objects.filter(date_match__gte=timezone.now().date()).order_by('date_match')[:10]
        matches_data = MatchesSerializer(upcoming_matches, many=True).data

        # Формируем общий JSON
        response_data = {
            "logo": site_data.get("logo", ""),
            "title": site_data.get("title", ""),
            "facebook": site_data.get("facebook_link", ""),
            "instagram": site_data.get("instagram_link", ""),
            "tiktok": site_data.get("tiktok_link", ""),
            "youtube": site_data.get("youtube_link", ""),
            "copyright": site_data.get("copy_right", ""),
            "upcoming_matches": matches_data,
            "news": news_data,
            "best_moments": moments_data
        }

        return Response(response_data)


class NewsListView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    