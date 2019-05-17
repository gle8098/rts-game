import logging

from src.Client.UI.TextWidget import TextContainer
from src.Client.UI.Window import Window
from src.utility.utilities import Vector


class WaitWindow(Window):
    def __init__(self, window_size=None):
        super().__init__()
        text = TextContainer('Waiting! Be comfy, take a cookie.')

        if window_size is not None:
            text_size = text.get_text_size()
            text_position = Vector((window_size[0] - text_size.x) / 2, (window_size[1] - text_size.y) / 3)
        else:
            text_position = Vector(400, 500)

        self.add_child(text, text_position)
        self.map = None

    def accept_action(self, action):
        if not isinstance(action, list):
            raise RuntimeError(
                "Action is not of type list. Don't know what to do with it")

        if action[0] == "MAP":
            self.map = action[1]
            logging.info("Acquired map")
            self.sio.emit("message", "MAP_RECEIVED")

        if action[0] == "START_GAME":
            from src.Client.Game import game
            game.start_main_window(self.map)
