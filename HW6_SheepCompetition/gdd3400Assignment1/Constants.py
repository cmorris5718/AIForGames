GAME_SPEED = 1

FRAME_RATE = 60
WORLD_WIDTH = 1024		# half 512
WORLD_HEIGHT = 768		# half 384
BACKGROUND_COLOR = (100, 149, 237)

# Graph Constants
GRID_SIZE = 16
NBR_RANDOM_OBSTACLES = 30
MIN_NBR_CLUMPED_OBSTACLES = 5
NBR_CLUMPED_OBSTACLES = 20

# Pen Constants
PEN_DEPTH = 160
PEN = [ [ [440, 312], [600, 312] ]  ]

# Dog Constants		  
DOG_HEIGHT = 32
DOG_WIDTH = 16
DOG_SPEED = 100 * GAME_SPEED
DOG_ANGULAR_SPEED = 1

# Sheep Constants
SHEEP_COUNT = 5
SHEEP_HEIGHT = 32
SHEEP_WIDTH = 16
SHEEP_SPEED = 100 * GAME_SPEED
SHEEP_ANGULAR_SPEED = .2
SHEEP_MIN_FLEE_DIST = 100

# Flocking Behavior Constants
SHEEP_NEIGHBOR_RADIUS = 50
SHEEP_BOUNDARY_RADIUS = 50
SHEEP_OBSTACLE_RADIUS = 50
SHEEP_ALIGNMENT_WEIGHT = 0.3
SHEEP_SEPARATION_WEIGHT = 0.325
SHEEP_COHESION_WEIGHT = 0.3
SHEEP_DOG_INFLUENCE_WEIGHT = 0.7
SHEEP_BOUNDARY_INFLUENCE_WEIGHT = 0.5
SHEEP_OBSTACLE_INFLUENCE_WEIGHT = 0.7

# General Debugging Constants
DEBUG_LINE_WIDTH = 1
DEBUGGING = True

# Graph Debugging
DEBUG_GRID_LINES = True
DEBUG_NEIGHBOR_LINES = False

# Agent Debugging
DEBUG_VELOCITY = True
DEBUG_BOUNDING_RECTS = True

# Sheep Debugging
DEBUG_BOUNDARIES = True
DEBUG_OBSTACLES = True
DEBUG_DOG_INFLUENCE = True
DEBUG_NEIGHBORS = True

# Dog Debugging
DEBUG_DOG_TARGET_LINE_WIDTH = 3
DEBUG_DOG_TARGET = True

