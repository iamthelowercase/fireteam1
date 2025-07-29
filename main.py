#!/usr/bin/env python3
## dev: remember to activate the venv for this to work!
## (``source ./bin/activate'')

import copy
import tcod

from actions import EscapeAction, MovementAction
from entity import Entity
import entity_factories
from engine import Engine
from procgen import generate_dungeon

from game_map import GameMap # added for testing map purposes

def main() -> None:
#     screen_width = 120
#     screen_height = 68
#     
#     map_width = 120
#     map_height = 68
#     

    # testing values for screen and map size
    screen_width = 70
    screen_height = 40
    map_width = 70
    map_height = 40
    
    room_max_size = 15
    room_min_size = 9
    max_rooms = 30
    
    max_monsters_per_room = 3


    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )


    # player0 = copy.deepcopy(entity_factories.player_character_1)
    player0 = copy.deepcopy(entity_factories.player)
    player0.x = int(screen_width / 2)
    # player0.x = 35
    player0.y = int(screen_height / 2) # forgot to cast to an integer!
    player0.char = "1"
    player0.name = "Zasta"
    
    player1 = copy.deepcopy(entity_factories.player)
    player1.x = int(screen_width / 3)
    player1.y = int(screen_height /3)
    player1.char = "2"
    player1.name = "Malarky"
    
    player2 = copy.deepcopy(entity_factories.player)
    player2.x = int((screen_width / 3) + (screen_width / 2))
    player2.y = int((screen_height / 3) + (screen_height / 2))
    player2.char = "3"
    player2.name = "Beep"
    
    player_characters = {player0, player1, player2}

    engine = Engine(starting_player=player0, player_characters=player_characters)
    
    # engine.game_map = generate_dungeon(
    #     max_rooms=max_rooms,
    #     room_min_size=room_min_size,
    #     room_max_size=room_max_size,
    #     map_width=map_width,
    #     map_height=map_height,
    #     max_monsters_per_room=max_monsters_per_room,
    #     engine=engine,
    # #     player=player0,
    # #     player_characters=player_characters,
    # )
    
    # generate empty testing map
    engine.game_map = GameMap(engine, map_width, map_height, entities=player_characters)
    
    player0.gamemap = engine.game_map
    player1.gamemap = engine.game_map
    player2.gamemap = engine.game_map
    
    engine.update_fov() #update the FOV for the first time ever 
    
    # engine = Engine(event_handler=event_handler, game_map=game_map, player=player0, player_characters=player_characters)

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

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
