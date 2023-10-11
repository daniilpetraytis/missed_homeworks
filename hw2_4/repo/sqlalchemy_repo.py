from sqlalchemy import select
from sqlalchemy.orm import Session

from repo.base_repo import BaseRepo


class SQLAlchemyRepo(BaseRepo):
    __session: Session = None

    def __init__(self, session):
        self.__session = session

    def add(self, entity):
        self.__session.add(entity)

    def remove(self, entity):
        self.__session.delete(entity)

    def get_by_id(self, table, id):
        return self.__session.get(table, id)

    def list(self, table):
        res = []
        for elem in self.__session.execute(select(table)).all():
            res.append(elem[0])
        return res

    def update(self, entity):
        updating = {}
        for elem in entity.__table__.columns.keys():
            if elem != "id":
                updating[elem] = entity.__dict__[elem]

        self.__session.query(type(entity)).filter(entity.id == type(entity).id).update(updating)
