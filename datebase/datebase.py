import pickle
import os
import sys
import logging

from dataclasses import dataclass, field
from services.services import Ship, GamePole

_BD = r'datebase\bd.pickle'

logger = logging.getLogger(__name__)

@dataclass
class UserBD:
    in_game: bool = False
    user_pole: GamePole = field(default_factory=list)
    comp_pole: GamePole = field(default_factory=list)
    games: int = 0
    wins: int = 0
    chat: list[str] = field(default_factory=list)


def write_to_bd() -> None:
    path = os.path.join(sys.path[0], _BD)
    with open(path, 'wb') as file:
        pickle.dump(users_bd, file)
    logger.info('Запись в БД')


def read_from_bd() -> set[dict]:
    path = os.path.join(sys.path[0], _BD)
    try:
        with open(path, 'rb') as file:
            res = pickle.load(file)
        logger.info('Чтение из БД', 'res:', res)
        return res
    except FileNotFoundError:
        print("Загрузить БД пользователей не возможно. Отсутствует файл datebase\\bd.pickle.\nПрекращение работы")
        write_to_bd()

def create_bd(path) -> None:
    users_bd = {0:UserBD()}
    # # Создаём папку
    # os.makedirs(os.path.dirname(path), exist_ok=True)  # exist_ok=True — не вызывает ошибку, если папка уже есть
    with open(path, 'wb') as file:
        pickle.dump(users_bd, file)
    logger.info('Создание файла БД')

# Инициализируем "базу данных"
path = os.path.join(sys.path[0], _BD)
if not os.path.exists(path):
    create_bd(path)
users_bd: dict[int, UserBD] = read_from_bd()
print(users_bd)
