# Next Steps
"Just plan out the next few baby steps"

# Future
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

### UI AND WINDOWS
#### Goals
* Support maps that are larger than the window (for playing large maps on small windows)
* Support maps that are smaller than the window (for playing normal/small maps on large windows/monitors)
* Support automatically scaling the tileset when the window is resized
* Support setting a "base scaling" for the tileset independently of the window size
* Support scaling the tileset independently of the window size
* "Sticky" the UI to the window independently of the map
