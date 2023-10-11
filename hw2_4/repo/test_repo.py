from sqlalchemy.orm import DeclarativeBase
from typing import Dict, Set

from repo.base_repo import BaseRepo

class TestRepo(BaseRepo):
    __state: Dict[str, Set[DeclarativeBase]] = None

    def __init__(self):
        self.__state = dict()

    def __touch_table(self, table_name):
        if table_name not in self.__state:
            self.__state[table_name] = set()

    def add(self, entity):
        self.__touch_table(entity.__tablename__)
        self.__state[entity.__tablename__].add(entity)

    def remove(self, entity):
        self.__touch_table(entity.__tablename__)
        self.__state[entity.__tablename__].remove(entity)

    def get_by_id(self, table, id):
        self.__touch_table(table.__tablename__)
        for entity in self.__state[table.__tablename__]:
            if entity.id == id:
                return entity
        return None

    def list(self, table):
        self.__touch_table(table.__tablename__)
        return list(self.__state[table.__tablename__])

    def update(self, entity):
        self.__touch_table(entity.__tablename__)
        for elem in self.__state[entity.__tablename__]:
            if elem.id == entity.id:
                self.__state[entity.__tablename__].remove(elem)
                self.__state[entity.__tablename__].add(entity)
                break
