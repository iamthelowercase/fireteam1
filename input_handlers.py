from typing import Optional

import tcod.event

from actions import Action, EscapeAction, BumpAction


class EventHandler(tcod.event.EventDispatch[Action]):
	def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
		raise SystemExit()
	def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
		action: Optional[Action] = None
		
		key = event.sym
		
		# numberpad movement keys
		if key == tcod.event.KeySym.KP_7:
			action = BumpAction(dx=-1, dy=-1)
		elif key == tcod.event.KeySym.KP_8:
			action = BumpAction(dx=0, dy=-1)
		elif key == tcod.event.KeySym.KP_9:
			action = BumpAction(dx=1, dy=-1)
		elif key == tcod.event.KeySym.KP_4:
			action = BumpAction(dx=-1, dy=0)
		# skip carefully over KP_5 for now
		elif key == tcod.event.KeySym.KP_6:
			action = BumpAction(dx=1, dy=0)
		elif key == tcod.event.KeySym.KP_1:
			action = BumpAction(dx=-1, dy=1)
		elif key == tcod.event.KeySym.KP_2:
			action = BumpAction(dx=0, dy=1)
		elif key == tcod.event.KeySym.KP_3:
			action = BumpAction(dx=1, dy=1)

		# switch controlled character
		

		elif key == tcod.event.KeySym.ESCAPE:
			action = EscapeAction()

		# if you made it here without a keypress, no valid key was pressed
		
		return action
