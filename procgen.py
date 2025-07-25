# class for containing all procedural-generation-specific code
# will eventually contain multiple floor generators

# TODO: update as per tutorial part 6 https://rogueliketutorials.com/tutorials/tcod/v2/part-6/

from __future__ import annotations

import random
from typing import Iterator, Iterable, Tuple, List, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
	from engine import Engine

class RectangularRoom:
	# defines a rectangular room, starting from the top left corner
	def __init__(self, x: int, y: int, width: int, height: int):
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height
	
	@property
	def center(self) -> Tuple[int,int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		# take a second to understand what that's doing and why that works
		return center_x, center_y
	
	@property
	def inner(self) -> Tuple[slice,slice]:
		"""Return the inner area of this room as a 2D array index."""
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
	
	def intersects(self, other: RectangularRoom) -> bool:
		"""Returns True if this room overlaps with another RectangularRoom"""
		return(
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def generate_dungeon(
	max_rooms: int,
	room_min_size: int,
	room_max_size: int,
	map_width: int,
	map_height: int,
	max_monsters_per_room: int,
	engine: Engine,
) -> GameMap:
	"""Generate a new dungeon map"""
	player = engine.player
	dungeon = GameMap(engine, map_width, map_height, entities=[player])
	
	rooms: List[RectangularRoom] = []
	
	for r in range(max_rooms):
		room_width = random.randint(room_min_size, room_max_size)
		room_height = random.randint(room_min_size, room_max_size)
		
		x = random.randint(0, dungeon.width - room_width - 1)
		y = random.randint(0, dungeon.height - room_height -1)
		
		new_room = RectangularRoom(x, y, room_width, room_height)
		
		# run through other rooms and see if they intersect with this one
		if any(new_room.intersects(other_room) for other_room in rooms):
			continue
		# if there are no intersections, we place the room
		
		# dig out the room
		dungeon.tiles[new_room.inner] = tile_types.floor
		
		if len(rooms) == 0:
			# the first room, where the player starts
			player.place(*new_room.center, dungeon)
		else: # all rooms after the first
			# dig a tunnel to connect this room and the previous one
			for x,y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor
		
		place_entities(new_room, dungeon, max_monsters_per_room)
		
		rooms.append(new_room)
	
	return dungeon

    # notes on monster types
    # troll = Entity(int(screen_width / 2 - 5), int(screen_height / 3), "T", (255, 255, 0))
    # zombie = Entity(int(screen_width / 2), int(screen_height / 2 - 5), "z", (0,255,255))

def place_entities(
	room: RectangularRoom, dungeon: GameMap, maximum_monsters: int,
	) -> None:
	number_of_monsters = random.randint(0, maximum_monsters)
	
	for i in range (number_of_monsters):
		x = random.randint(room.x1 + 1, room.x2 - 1)
		y = random.randint(room.y1 + 1, room.y2 - 1)
		
		if not any (entity.x == x and entity.y == y for entity in dungeon.entities):
			if random.random() < 0.8:
				entity_factories.zombie.spawn(dungeon, x, y)
			else:
				entity_factories.Troll.spawn(dungeon, x, y)

def tunnel_between(
	start: Tuple[int,int], end: Tuple[int,int]
	) -> Iterator[Tuple[int,int]]:
	"""Return an L-shaped tunnel between these two points."""
	x1, y1 = start
	x2, y2 = end
	
	
	
	if random.random() < 0.5:
		# end up moving horizontally, then vertically
		corner_x, corner_y = x2, y1
	else:
		# end up moving vertically, then horizontally
		corner_x, corner_y = x1, y2
	
	die = random.random() # set a temp var to a random value
	
	if die < 0.15: # start comparing the temp var to decide what size tunnel to dig
		# width 1 tunnel
		
		for x,y in simple_tunnel((x1, y1), (corner_x, corner_y)):
			yield x,y
		for x,y in simple_tunnel((corner_x, corner_y), (x2, y2)):
			yield x,y
		
	elif die < 0.5:
		# width 2 tunnel, type 1
		for x,y in simple_tunnel((x1, y1), (corner_x, corner_y)):
			yield x,y
		for x,y in simple_tunnel((corner_x, corner_y), (x2, y2)):
			yield x,y
		for x,y in simple_tunnel((x1 - 1, y1 - 1), (corner_x - 1, corner_y - 1)):
			yield x,y
		for x,y in simple_tunnel((corner_x - 1, corner_y - 1), (x2 - 1, y2 - 1)):
			yield x,y
	elif die < 0.85:
		# width 2 tunnel, type 2
		for x,y in simple_tunnel((x1, y1), (corner_x, corner_y)):
			yield x,y
		for x,y in simple_tunnel((corner_x, corner_y), (x2, y2)):
			yield x,y
		for x,y in simple_tunnel((x1 + 1, y1 + 1), (corner_x + 1, corner_y + 1)):
			yield x,y
		for x,y in simple_tunnel((corner_x + 1, corner_y + 1), (x2 + 1, y2 + 1)):
			yield x,y
	else:
		# width 3 tunnel
		for x,y in simple_tunnel((x1 - 1, y1 - 1), (corner_x - 1, corner_y - 1)):
			yield x,y
		for x,y in simple_tunnel((corner_x - 1, corner_y - 1), (x2 - 1, y2 - 1)):
			yield x,y
		for x,y in simple_tunnel((x1, y1), (corner_x, corner_y)):
			yield x,y
		for x,y in simple_tunnel((corner_x, corner_y), (x2, y2)):
			yield x,y
		for x,y in simple_tunnel((x1 + 1, y1 + 1), (corner_x + 1, corner_y + 1)):
			yield x,y
		for x,y in simple_tunnel((corner_x + 1, corner_y + 1), (x2 + 1, y2 + 1)):
			yield x,y
	

def simple_tunnel(
	start: Tuple[int,int], end: Tuple[int,int]
	) -> Iterator[Tuple[int,int]]:
	"""Return simple straight tunnel between these two points."""
	x1, y1 = start
	x2, y2 = end
	
	# generate the coordinates for this tunnel
	for x, y in tcod.los.bresenham((x1, y1), (x2, y2)).tolist():
		yield x, y

# def test_dungeon(
# 	max_rooms: int,
# 	room_min_size: int,
# 	room_max_size: int,
# 	map_width: int,
# 	map_height: int,
# 	max_monsters_per_room: int,
# 	player: Entity,
# 	player_characters: Iterable[Entity],
# ) -> GameMap:
# 	"""Generate a fixed dungeon specifically for testing purposes"""
# 	
