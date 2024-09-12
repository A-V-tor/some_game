from sqladmin import ModelView
from src.database.models import Player, PlayerLevel, Prize, Level, LevelPrize, Boost


class PlayerView(ModelView, model=Player):
    name = 'Игрок'
    name_plural = 'Игроки'
    icon = 'fa-solid fa-user'
    column_labels = {
        Player.player_id: 'Идентификатор',
        Player.first_visit: 'Первое посещение',
        Player.last_visit: 'Последнее посещение',
        Player.is_daily_visit: 'Непрерывное посещение игры?',
    }

    column_list = [
        Player.player_id,
        Player.first_visit,
        Player.last_visit,
        Player.is_daily_visit,
    ]


class PlayerLevelView(ModelView, model=PlayerLevel):
    name = 'Уровень игрока'
    name_plural = 'Уровни игрока'
    column_labels = {
        PlayerLevel.completed: 'Дата завершения',
        PlayerLevel.is_completed: 'Завершен?',
        PlayerLevel.score: 'очки уровня'
    }

    column_list = [
        PlayerLevel.completed,
        PlayerLevel.is_completed,
        PlayerLevel.score
    ]


class PrizeView(ModelView, model=Prize):
    name = 'Приз'
    name_plural = 'Призы'
    column_labels = {
        Prize.id: 'id',
        Prize.title: 'Наименование',
    }

    column_list = [
        Prize.id,
        Prize.title
    ]


class LevelView(ModelView, model=Level):
    name = 'Уровень'
    name_plural = 'Уровни'
    column_labels = {
        Level.title: 'Наименование',
        Level.order: 'Значение',
    }

    column_list = [
        Level.title,
        Level.order
    ]


class LevelPrizeView(ModelView, model=LevelPrize):
    name = 'Приз уровня'
    name_plural = 'Призы уровня'
    column_labels = {
        LevelPrize.id: 'id',
        LevelPrize.received: 'дата получения',
    }

    column_list = [
        LevelPrize.id,
        LevelPrize.received
    ]

    form_excluded_columns = [LevelPrize.received]


class BoostView(ModelView, model=Boost):
    name = 'Буст'
    name_plural = 'Бусты'
    column_labels = {
        Boost.id: 'id',
        Boost.type: 'тип',
    }

    column_list = [
        Boost.id,
        Boost.type
    ]


