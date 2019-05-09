from math import sin, cos
from random import randint

from src.Server.WorldState import world
from src.utility.constants import *
from random import randint
from math import sin, cos
from src.Server.Entity import PlayerEntity, Enemy


class GeometrySystem:

    def get_visible_tiles(self, entity_id):
        # Обновлять glare для правильного игрока
        glare_map = None
        visible_tiles = []
        if entity_id == world.first_player_id:
            glare_map = world.first_player_glare
        if entity_id == world.second_player_id:
            glare_map = world.second_player_id

        for i in range(360):
            deg = i * 3.1415 / 180
            x0 = world.get_box(entity_id).centerx
            y0 = world.get_box(entity_id).centery
            x = round(cos(deg) * VISION_RANGE) + world.get_box(
                entity_id).centerx
            y = round(sin(deg) * VISION_RANGE) + world.get_box(
                entity_id).centery

            diag_dist = max(abs(x - x0), abs(y - y0))

            for j in range(diag_dist):
                tx = round(x0 + (j / diag_dist) * (x - x0))
                ty = round(y0 + (j / diag_dist) * (y - y0))

                if (tx < 0 or tx >= world.map.width * MAP_SCALE) or (
                        ty < 0 or ty >= world.map.height * MAP_SCALE):
                    break
                if world.map.level[tx][ty] == WALL:
                    visible_tiles.append((tx, ty))
                    break
                visible_tiles.append((tx, ty))
                if glare_map is not None:
                    glare_map[tx][ty] = 1
        return visible_tiles

    # TODO: нормальная система зрения
    @staticmethod
    def _is_visible(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (
                position1[1] - position2[1]) ** 2) ** 0.5 < VISION_RANGE

    @staticmethod
    def _is_attackable(position1: tuple, position2: tuple) -> bool:
        return ((position1[0] - position2[0]) ** 2 + (
                position1[1] - position2[1]) ** 2) ** 0.5 < ATTACK_RANGE

    def get_visible_entities(self, entity_id) -> list:
        entities_id = []
        for other_entity_id in world.entity.keys():
            if self._is_visible(world.get_position(entity_id),
                                world.get_position(other_entity_id)):
                entities_id.append(other_entity_id)
        return entities_id

    def get_attackable_entites(self, entity_id) -> list:
        entities_id = []
        if isinstance(world.entity[entity_id], PlayerEntity):
            EnemyClass = Enemy
        if isinstance(world.entity[entity_id], Enemy):
            EnemyClass = PlayerEntity

        for other_entity_id in world.entity.keys():
            if isinstance(world.entity[other_entity_id], EnemyClass):
                if self._is_attackable(world.get_position(entity_id), world.get_position(other_entity_id)) \
                        and other_entity_id != entity_id:
                    entities_id.append(other_entity_id)
        return entities_id

    # TODO
    def generate_npc_movement(self, npc_id):
        return randint(-1, 1), randint(-1, 1)

    # Провекра пересечения хитбоксов
    @staticmethod
    def collide(box1, box2):
        return box1.colliderect(box2)

    @staticmethod
    def collide_with_wall(box):  # Саша проверь
        non_passable_textures = {WALL, STONE}
        return world.map.get(
            *box.topleft) in non_passable_textures or world.map.get(
            *box.topright) \
               in non_passable_textures or world.map.get(
            *box.bottomleft) in non_passable_textures or \
               world.map.get(*box.bottomright) in non_passable_textures
