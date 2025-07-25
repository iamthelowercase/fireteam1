from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
	from entity import Entity
	from engine import Engine

class GameMap:
	def __init__(
		self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
	):
		self.engine = engine
		self.width, self.height = width, height # remember to change this line if you change the ordering on the console
		self.entities = set(entities)
		# self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
		self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F") #testing with an empty dungeon
		
		self.visible = np.full(
			(width, height), fill_value=False, order="F"
		) # tiles the player can see currently
		self.explored = np.full(
			(width, height), fill_value=False, order="F"
		) # tiles the player has seen before, but can't see currently
	
	def get_blocking_entity_at_location(
		self, location_x: int, location_y: int
	) -> Optional[Entity]:
		for entity in self.entities:
			if (
				entity.blocks_movement 
				and entity.x == location_x 
				and entity.y == location_y
			):
				return entity
		return None
	
	def in_bounds(self, x: int, y: int) -> bool:
		"""Return true if x and y are inside the bounds of this map."""
		return 0 <= x < self.width and 0 <= y < self.height
		# that is a gnarly inlined return but it's so good that it *is* inlined
	
	def render(self, console: Console) -> None:
		"""Renders the map.
		
		If a tile is in the "visible" array, then draw it with "light" icon and colors.
		If it isn't, but is in the "explored" array, then draw it with "dark" icon and colors.
		Otherwise, the default is "SHROUD".
		"""
		console.rgb[0:self.width, 0:self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD
		)
		
		for entity in self.entities:
			# only print the entities that are in the FOV
			if self.visible[entity.x, entity.y]:
				console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
