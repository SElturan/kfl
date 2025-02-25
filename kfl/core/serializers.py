from rest_framework import serializers
from .models import Teams,Management ,Players, Standings, Matches, EventsMathes, StaticticsPlayerSeason, SiteSettings, News, BestMoments, MatchLineup


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['id','name', 'logo', 'city']


class TeamsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['id','name', 'logo', 'city', 'stadium', 'coach', 'founded_year', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'clean_sheets', ]


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = ['id', 'team', 'first_name', 'last_name', 'position', 'photo']


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields = ['id', 'first_name', 'last_name', 'position', 'number', 'nationality', 'goals', 'assists']

class PlayerDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    team_name = serializers.CharField(source="team.name")
    team_id = serializers.IntegerField(source="team.id")
    team_logo = serializers.CharField(source="team.logo")

    class Meta:
        model = Players
        fields = [
            "id", "full_name", "team_name", "team_id", "team_logo","photo", "birth_date", "position", "number",
            "height", "weight", "nationality", "goals", "assists", "yellow_cards",
            "red_cards", "games", "minutes"
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StandingsSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_logo = serializers.CharField(source='team.logo', read_only=True)
    calculated_goals_difference = serializers.IntegerField(read_only=True)

    class Meta:
        model = Standings
        fields = ['id', 'tournament', 'season', 'team_name', 'team_logo', 'season', 'games', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'calculated_goals_difference','points']


class MatchesSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    home_team_logo = serializers.CharField(source='home_team.logo', read_only=True)
    away_team_logo = serializers.CharField(source='away_team.logo', read_only=True)

    class Meta:
        model = Matches
        fields = ['id','tournament', 'season', 'round', 'home_team_logo', 'away_team_logo', 'home_team_name', 'away_team_name', 'date_match', 'home_goals', 'away_goals', 'stadium', 'status', 'mvp']

class MatchLineupSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.name", read_only=True)

    class Meta:
        model = MatchLineup
        fields = ["id", "player_name"]

class EventsMathesSerializer(serializers.ModelSerializer):
    player_name = serializers.SerializerMethodField()
    match_info = serializers.SerializerMethodField()

    class Meta:
        model = EventsMathes
        fields = ['id', 'match_info', 'player_name', 'event', 'time']

    def get_player_name(self, obj):
        return f"{obj.player.first_name} {obj.player.last_name}"

    def get_match_info(self, obj):
        return f"{obj.match.home_team.name} vs {obj.match.away_team.name} - {obj.match.date_match}"


class StaticticsPlayerSeasonSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source="player.__str__")

    class Meta:
        model = StaticticsPlayerSeason
        fields = [
            'tournament', 'season', "player_name", "season", "goals", "assists", "yellow_cards",
            "red_cards", "games", "minutes"
        ]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['logo', 'title', 'facebook_link', 'instagram_link', 'tiktok_link', 'youtube_link', 'copy_right']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'image', 'title', 'text', 'date']


class BestMomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestMoments
        fields = ['id', 'title', 'description', 'link_moments', 'date']
