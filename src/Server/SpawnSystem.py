from .Entity import Enemy, PlayerEntity
from .WorldState import World
from random import randint
from ..utility.constants import *
from .Entity import MeleeEnemy
from pygame import Rect
from .GeometrySystem import GeometrySystem
import logging

class MonsterSpawner:
    def __init__(self):
        self._monster_factories = []

    def spawn_monster(self, position):
        size =  len(self._monster_factories)
        return self._monster_factories[randint(0, size - 1)].generate_enemy()

    def add_monster_factory(self, factory):
        self._monster_factories.append(factory)

class SpawnSystem:
    def __init__(self):
        self._enemy_types = []

    def generate_players(self):
        self.create_player(World.get_first_player_id())
        self.create_player(World.get_second_player_id())
    def add_enemy_type(self, enemy_type: Enemy):
        self._enemy_types.append(enemy_type)

    def create_enemy(self, position=None):
        enemy_type = randint(0, len(self._enemy_types) - 1)
        current_id = World.entity.size()
        damage = generate_enemy_damage()
        health = generate_enemy_health()
        direction = generate_random_direction()
        box = None  # TODO: размеры дефолтных хитбоксов?
        entity = enemy_type().set_damage(damage).set_velocity(ENEMY_VELOCITY)\
            .set_direction(direction).set_position(position)\
            .set_health(health).set_box(box).set_id(self._current_id)
        World.entity[self._current_id] = entity
        World.movable_entities.add(self._current_id)
        World.enemies.add(self._current_id)

    # TODO: поддержка второго игрока
    def create_player(self, player_id): # Саша проверь кажется что position не нужен
        player_box = generate_random_free_box(Rect(0, 0, MAP_SCALE, MAP_SCALE))
        World.entity[player_id] = PlayerEntity().set_damage(PLAYER_START_DAMAGE).set_velocity(PLAYER_VELOCITY)\
            .set_direction((0, 0)).set_position((0, 0)).set_health(10).set_id(len(World.entity)).\
            set_box(player_box).set_position((player_box.centerx, player_box.centery))
        World.movable_entities.add(player_id)

    # TODO: система вещей?
    def create_item(self):
        pass


# TODO: вещи связанные с генерацией параметров у монстров
def generate_random_direction():
    return 0, 0


def generate_enemy_damage():
    return 0


def generate_enemy_health():
    return 0


def generate_random_free_box(box):
    x, y = 0, 0
    while(1):
        x = randint(0, MAP_SCALE * World.map.width - 1)
        y = randint(0, MAP_SCALE * World.map.height - 1)
        new_box = box.move(x, y)
        if (not GeometrySystem.collide_with_wall(new_box)):
            intersect_flag = False
            logging.debug("Enteties - {}".format(World.entity))
            for id, ent in World.entity.items():
                ent_box = ent.get_box()
                if (GeometrySystem.collide(ent_box, new_box)):
                    intersect_flag = True
                    break
            if not intersect_flag:
                return new_box
