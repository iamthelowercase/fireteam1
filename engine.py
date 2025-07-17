from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov() # update the FOV after every player action

    def update_fov(self) -> None:
        """ Recompute the visible area based on the player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=12, # this number controls how far the player characters can see
            light_walls=True, # added as part of experimenting with FOV algorithms; unneeded otherwise
            algorithm=0,
            # agorthim = 0 # a basic ray casting implementation that I kind of like
            # see https://python-tcod.readthedocs.io/en/latest/tcod/map.html#tcod.map.compute_fov for more options, although not well explained how to invoke them
        )
        # if a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()
