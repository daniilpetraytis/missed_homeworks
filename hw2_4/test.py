import pytest

from repo.sqlalchemy_repo import SQLAlchemyRepo
from repo.test_repo import TestRepo

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import create_engine

from dal.player import Player
from dal.game import Game
from dal.game_status import GameStatus
from dal.turn_history import TurnHistory

@pytest.fixture
def session():
    db_string = "postgresql://admin:admin@localhost:5432/admin"
    engine = create_engine(db_string)
    Session = sessionmaker(bind=engine)
    yield Session()

def player(entities, entity=None):
    if entity is None:
        entity = Player(name="PLAYER", win_count=0)
    else:
        entity.name += "_PLAYER"
    return entity


def game_status(entities, entity=None):
    if entity is None:
        entity = GameStatus(title="GAME")
    else:
        entity.title += "_GAME"
    return entity

def game(entities, entity=None):
    if entity is None:
        for entity in entities:
            if type(entity) == Player:
                player = entity
            elif type(entity) == GameStatus:
                game_status = entity
        entity = Game(
            start_datetime=func.now(),
            hidden_word="TEST",
            player_id=player.id,
            game_status_id=game_status.id,
        )
    else:
        entity.hidden_word += "_WORD"
    return entity

def turn_history(entities, entity=None):
    if entity is None:
        for entity in entities:
            if type(entity) == Game:
                game = entity

        entity = TurnHistory(
            game_id=game.id,
            turn_datetime=func.now(),
            guessed_letter="X",
            current_word_status="WORD"
        )
    else:
        entity.current_word_status += "_WORD"
    return entity


def check_entity(repo1, repo2, entity):
    return (entity in repo1.list(type(entity))) == (entity in repo2.list(type(entity)))


@pytest.mark.parametrize('entity_functions', [
    (player,),
    (player, game_status),
    (player, game_status, game)
])
def test_add_list(session, entity_functions):
    sqlalchemy_repo = SQLAlchemyRepo(session)
    test_repo = TestRepo()

    entities = []
    for entity_function in entity_functions:
        entity = entity_function(entities)
        entities.append(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)
        sqlalchemy_repo.add(entity)
        test_repo.add(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)
    session.commit()

@pytest.mark.parametrize('entity_functions', [
    (player,),
    (player, game_status),
    (player, game_status, game),
    (player, game_status, game, turn_history),
])
def test_add_remove_list(session, entity_functions):
    sqlalchemy_repo = SQLAlchemyRepo(session)
    test_repo = TestRepo()
    
    entities = []
    for entity_function in entity_functions:
        entity = entity_function(entities)
        entities.append(entity)
        
        assert check_entity(test_repo, sqlalchemy_repo, entity)
        sqlalchemy_repo.add(entity)
        test_repo.add(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)

    for entity in reversed(entities):
        assert check_entity(test_repo, sqlalchemy_repo, entity)
        sqlalchemy_repo.remove(entity)
        test_repo.remove(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)

    session.commit()


def is_correct(sqlalchemy_repo, test_repo, type_entity, entity_id):
    return sqlalchemy_repo.get_by_id(type_entity, entity_id) == test_repo.get_by_id(type_entity, entity_id)


@pytest.mark.parametrize('entity_functions', [
    (player,),
    (player, game_status),
    (player, game_status, game),
    (player, game_status, game, turn_history),
])
def test_add_get(session, entity_functions):
    sqlalchemy_repo = SQLAlchemyRepo(session)
    test_repo = TestRepo()

    entities = []
    for entity_function in entity_functions:
        entity = entity_function(entities)
        entities.append(entity)

        assert check_entity(test_repo, sqlalchemy_repo, entity)
        sqlalchemy_repo.add(entity)
        test_repo.add(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)

    for entity in reversed(entities):
        assert is_correct(sqlalchemy_repo, test_repo, type(entity), entity.id)

    session.commit()


@pytest.mark.parametrize('entity_functions', [
    (player,),
    (player, game_status),
    (player, game_status, game),
    (player, game_status, game, turn_history),
])
def test_add_get_update(session, entity_functions):
    sqlalchemy_repo = SQLAlchemyRepo(session)
    test_repo = TestRepo()
    
    entities = []
    for entity_function in entity_functions:
        entity = entity_function(entities)
        entities.append(entity)
        
        assert check_entity(test_repo, sqlalchemy_repo, entity)
        sqlalchemy_repo.add(entity)
        test_repo.add(entity)
        assert check_entity(test_repo, sqlalchemy_repo, entity)
    
    for id in range(len(entities)):
        entity = entity_functions[id](entities, entities[id])
        sqlalchemy_repo.update(entity)
        test_repo.update(entity)
        assert is_correct(sqlalchemy_repo, test_repo, type(entity), entity.id)

    session.commit()
