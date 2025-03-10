from django.db.models.signals import post_save, post_delete,pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import EventsMathes, Matches, Standings, StaticticsPlayerSeason, EventsMathes

# Обновление статистики игроков при добавлении события матча (голы, карточки и т.д.)
@receiver(post_save, sender=EventsMathes)
def update_player_statistics(sender, instance, created, **kwargs):
    if created:
        player_stats, _ = StaticticsPlayerSeason.objects.get_or_create(
            player=instance.player,
            tournament=instance.match.tournament,
            season=instance.match.season
        )

        if instance.event == "Гол":
            player_stats.goals += 1
        elif instance.event == "Пас":
            player_stats.assists += 1
        elif instance.event == "Желтая карточка":
            player_stats.yellow_cards += 1
        elif instance.event == "Красная карточка":
            player_stats.red_cards += 1

        player_stats.save()


# Автоматическое обновление турнирной таблицы после завершения матча
@receiver(post_save, sender=Matches)
def update_standings_after_match(sender, instance, **kwargs):
    if instance.status == "Закончен":
        home_team, _ = Standings.objects.get_or_create(
            team=instance.home_team, 
            tournament=instance.tournament, 
            season=instance.season
        )
        away_team, _ = Standings.objects.get_or_create(
            team=instance.away_team, 
            tournament=instance.tournament, 
            season=instance.season
        )

        home_team.games += 1
        away_team.games += 1

        home_goals = instance.home_goals or 0  # Если None, то 0
        away_goals = instance.away_goals or 0  # Если None, то 0

        home_team.goals_scored += home_goals
        home_team.goals_conceded += away_goals

        away_team.goals_scored += away_goals
        away_team.goals_conceded += home_goals

        if home_goals > away_goals:
            home_team.wins += 1
            home_team.points += 3
            away_team.losses += 1
        elif home_goals < away_goals:
            away_team.wins += 1
            away_team.points += 3
            home_team.losses += 1
        else:
            home_team.draws += 1
            away_team.draws += 1
            home_team.points += 1
            away_team.points += 1

        home_team.goals_difference = home_team.goals_scored - home_team.goals_conceded
        away_team.goals_difference = away_team.goals_scored - away_team.goals_conceded

        home_team.save()
        away_team.save()


@receiver(post_save, sender=EventsMathes)
def update_match_score(sender, instance, created, **kwargs):
    if created and instance.match.status == "В процессе" and instance.event == "Гол":
        match = instance.match  # Получаем матч

        # Проверяем, что значения не None, иначе присваиваем 0
        match.home_goals = match.home_goals if match.home_goals is not None else 0
        match.away_goals = match.away_goals if match.away_goals is not None else 0

        # Увеличиваем счет в зависимости от команды игрока
        if instance.player.team == match.home_team:
            match.home_goals += 1
        elif instance.player.team == match.away_team:
            match.away_goals += 1

        match.save()  # Сохраняем обновленный счет

@receiver(pre_save, sender=Matches)
def update_match_status(sender, instance, **kwargs):
    # Если статус еще не обновлен и время матча уже прошло
    if instance.status == 'Не начался' and instance.date_match <= timezone.now().date():
        if instance.time_match <= timezone.now().time():
            instance.status = 'В процессе'