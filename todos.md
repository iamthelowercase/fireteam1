# Next Steps
"Just plan out the next few baby steps"

* not exactly a baby step: work through the codebase and get moving multiple player-controlled characters around working
    * temporarily disable random dungeon generation.  Just give us a blank screen for now.
    * temporarily disable field of view -- we need to be able to see everything.
    * get multiple characters for the player to control showing up
    * figure out how an action to control which character the player can control could work, and implement that
    * once multiple characters controlled by the player are working, whip up a static test dungeon and generate in that, for testing future things
    * play with Field of View in the test dungeon, and get that working in a way we like
        * there are multiple algorithms to choose from, do we like any of them better than others?  Which do we like best?
        * is it working right with multiple PCs?
    * get semi random placement of PCs working in the test dungeon
    * since we're here, get the basics of the time system working.
    * *then* we can turn random dungeon generation back on.

## Study
* Play around with sets in the interactive interpreter.  Can you append to sets?  Are they accessed with a normal index like lists are?

# Future

## time system
"It is usually more straightforward to copy the collection or create a new collection" (python for programmers, 4.2)
* for entities in turn_order; if took action append took_action; else append no_action; end-of-tick append no_action took_action

## MOVEMENT
### Movement and UI
* The ability to move several characters under player control at once, as a block

## ROOMS AND FLOORS
* Create multiple types of floor generation systems
    * including a BSP-based floor generator
* create mulitple types of rooms to generate in room-based generation
* figure out where to put the decision between types of floor generation
* come up with multiple types of "non-rooms" (CF tunnels)
    * implement generation functions for them
    * refactor the basic tunnel function to dig really simple tunnels and one or more caller functions to use it
* Adjust the tunnel generation to eliminate those annoying "outside stair steps" on width-2 tunnels

## UI
* figure out how to handle control of multiple characters in a non-turn-based system
    * there are multiple possible control schemes.  Think of more than one, then compare them
* figure out how to *display* control of multiple characters
* Figure out how to uncouple *UI* display from *map* display

### UI AND WINDOWS
#### Goals
* Support maps that are larger than the window (for playing large maps on small windows)
* Support maps that are smaller than the window (for playing normal/small maps on large windows/monitors)
* Support automatically scaling the tileset when the window is resized
* Support setting a "base scaling" for the tileset independently of the window size
* Support scaling the tileset independently of the window size
* "Sticky" the UI to the window independently of the map

## SETPIECES
* Advancing under fire, explosions going off all around
* anything with a forward or assault squad, and a base-holding squad