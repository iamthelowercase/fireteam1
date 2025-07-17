from __future__ import annotations
from typing import Iterable, TYPE_CHECKING
import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
	from entity import Entity

class GameMap:
	def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
		self.width, self.height = width, height # remember to change this line if you change the ordering on the console
		self.entities = set(entities)
		self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
		
		self.visible = np.full((width, height), fill_value=False, order="F")
			# tiles the player can see currently
		self.explored = np.full((width, height), fill_value=False, order="F")
			# tiles the player has seen before, but can't see currently
	
	def in_bounds(self, x: int, y: int) -> bool:
		"""Return true if x and y are inside the bounds of this map."""
		return 0 <= x < self.width and 0 <= y < self.height
		# that is a gnarly inlined return but it's so good that it *is* inlined
	
	def render(self, console: Console) -> None:
		"""Renders the map.
		"""
		console.rgb[0:self.width, 0:self.height] = np.select(
			condlist=[self.visible, self.explored],
			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_types.SHROUD
		)
