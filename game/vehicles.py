import random

import pygame

from . import settings as S 
from .assets import load_frame


class Vehicle:
    def __init__(self, spec : dict, lane : "Lane"):
        
        self.lane = lane
        self.spec_name = spec["name"] #e.g "bus"
        scale = spec["scale"] * lane.depth_scale
        self.frame = load_frame(spec["file"], scale, flip=lane.direction != spec["faces"])
        self.width = self.frame.surface.get_width()
        
        #make far lane slower
        self.base_speed = random.uniform(*spec["speed"]) * lane.depth_scale
        self.speed = self.base_speed
        
        # x is the CENTER of the sprite
        self.x = (-self.width / 2  -5) if lane.direction > 0 else (S.SCREEN_W + self.width/ 2 + 5)
        
    @property
    def sort_y(self) -> float:
        return self.lane.ground_y
    
    @property
    def off_screen(self) -> bool:
        if self.lane.direction > 0:
            return self.x - self.width / 2 > S.SCREEN_W
        return self.x + self.width / 2 < 0
    
    def update(self, dt : float) -> None:
        self.x += self.lane.direction * self.speed * dt
        
    def draw(self, screen : pygame.Surface) -> None:
        surf, foot = self.frame
        screen.blit(surf, (round(self.x - self.width / 2), round(self.lane.ground_y - foot)))
        
        
class Lane:
    def __init__(self, ground_y : int, direction : int, depth_scale : float):
        self.ground_y = ground_y
        self.direction = direction
        self.depth_scale = depth_scale
        self.vehicles : list[Vehicle] = [] # index 0 = furthest along
        self.spawn_timer = random.uniform(0.0, 1.5)
        self._weights = [t["weight"] for t in S.VEHICLE_TYPES]