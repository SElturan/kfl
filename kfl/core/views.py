from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, IntegerField
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.filters import OrderingFilter
from rest_framework import filters, generics, status, viewsets, mixins
from .models import Teams, Season,Players, Management , Standings, Matches, EventsMathes, SiteSettings, News, BestMoments, MatchLineup
from django.db.models import Q, Case, When, Value, IntegerField
from .serializers import TeamsSerializer, ManagementSerializer, TeamsDetailSerializer, PlayersSerializer, StandingsSerializer, PlayerDetailSerializer, MatchesSerializer, EventsMathesSerializer, SiteSettingsSerializer, NewsSerializer, \
    BestMomentsSerializer, MatchLineupSerializer
from django.utils.timezone import now


class TeamsModelViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'city']
    search_fields = ['name', 'city']
    ordering_fields = ['name', 'city']
    ordering = ['name']

    
    @action(detail=True, methods=['get'], url_path='detail', url_name='detail')
    def detail(self, request, pk=None):
        team = self.get_object()
        serializer = TeamsDetailSerializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='players', url_name='players')
    def players(self, request, pk=None):
        team = self.get_object()
        players = Players.objects.filter(team=team)
        
        grouped_players = {
            "forwards": PlayersSerializer(players.filter(position__icontains="Нападающий"), many=True).data,
            "midfielders": PlayersSerializer(players.filter(position__icontains="Полузащитник"), many=True).data,
            "defenders": PlayersSerializer(players.filter(position__icontains="Защитник"), many=True).data,
            "goalkeepers": PlayersSerializer(players.filter(position__icontains="Вратарь"), many=True).data,
            "management": ManagementSerializer(Management.objects.filter(team=team), many=True).data
        }

        response_data = {
            "team": TeamsSerializer(team).data,
            "players": grouped_players
        }

        return Response(response_data)
    
    @action(detail=True, methods=['get'], url_path='matches', url_name='matches')
    def matches(self, request, pk=None):
        team = self.get_object()
        current_season = Season.objects.filter(is_current=True).first()

        # Если текущий сезон не найден, возвращаем все матчи (сериализуем их)
        if not current_season:
            matches = Matches.objects.all()
        else:
            # Иначе, фильтруем матчи по команде и текущему сезону
            matches = Matches.objects.filter(Q(home_team=team) | Q(away_team=team), season=current_season)

        # Сериализуем данные и возвращаем их в Response
        serializer = MatchesSerializer(matches, many=True)
        return Response(serializer.data)



class PlayerDetailView(RetrieveAPIView):
    queryset = Players.objects.all()
    serializer_class = PlayerDetailSerializer


class StandingsListView(ListAPIView):
    serializer_class = StandingsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['season', 'tournament']

    def get_queryset(self):
        standings = Standings.objects.select_related('team', 'tournament')

        # Применяем вычисление разницы голов для каждой записи
        for standing in standings:
            standing.goals_difference = standing.goals_scored - standing.goals_conceded
            standing.save()  # Сохраняем разницу голов в базе данных

        return standings.order_by('-points', '-goals_difference')


class TeamMatchesView(ListAPIView):
    serializer_class = MatchesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament']
    ordering_fields = ['date_match']
    ordering = ['date_match']

    def get_queryset(self):

        team_id = self.kwargs.get('team_id')

        # Определяем текущий сезон
        current_season = Season.objects.filter(is_current=True).first()

        if not current_season:
            return Matches.objects.none()  # Если сезона нет, возвращаем пустой список

        # Фильтруем матчи текущего сезона
        queryset = Matches.objects.filter(season=current_season, home_team_id=team_id) | Matches.objects.filter(
            season=current_season, away_team_id=team_id
        )

        return queryset


class MatchListView(ListAPIView):
    serializer_class = MatchesSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tournament', 'round']
    ordering_fields = ['date_match']
    ordering = ['date_match']

    # Указываем базовый queryset
    queryset = Matches.objects.all()

    def get_queryset(self):
        # Получаем фильтры из запроса
        queryset = super().get_queryset()

        # Применяем дополнительные фильтры, если они есть
        tournament_id = self.request.query_params.get('tournament')
        round_id = self.request.query_params.get('round')

        if tournament_id:
            queryset = queryset.filter(tournament_id=tournament_id)

        if round_id:
            queryset = queryset.filter(round_id=round_id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Получаем общее количество команд в турнире
        total_teams = Teams.objects
        total_teams = total_teams.count()

        # Определяем количество матчей (половина от общего числа команд)
        max_matches = total_teams // 2

        # Хранение уже добавленных команд
        added_teams = set()
        matches_list = []

        for match in queryset:
            if match.home_team.id not in added_teams and match.away_team.id not in added_teams:
                matches_list.append(match)
                added_teams.add(match.home_team.id)
                added_teams.add(match.away_team.id)

                # Ограничиваем количество матчей
                if len(matches_list) >= max_matches:
                    break

        serializer = self.get_serializer(matches_list, many=True)
        return Response(serializer.data)

    

class MatchLineupListView(ListAPIView):
    serializer_class = MatchLineupSerializer

    def get_queryset(self):
        match_id = self.kwargs["match_id"]
        match = get_object_or_404(Matches, id=match_id)
        return MatchLineup.objects.filter(match=match)

    def list(self, request, *args, **kwargs):
        match_id = self.kwargs["match_id"]
        match = get_object_or_404(Matches, id=match_id)

        def get_team_lineup(team):
            starting = self.get_queryset().filter(team=team, is_starting=True)
            substitutes = self.get_queryset().filter(team=team, is_substitute=True)
            return {
                "starting": MatchLineupSerializer(starting, many=True).data,
                "substitutes": MatchLineupSerializer(substitutes, many=True).data
            }

        return Response({
            "match": f"{match.home_team.name} vs {match.away_team.name}",
            "date": match.date_match,
            "stadium": match.stadium,
            "status": match.status,
            "home_team": {
                "team_name": match.home_team.name,
                "lineup": get_team_lineup(match.home_team)
            },
            "away_team": {
                "team_name": match.away_team.name,
                "lineup": get_team_lineup(match.away_team)
            }
        })

class MatchEventsListView(ListAPIView):
    serializer_class = EventsMathesSerializer

    def get_queryset(self):
        match_id = self.kwargs.get('match_id')
        return EventsMathes.objects.filter(match_id=match_id).order_by('time')




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

class NewsDetailView(RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer