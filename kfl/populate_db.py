from datetime import date
import random
from faker import Faker
from django.utils.timezone import make_aware
from core.models import Teams, Players, Matches, Standings, StaticticsPlayerSeason, Season, Tournament  # Импорт Tournament

fake = Faker()

# Данные о командах Кыргызстана
teams_data = [
    ("Абдыш-Ата", 27, 22, 3, 2, 67, 15, 69),
    ("Дордой", 27, 17, 8, 2, 43, 18, 59),
    ("Мурас Юнайтед", 27, 16, 6, 5, 50, 34, 54),
    ("Алай", 27, 13, 8, 6, 37, 29, 47),
    ("Нефтчи Кочкор-Ата", 27, 8, 7, 12, 36, 40, 31),
    ("Илбирс", 27, 8, 2, 17, 30, 48, 26),
    ("ОшМУ Алдиер", 27, 6, 7, 14, 27, 43, 25),
    ("Талант", 27, 6, 6, 15, 20, 43, 24),
    ("Алга", 27, 5, 5, 17, 29, 48, 20),
    ("Кыргызалтын", 27, 4, 8, 15, 19, 40, 20),
]

# Очистка базы перед добавлением новых данных
Teams.objects.all().delete()
Players.objects.all().delete()
Matches.objects.all().delete()
Standings.objects.all().delete()
StaticticsPlayerSeason.objects.all().delete()

# Создание сезона
season_2024, created = Season.objects.get_or_create(
    year=2024,
    defaults={
        'start_date': date(2024, 1, 1),
        'end_date': date(2024, 12, 31),
    }
)

# Создание турнира с указанием сезона
tournament_2024, created = Tournament.objects.get_or_create(
    name="Турнир 2024",  # Название турнира
)

# Создание команд
teams = []
for name, games, wins, draws, losses, goals_scored, goals_conceded, points in teams_data:
    team = Teams.objects.create(name=name)
    teams.append(team)

    # Добавление команды в турнирную таблицу
    Standings.objects.create(
        team=team,
        season=season_2024,
        tournament=tournament_2024,  # Указываем турнир
        games=games,
        wins=wins,
        draws=draws,
        losses=losses,
        goals_scored=goals_scored,
        goals_conceded=goals_conceded,
        points=points
    )

# Создание игроков с реалистичными позициями
positions = {
    "Вратарь": 2,
    "Защитник": 5,
    "Полузащитник": 6,
    "Нападающий": 4,
}

for team in teams:
    for position, count in positions.items():
        for _ in range(count):
            player = Players.objects.create(
                team=team,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=35),
                position=position,
                number=random.randint(1, 99),
                height=random.randint(170, 195),
                weight=random.randint(65, 95),
                nationality="Кыргызстан",
                goals=random.randint(0, 15),
                assists=random.randint(0, 10),
                yellow_cards=random.randint(0, 5),
                red_cards=random.randint(0, 2),
                games=random.randint(5, 27),
                minutes=random.randint(300, 2500),
            )

            # Статистика игрока за сезон
            StaticticsPlayerSeason.objects.create(
                player=player,
                season=season_2024,  # Указываем сезон
                tournament=tournament_2024,  # Указываем турнир
                goals=player.goals,
                assists=player.assists,
                yellow_cards=player.yellow_cards,
                red_cards=player.red_cards,
                games=player.games,
                minutes=player.minutes
            )


print("Команды, игроки и турнирная таблица успешно добавлены в базу данных!")