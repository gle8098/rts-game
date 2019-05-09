from .WorldState import world
from pygame import Rect
from .Entity import MeleeEnemy
from ..utility.constants import *


class EnemyFactory:
    def __init__(self):
        pass

    def generate_enemy(self):
        raise NotImplementedError


class MeleeEnemyFactory(EnemyFactory):
    def __init__(self):
        super().__init__()

    def generate_enemy(self):
        current_id = len(world.entity)
        box = generate_box()
        damage = generate_enemy_damage()
        health = generate_enemy_health()
        direction = generate_random_direction()
        return MeleeEnemy().set_id(current_id).set_box(box).set_damage(damage)\
            .set_health(health).set_direction(direction).set_attack_reload(ATTACK_RELOAD).set_velocity(ENEMY_VELOCITY)


# TODO: вещи связанные с генерацией параметров у монстров
def generate_random_direction():
    return 1, 0


def generate_enemy_damage():
    return 10


def generate_enemy_health():
    return 100000

def generate_box():
    return Rect(0, 0, ENEMY_BOX_SIZE, ENEMY_BOX_SIZE)
