from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT /"assets"

#Window
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60
TITLE = "University of Ibadan - Main Gate"
MAX_DT = 0.05  #made low so sprites don't teleport

#Road lanes
# ground_y is where the WHEELS touch the road (road surface is ~y=535..720).
# Traffic drives on the right: the near lane moves left->right, the far lane
# moves right->left.
FAR_LANE = dict(ground_y=600, direction=-1, depth_scale=0.85)
NEAR_LANE = dict(ground_y=675, direction=+1, depth_scale=1.00)


LANE_SPAWN_INTERVAL = (2.0, 5.0) #seconds between spawn attempts
LANE_MIN_SPAWN_GAP = 60 #Free space needed at the entry edge to spawn
LANE_SAFE_GAP = 130 # a follower starts matching the leader's speed               
LANE_BRAKE = 600 # px/s^2                  
LANE_ACCEL = 150 # px/s^2   



# faces = which way the ORIGINAL artwork points (+1 right, -1 left).
# The loader mirrors the sprite only when this differs from the lane direction.
VEHICLE_TYPES = [
    dict(name="car_red",      file="vehicles/car_red.png",      faces=+1, scale=1.00, speed=(190, 250), weight=3),
    dict(name="car_blue",     file="vehicles/car_blue.png",     faces=-1, scale=1.00, speed=(190, 250), weight=3),
    dict(name="danfo_yellow", file="vehicles/danfo_yellow.png", faces=-1, scale=1.25, speed=(150, 210), weight=3),
    dict(name="bus",          file="vehicles/bus.png",          faces=+1, scale=1.50, speed=(110, 150), weight=1),
]              