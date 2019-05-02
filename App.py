import src.Server.Server as Server
import logging
import queue
from src.Server import Logic
import time
from src.Server.WorldState import World
from src.Server.ActionBuilder import ActionBuilder


class App:
    def __init__(self, server):
        self.server = server
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()
        self.logic = Logic.Logic()

    def update(self):
        while not self.server.action_queue.empty():
            player_id, current_action = self.server.action_queue.get()
            logging.debug("action {}".format(current_action))
            if current_action.startswith("MOVE"):
                if current_action == "MOVE_LEFT":
                    self.logic.move(World.get_first_player_id(), (-1, 0))
                    self.logic.animation_system.continue_or_reset(0, 'walk_left')
                if current_action == "MOVE_RIGHT":
                    self.logic.move(World.get_first_player_id(), (1, 0))
                    self.logic.animation_system.continue_or_reset(0, 'walk_right')
                if current_action == "MOVE_UP":
                    self.logic.move(World.get_first_player_id(), (0, -1))
                    self.logic.animation_system.continue_or_reset(0, 'walk_up')
                if current_action == "MOVE_DOWN":
                    self.logic.move(World.get_first_player_id(), (0, 1))
                    self.logic.animation_system.continue_or_reset(0, 'walk_down')
            if current_action == "STOP":
                self.logic.animation_system.continue_or_reset(0, 'idle')

        self.logic.move_all_unplayable_entities()

    def send_information(self):
        entities_to_draw = []
        for visible_entity in self.logic.geometry_system.get_visible_entities(
                World.get_first_player_id()):
            if visible_entity in World.enemies:
                entities_to_draw.append(ActionBuilder().set_x(
                    World.get_position(visible_entity)[0])
                                        .set_y(
                    World.get_position(visible_entity)[1]).set_type(
                    "ENEMY").get_action())
            if visible_entity in World.projectiles:
                entities_to_draw.append(ActionBuilder().set_x(
                    World.get_position(visible_entity)[0])
                                        .set_y(
                    World.get_position(visible_entity)[1]).set_type(
                    "PROJECTILE").get_action())
            if visible_entity == World.get_first_player_id():
                entities_to_draw.append(ActionBuilder().set_x(
                    World.get_position(World.get_first_player_id())[0])
                                        .set_y(
                    World.get_position(World.get_first_player_id())[
                        1]).set_type("PLAYER1")
                                        .set_animation_state(
                    *self.logic.animation_system.get_animation_state(0))
                                        .get_action())
        self.server.send_obj_to_player(entities_to_draw,
                                       World.get_first_player_id())


if __name__ == '__main__':
    with Server.SafeServer() as server:
        App = App(server)
        logging.basicConfig(level=logging.INFO)
        while True:
            time.sleep(0.01)
            App.update()
            App.send_information()