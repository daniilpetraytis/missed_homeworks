from sqlalchemy import Column, Integer, VARCHAR

from dal.base import Base


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    win_count = Column(Integer, nullable=False)
