from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
	from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):
	def __init__(self, engine: Engine):
		self.engine = engine
	
	def handle_events(self) -> None:
		for events in tcod.event.wait():
			action = self.dispatch(events)
			
			if action is None:
				continue
				# jump back up the loop and continue waiting for the player to input something
			action.perform()
			
			# advance time until the next time we need player input to continue
			self.engine.process_time()
			# update the FOV before the player's next action
			self.engine.update_fov()
			
	def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
		raise SystemExit()
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		action: Optional[Action] = None
		
		key = event.sym
		
		character = self.engine.player
		
		# numberpad movement keys
		if key == tcod.event.KeySym.KP_7:
			action = BumpAction(character, dx=-1, dy=-1)
		elif key == tcod.event.KeySym.KP_8:
			action = BumpAction(character, dx=0, dy=-1)
		elif key == tcod.event.KeySym.KP_9:
			action = BumpAction(character, dx=1, dy=-1)
		elif key == tcod.event.KeySym.KP_4:
			action = BumpAction(character, dx=-1, dy=0)
		# skip carefully over KP_5 for now
		elif key == tcod.event.KeySym.KP_6:
			action = BumpAction(character, dx=1, dy=0)
		elif key == tcod.event.KeySym.KP_1:
			action = BumpAction(character, dx=-1, dy=1)
		elif key == tcod.event.KeySym.KP_2:
			action = BumpAction(character, dx=0, dy=1)
		elif key == tcod.event.KeySym.KP_3:
			action = BumpAction(character, dx=1, dy=1)

		# switch controlled character
		

		elif key == tcod.event.KeySym.ESCAPE:
			action = EscapeAction(character)

		# if you made it here without a keypress, no valid key was pressed
		
		return action
