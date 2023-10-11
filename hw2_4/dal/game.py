from sqlalchemy import Integer, VARCHAR, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship

from dal.base import Base
from dal.player import Player
from dal.game_status import GameStatus


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime = Column(DateTime(timezone=True))
    game_status_id = Column(Integer, ForeignKey(GameStatus.id), nullable=False)
    hidden_word = Column(VARCHAR(100), nullable=False)
    game = relationship(Player, foreign_keys=player_id)
    game_status = relationship(GameStatus, foreign_keys=game_status_id)
