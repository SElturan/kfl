import random
from datetime import datetime, timedelta
from faker import Faker
from django.utils.timezone import make_aware
from core.models import Teams, Players, Matches, Standings, StaticticsPlayerSeason

fake = Faker()

# Данные о командах
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

# Очистка базы перед добавлением
Teams.objects.all().delete()
Players.objects.all().delete()
Matches.objects.all().delete()
Standings.objects.all().delete()
StaticticsPlayerSeason.objects.all().delete()

# Создание команд
teams = []
for name, games, wins, draws, losses, goals_scored, goals_conceded, points in teams_data:
    team = Teams.objects.create(name=name)
    teams.append(team)

    # Добавление в турнирную таблицу
    Standings.objects.create(
        team=team,
        season="2024",
        games=games,
        wins=wins,
        draws=draws,
        losses=losses,
        goals_scored=goals_scored,
        goals_conceded=goals_conceded,
        points=points
    )

# Создание игроков
positions = ["Вратарь", "Защитник", "Полузащитник", "Нападающий"]
for team in teams:
    for _ in range(11):
        player = Players.objects.create(
            team=team,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=35),
            position=random.choice(positions),
            number=random.randint(1, 99),
            height=random.randint(165, 200),
            weight=random.randint(60, 100),
            nationality=fake.country(),
            goals=random.randint(0, 20),
            assists=random.randint(0, 10),
            yellow_cards=random.randint(0, 5),
            red_cards=random.randint(0, 2),
            games=random.randint(5, 27),
            minutes=random.randint(100, 2500),
        )

        # Создание статистики игрока по сезонам
        StaticticsPlayerSeason.objects.create(
            player=player,
            season="2024",
            goals=player.goals,
            assists=player.assists,
            yellow_cards=player.yellow_cards,
            red_cards=player.red_cards,
            games=player.games,
            minutes=player.minutes
        )

# Создание матчей (по 5 матчей для каждой команды)
matches = []
match_dates = [make_aware(datetime.now() - timedelta(days=i)) for i in range(1, 31, 5)]

for team in teams:
    opponents = random.sample(teams, 5)  # Выбираем 5 случайных команд-соперников
    for opponent in opponents:
        if team != opponent:
            match = Matches.objects.create(
                home_team=team,
                away_team=opponent,
                date_match=random.choice(match_dates),
                home_goals=random.randint(0, 5),
                away_goals=random.randint(0, 5),
                stadium=fake.company(),
                status="Закончен"
            )
            matches.append(match)

print("База данных успешно заполнена!")
