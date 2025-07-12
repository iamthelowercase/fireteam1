#!/usr/bin/env python3
## dev: remember to activate the venv for this to work!
## (``source ./bin/activate'')

import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from entity import Entity
from engine import Engine

def main() -> None:
    screen_width = 80
    screen_height = 50


    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    troll = Entity(int(screen_width / 2 - 5), int(screen_height / 3), "T", (255, 255, 0))
    zombie = Entity(int(screen_width / 2), int(screen_height / 2 - 5), "z", (0,255,255))
    entities = {troll, zombie, player}
    
    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    with tcod.context.new_terminal(
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
