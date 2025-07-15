# class for containing all procedural-generation-specific code
# will eventually contain multiple floor generators

from __future__ import annotations
import random
from typing import Iterator, Tuple, List, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
	from entity import Entity

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
	player: Entity,
) -> GameMap:
	"""Generate a new dungeon map"""
	dungeon = GameMap(map_width, map_height)
	
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
			player.x, player.y = new_room.center
		else: # all rooms after the first
			# dig a tunnel to connect this room and the previous one
			for x,y in tunnel_between(rooms[-1].center, new_room.center):
				dungeon.tiles[x, y] = tile_types.floor
		
		rooms.append(new_room)
	
	return dungeon

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
