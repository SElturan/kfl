from django.contrib import admin
from .models import Teams, Players, Matches, EventsMathes, StaticticsPlayerSeason, Standings

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stadium', 'coach', 'founded_year')
    search_fields = ('name', 'city', 'coach')
    list_filter = ('founded_year',)

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team', 'position', 'number', 'nationality', 'goals', 'assists')
    search_fields = ('first_name', 'last_name', 'team__name', 'position')
    list_filter = ('team', 'position', 'nationality')

@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date_match', 'home_goals', 'away_goals', 'status')
    search_fields = ('home_team__name', 'away_team__name', 'stadium')
    list_filter = ('status', 'date_match')

@admin.register(EventsMathes)
class EventsMathesAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'event', 'time')
    search_fields = ('match__home_team__name', 'match__away_team__name', 'player__first_name', 'player__last_name')
    list_filter = ('event',)

@admin.register(StaticticsPlayerSeason)
class StaticticsPlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ('player', 'season', 'goals', 'assists', 'yellow_cards', 'red_cards')
    search_fields = ('player__first_name', 'player__last_name', 'season')
    list_filter = ('season',)

@admin.register(Standings)
class StandingsAdmin(admin.ModelAdmin):
    list_display = ('team', 'season', 'games', 'wins', 'draws', 'losses', 'points')
    search_fields = ('team__name', 'season')
    list_filter = ('season',)
