from sqlalchemy import Integer, VARCHAR, Column

from dal.base import Base

class GameStatus(Base):
    __tablename__ = "game_status"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(VARCHAR(20), nullable=False)
