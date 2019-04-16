import Server
import logging
import queue
import Logic
import time
from WorldState import World
from ActionBuilder import ActionBuilder


class App:
    def __init__(self):
        self.server = Server.SafeServer()
        self.server.start_as_daemon()
        self.action_queue = queue.Queue()
        self.logic = Logic.Logic()

    def update(self):
        while not self.server.action_queue.empty():
            player_id, current_action = self.server.action_queue.get()

        self.logic.move_all_unplayable_entities()

    def send_information(self):
        entities_to_draw = []
        for visible_entity in self.logic.geometry_system.get_visible_entities(World.get_first_player_id()):
            if visible_entity in World.enemies:
                entities_to_draw.append(ActionBuilder().set_x(World.get_position(visible_entity)[0])
                                        .set_y(World.get_position(visible_entity)[1]).set_type("ENEMY").get_action())
            if visible_entity in World.projectiles:
                entities_to_draw.append(ActionBuilder().set_x(World.get_position(visible_entity)[0])
                                        .set_y(World.get_position(visible_entity)[1]).set_type("PROJECTILE").get_action())
        self.server.send_obj_to_player(entities_to_draw, World.get_first_player_id())


if __name__ == '__main__':
    App = App()
    while True:
        time.sleep(0.01)
        logging.basicConfig(level=logging.DEBUG)
        App.update()
        App.send_information()
