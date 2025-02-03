from django.db import models

class Teams(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название команды')
    logo = models.ImageField(upload_to='teams/', verbose_name='Логотип команды',null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='Город',null=True, blank=True)
    stadium = models.CharField(max_length=100, verbose_name='Стадион',null=True, blank=True)
    coach = models.CharField(max_length=100, verbose_name='Тренер',null=True, blank=True)
    founded_year = models.IntegerField(verbose_name='Год основания',null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class Players(models.Model):

    class PositionChoices(models.TextChoices):
        GOALKEEPER = 'Вратарь'
        DEFENDER = 'Защитник'
        MIDFIELDER = 'Полузащитник'
        FORWARD = 'Нападающий'

    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='Команда')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='players/', verbose_name='Фото',null=True, blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения',null=True, blank=True)
    position = models.CharField(max_length=100, choices=PositionChoices.choices, verbose_name='Позиция',null=True, blank=True)
    number = models.IntegerField(verbose_name='Номер',null=True, blank=True)
    height = models.IntegerField(verbose_name='Рост',null=True, blank=True)
    weight = models.IntegerField(verbose_name='Вес',null=True, blank=True)
    nationality = models.CharField(max_length=100, verbose_name='Национальность',null=True, blank=True)
    goals = models.IntegerField(verbose_name='Голы',null=True, blank=True)
    assists = models.IntegerField(verbose_name='Пасы',null=True, blank=True)
    yellow_cards = models.IntegerField(verbose_name='Желтые карточки',null=True, blank=True)
    red_cards = models.IntegerField(verbose_name='Красные карточки',null=True, blank=True)
    games = models.IntegerField(verbose_name='Игры',null=True, blank=True)
    minutes = models.IntegerField(verbose_name='Минуты',null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Matches(models.Model): 

    class StatusChoices(models.TextChoices):
        NOT_STARTED = 'Не начался'
        IN_PROGRESS = 'В процессе'
        FINISHED = 'Закончен'

    home_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='home_team', verbose_name='Хозяева')
    away_team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='away_team', verbose_name='Гости')
    date_match = models.DateField(verbose_name='Дата матча',null=True, blank=True)
    home_goals = models.IntegerField(verbose_name='Голы хозяев',null=True, blank=True)
    away_goals = models.IntegerField(verbose_name='Голы гостей',null=True, blank=True)
    stadium = models.CharField(max_length=100, verbose_name='Стадион',null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус')


    def __str__(self):
        return self.home_team.name + ' ' + str(self.home_goals) + ' - ' + str(self.away_goals) + ' ' + self.away_team.name

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


class EventsMathes(models.Model):

    class EventChoices(models.TextChoices):
        GOAL = 'Гол'
        ASSIST = 'Пас'
        YELLOW_CARD = 'Желтая карточка'
        RED_CARD = 'Красная карточка'
        NO_PENALTY = 'Незабитый пенальти'
        PENALTY = 'Забитый пенальти'
        SUBSTITUTION = 'Замена'
        AUTO_GOAL = 'Автогол'
        INJURY = 'Травма'


    match = models.ForeignKey(Matches, on_delete=models.CASCADE, verbose_name='Матч')
    player = models.ForeignKey(Players, on_delete=models.CASCADE, verbose_name='Игрок')
    event = models.CharField(max_length=100, choices=EventChoices.choices, verbose_name='Событие')
    time = models.TimeField(verbose_name='Время')

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name + ' - ' + self.event

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

class StaticticsPlayerSeason(models.Model):

    YEAR_CHOICES = [(str(year), str(year)) for year in range(1800, 2101)]

    player = models.ForeignKey(Players, on_delete=models.CASCADE, verbose_name='Игрок')
    season = models.CharField(max_length=100, choices=YEAR_CHOICES, verbose_name='Сезон')
    goals = models.IntegerField(verbose_name='Голы')
    assists = models.IntegerField(verbose_name='Пасы')
    yellow_cards = models.IntegerField(verbose_name='Желтые карточки')
    red_cards = models.IntegerField(verbose_name='Красные карточки')
    games = models.IntegerField(verbose_name='Игры')
    minutes = models.IntegerField(verbose_name='Минуты')

    def __str__(self):
        return self.player.first_name + ' ' + self.player.last_name + ' - ' + self.season

    class Meta:
        verbose_name = 'Статистика игрока за сезон'
        verbose_name_plural = 'Статистика игроков за сезон'

class Standings(models.Model):

    YEAR_CHOICES = [(str(year), str(year)) for year in range(1800, 2101)]

    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='Команда')
    season = models.CharField(max_length=100, choices=YEAR_CHOICES, verbose_name='Сезон')
    games = models.IntegerField(verbose_name='Игры')
    wins = models.IntegerField(verbose_name='Победы')
    draws = models.IntegerField(verbose_name='Ничьи')
    losses = models.IntegerField(verbose_name='Поражения')
    goals_scored = models.IntegerField(verbose_name='Забитые голы')
    goals_conceded = models.IntegerField(verbose_name='Пропущенные голы')
    points = models.IntegerField(verbose_name='Очки')

    def __str__(self):
        return self.team.name + ' - ' + self.season

    class Meta:
        verbose_name = 'Турнирная таблица'
        verbose_name_plural = 'Турнирные таблицы'


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='site_logo/', verbose_name="Логотип", null=True, blank=True)
    favicon = models.ImageField(upload_to='site_favicon/', verbose_name="Фавикон", null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы", null=True, blank=True)
    facebook_link = models.URLField(verbose_name="Facebook", null=True, blank=True)
    instagram_link = models.URLField(verbose_name="Instagram", null=True, blank=True)
    tiktok_link = models.URLField(verbose_name="TikTok", null=True, blank=True)
    youtube_link = models.URLField(verbose_name="YouTube", null=True, blank=True)
    copy_right = models.CharField(max_length=255, verbose_name="Копирайт", null=True, blank=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение',null=True, blank=True)
    date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class BestMoments(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Текст')
    link_moments = models.URLField(verbose_name="Лучшие моменты", null=True, blank=True)
    date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Лучшие моменты'
        verbose_name_plural = 'Лучшие моменты'

