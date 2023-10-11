from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from dal.base import Base
from dal.game import Game


class TurnHistory(Base):
    __tablename__ = "turn_history"

    id = Column(Integer, primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey(Game.id), nullable=False)
    turn_datetime = Column(DateTime(timezone=True), nullable=False)
    guessed_letter = Column(VARCHAR(1), nullable=False)
    current_word_status = Column(VARCHAR(100), nullable=False)
    game = relationship(Game, foreign_keys=game_id)
