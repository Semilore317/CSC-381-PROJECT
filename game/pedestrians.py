import math
import random
import pygame

from . import settings as S
from .assets import load_frame

class Pedestrian :
    def __init__(self, name : str, direction : int):
        self.direction = direction
        flip = direction < 0
        
        #two poses
        self.frames = [
            load_frame(f"pedestrians/{name}.png", S.PED_SCALE, flip),
            load_frame(f"pedestrians/{name}_walk2.png", S.PED_SCALE, flip),
        ]
        
        self.width = self.frames[0].surface.get_width()
        self.speed = random.uniform(*S.PED_SPEED)
        self.ground_y = random.randint(*S.PED_GROUND_Y)
        
        #random starting phase so two students strides never match
        self.distance = random.uniform(0, 2 * S.PED_STRIDE_PX)
        self.x = (-self.width / 2 -5) if direction > 0 else (S.SCREEN_W + self.width / 2 + 5)
        
    @property
    def sort_y(self) -> float :
        return self.ground_y
    
    @property
    def off_screen(self) -> bool :
        if self.direction > 0:
            return self.x - self.width / 2 > S.SCREEN_W
        return self.x + self.width / 2 < 0
    
    def update(self, dt : float) -> None:
        step = self.speed * dt
        self.x += self.direction * step
        self.distance += step
        
    def draw(self, screen : pygame.Surface) -> None:
        steps = self.distance / S.PED_STRIDE_PX
        frame = self.frames[int(steps) % len(self.frames)]
        #TODO(sound) : optional footsteps, A foot lands each time int(steps) changes
        #posibly skip in case walkers become too much
        
        lift = math.sin((steps % 1.0) *math.pi) * S.PED_BOB_PX
        surf, foot = frame
        screen.blit(surf, (round(self.x - self.width / 2), round(self.ground_y - foot - lift) ))


class PedestrianSpawner:
    def __init__(self)   :
        self.pedestrians : list[Pedestrian] = []
        self.timer = random.uniform(0.0, 1.0)
        
    def update(self, dt : float) -> None:
        self.timer -= dt
        if self.timer <= 0 and len(self.pedestrians) < S.PED_MAX:
            direction = random.choice((-1, 1))
            self.pedestrians.append(Pedestrian(random.choice(S.PED_NAMES), direction))
            self.timer = random.uniform(*S.PED_SPAWN_INTERVAL)
        elif self.timer <= 0:
            self.timer = 0.5  #cap rece
            
        for p in self.pedestrians:
            p.update(dt)
        self.pedestrians = [ p for p in self.pedestrians if not p.off_screen ]
        
    