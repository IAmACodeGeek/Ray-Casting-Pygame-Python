import math

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

WINDOW_HEIGHT = 480
WINDOW_WIDTH = WINDOW_HEIGHT * 2

FPS = 60

# The dimensions of the map is 8 by 8
MAP_DIMENSION = 12, 12

# Sizes of the tiles in the map
MAP_TILE_WIDTH = WINDOW_WIDTH / (2 * MAP_DIMENSION[0])
MAP_TILE_HEIGHT = WINDOW_HEIGHT / MAP_DIMENSION[1]

# The layout of the map is
MAP_LAYOUT = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
              [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
              [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
              [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# Player radius on map
PLAYER_RADIUS = MAP_TILE_WIDTH / 8

# Position of the player on the map
player_x = (WINDOW_WIDTH / 2) / 2 - 10
player_y = (WINDOW_HEIGHT / 2)

# Player direction angle
player_angle = math.pi / 2

# Field of vision of the player
PLAYER_FOV = math.pi / 3
PLAYER_HALF_FOV = PLAYER_FOV / 2

# Speed of the player
PLAYER_SPEED = MAP_TILE_WIDTH / 30

# Agular speed of rotation of the player
ROTATION_SPEED = 0.1

# No of rays to be casted or in other words no of column elements that will be in our 3d transformation
NO_OF_RAYS = WINDOW_WIDTH // (2 * 6) # Each column element in the 3d view will be six pixels wide

# Angle between the rays
STEP_ANGLE = PLAYER_FOV / NO_OF_RAYS

# Using Pythagoras theorem the maximum length of the ray can only be root two times the window height that is from one corner of the map to the other corner
MAX_RAY_LENGTH = int(2**0.5 * WINDOW_HEIGHT)

# The width of each column in the 3d view returned by each ray which hits a target
RAY_DISP_WIDTH = (WINDOW_WIDTH / 2) / NO_OF_RAYS

# Actual height of the walls
WALL_HEIGHT = 21000

# The line which shows the direction of the player in the map
DIR_RAY_LENGTH = 10

# Ray length increment length
RAY_STEP = 5