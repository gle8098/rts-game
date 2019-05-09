from .Entity import Enemy, PlayerEntity
from .WorldState import world
from random import randint
from .EnemyFactory import MeleeEnemyFactory
from ..utility.constants import *
from .Entity import MeleeEnemy
from pygame import Rect
from .GeometrySystem import GeometrySystem
import logging


class MonsterSpawner:
    def __init__(self):
        self._monster_factories = []

    def spawn_monster(self, *args):
        size = len(self._monster_factories)
        return self._monster_factories[randint(0, size - 1)].generate_enemy()

    def add_monster_factory(self, factory):
        self._monster_factories.append(factory)


class SpawnSystem:
    def __init__(self):
        self._enemy_types = []
        self.monster_spawner = MonsterSpawner()
        self.melee_enemy_factory = MeleeEnemyFactory()
        self.monster_spawner.add_monster_factory(self.melee_enemy_factory)

    def generate_players(self):
        self.create_player(world.get_first_player_id())
        self.create_player(world.get_second_player_id())

    def create_enemy(self, position=None):
        entity = self.monster_spawner.spawn_monster()  # Создание
        entity_box = generate_random_free_box(entity.get_box())  # Определение куда его поставить на карте
        entity.set_box(entity_box)

        # Добавление во всевозможные хранилища
        world.entity[entity._id] = entity
        world.movable_entities.add(entity._id)
        world.enemies.add(entity._id)

    def create_player(self, player_id):
        player_box = generate_random_free_box(Rect(0, 0, PLAYER_HEIGHT, PLAYER_WIDTH))
        world.entity[player_id] = PlayerEntity().set_damage(PLAYER_START_DAMAGE).set_velocity(PLAYER_VELOCITY)\
            .set_direction((0, 0)).set_health(PLAYER_HEALTH).set_id(len(world.entity)).\
            set_box(player_box).set_position((player_box.centerx, player_box.centery))
        world.movable_entities.add(player_id)

    # TODO: система вещей?
    def create_item(self):
        pass


def generate_random_free_box(box):
    while(True):
        x = randint(0, MAP_SCALE * world.map.width - 1)
        y = randint(0, MAP_SCALE * world.map.height - 1)
        new_box = box.move(x, y)
        if not GeometrySystem.collide_with_wall(new_box):
            intersect_flag = False
            logging.debug("Enteties - {}".format(world.entity))
            for id, ent in world.entity.items():
                ent_box = ent.get_box()
                if GeometrySystem.collide(ent_box, new_box):
                    intersect_flag = True
                    break
            if not intersect_flag:
                return new_box
