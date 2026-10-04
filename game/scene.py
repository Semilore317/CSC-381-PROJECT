import pygame

from . import settings as S 
from .assets import load_background
from .pedestrians import PedestrianSpawner
from .vehicles import Lane


class Scene:
    def __init__(self):
        self.background = load_background("background/ui_gate_day.png")
        self.lanes = [Lane(**S.FAR_LANE), Lane(**S.NEAR_LANE)]
        self.walkers = PedestrianSpawner()
        self._font = None
        
        #run the simulation forward so the very first frame already has traffic
        steps = int(S.PREWARM_SECONDS * 30)
        for _ in range(steps):
            self.update(1/30)
            
    def update(self, dt : float) -> None:
        for lane in self.lanes:
            lane.update(dt)
        self.walkers.update(dt)
        
    def _drawables(self):
        items = list(self.walkers.pedestrians)
        for lane in self.lanes:
            items.extend(lane.vehicles)
        return sorted(items, key=lambda o : o.sort_y)
    
    def draw(self, screen : pygame.Surface, debug: bool = False, fps: float = 0.0) -> None:
        screen.blit(self.background, (0, 0))
        for obj in self._drawables():
            obj.draw(screen)
        if debug:
            self._draw_debug(screen, fps)
            
    
    def _draw_debug(self, screen : pygame.Surface, fps : float) -> None:
        if self._font is None:
            self._font = pygame.font.SysFont(None, 22)
        y0, y1 = S.PED_GROUND_Y
        band = pygame.Surface((S.SCREEN_W, y1 - y0 + 1), pygame.SRCALPHA)
        band.fill((225, 200, 0, 60))
        screen.blit(band, (0, y0)) #yellow = pedestrian foot band
        for lane in self.lanes: #red lines = lane ground lines
            pygame.draw.line(screen, (225, 60, 60), (0, lane.ground_y), (S.SCREEN_W, lane.ground_y), 1)
        n_veh = sum(len(l.vehicles) for l in self.lanes)
        text = f"FPS {fps:4.0f}   vehicles {n_veh}   students {len(self.walkers.pedestrians)}"
        screen.blit(self._font.render(text, True, (255, 255, 255), (0, 0, 0)), (8, 8))
            
            
        