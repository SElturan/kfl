from django.contrib import admin
from .models import Teams, Management, Players, Season, Tournament, \
    Round, Matches, MatchLineup, EventsMathes, \
        StaticticsPlayerSeason, SeasonAwards, Standings, \
            SiteSettings, News, BestMoments, Sponsor, CompanyInfo, Judge
# Для модели Teams
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'stadium', 'coach', 'founded_year')
    search_fields = ('name', 'city')
    list_filter = ('city',)

# Для модели Management
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'position', 'team')
    search_fields = ('first_name', 'last_name', 'position')
    list_filter = ('position',)

# Для модели Players
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'team', 'position', 'number', 'games', 'goals', 'assists', 'yellow_cards', 'red_cards')
    search_fields = ('first_name', 'last_name', 'team__name')
    list_filter = ('team', 'position', 'games', 'goals', 'yellow_cards')

# Для модели Tournament
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id','name','country')
    search_fields = ('name', 'country')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id','year', 'is_current', 'start_date', 'end_date')
    search_fields = ('year',)
    list_filter = ('is_current',)


# Для модели Round
class RoundAdmin(admin.ModelAdmin):
    list_display = ('id','tournament', 'season', 'round_number')
    search_fields = ('tournament__name', 'season__year')
    list_filter = ('tournament', 'season')

# Для модели Matches
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id','tournament', 'season', 'home_team', 'away_team', 'date_match','time_match', 'status', 'home_goals', 'away_goals', 'stadium', 'documents')
    search_fields = ('tournament__name', 'home_team__name', 'away_team__name')
    list_filter = ('tournament', 'season', 'status', 'home_team', 'away_team')

# Для модели MatchLineup
class MatchLineupAdmin(admin.ModelAdmin):
    list_display = ('id','match', 'team', 'player', 'is_starting', 'is_substitute')
    search_fields = ('match__tournament__name', 'player__first_name', 'player__last_name')
    list_filter = ('match', 'team', 'is_starting', 'is_substitute')

class EventsMathesAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'player', 'event', 'time')
    search_fields = ('match__tournament__name', 'player__first_name', 'player__last_name', 'event')
    list_filter = ('match', 'event')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "match":
            # Фильтруем только матчи со статусом "В процессе"
            kwargs['queryset'] = Matches.objects.filter(status="В процессе")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Для модели StaticticsPlayerSeason
class StaticticsPlayerSeasonAdmin(admin.ModelAdmin):
    list_display = ('id','player', 'tournament', 'season', 'goals', 'assists', 'yellow_cards', 'red_cards', 'games', 'minutes')
    search_fields = ('player__first_name', 'player__last_name', 'tournament__name', 'season__year')
    list_filter = ('tournament', 'season')

# Для модели SeasonAwards
class SeasonAwardsAdmin(admin.ModelAdmin):
    list_display = ('id','season', 'tournament', 'best_scorer', 'best_goalkeeper', 'best_coach', 'best_team', 'best_player')
    search_fields = ('season__year', 'tournament__name')
    list_filter = ('season', 'tournament')

# Для модели Standings
class StandingsAdmin(admin.ModelAdmin):
    list_display = ('id','team', 'tournament', 'season', 'games', 'wins', 'draws', 'losses', 'goals_scored', 'goals_conceded', 'goals_difference', 'points')
    search_fields = ('team__name', 'tournament__name', 'season__year')
    list_filter = ('tournament', 'season')

# Для модели SiteSettings
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'logo', 'favicon', 'facebook_link', 'instagram_link', 'tiktok_link', 'youtube_link', 'copy_right')
    search_fields = ('title',)

# Для модели News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'date', 'image')
    search_fields = ('title', 'text')
    list_filter = ('date',)

# Для модели BestMoments
class BestMomentsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'link_moments', 'date')
    search_fields = ('title', 'description')
    list_filter = ('date',)

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_preview')
    search_fields = ('name',)

    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return "Нет фото"
    
    photo_preview.allow_tags = True
    photo_preview.short_description = "Превью фото"

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('id','about', 'documents', 'management', 'address', 'phone', 'email', 'facebook_link', 'instagram_link', 'tiktok_link', 'youtube_link', )

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo')



# Регистрируем модели
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Management, ManagementAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Matches, MatchesAdmin)
admin.site.register(MatchLineup, MatchLineupAdmin)
admin.site.register(EventsMathes, EventsMathesAdmin)
admin.site.register(StaticticsPlayerSeason, StaticticsPlayerSeasonAdmin)
admin.site.register(SeasonAwards, SeasonAwardsAdmin)
admin.site.register(Standings, StandingsAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(BestMoments, BestMomentsAdmin)
