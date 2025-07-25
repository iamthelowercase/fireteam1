from __future__ import annotations

# from typing import Iterable, Any, TYPE_CHECKING
from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    # from input_handlers import EventHandler
    from game_map import GameMap


class Engine:
    game_map: GameMap
    
    # def __init__(self, player: Entity, player_characters: [Entity]):
    def __init__(self, starting_player: Entity, player_characters: set[Entity]):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = starting_player
        self.player_characters = player_characters

    def process_time(self) -> None:
        # simple turn stub for now
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')

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
