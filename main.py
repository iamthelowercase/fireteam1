#!/usr/bin/env python3
## dev: remember to activate the venv for this to work!
## (``source ./bin/activate'')

import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from entity import Entity
from engine import Engine
from procgen import generate_dungeon

def main() -> None:
    screen_width = 120
    screen_height = 68
    
    map_width = 120
    map_height = 68
    
    room_max_size = 15
    room_min_size = 9
    max_rooms = 30


    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )
    
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Fireteam! pre-alpha",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
