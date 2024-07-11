import pickle
import os
import sys
import logging

from dataclasses import dataclass, field

_BD = r'datebase\bd.pickle'

logger = logging.getLogger(__name__)

@dataclass
class UserBD:
    page: int = 1
    bookmarks: set[int] = field(default_factory=set)


def write_to_bd() -> None:
    path = os.path.join(sys.path[0], _BD)
    with open(path, 'wb') as file:
        pickle.dump(users_bd, file)
    logger.info('Запись в БД')


def read_from_bd() -> set[dict]:
    path = os.path.join(sys.path[0], _BD)
    with open(path, 'rb') as file:
        res = pickle.load(file)
    logger.info('Чтение из БД')
    return res


# Инициализируем "базу данных"
users_bd: dict[int, UserBD] = read_from_bd()
print(users_bd)