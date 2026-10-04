from functools import lru_cache
from typing import NamedTuple

import pygame

from .settings import ASSET_DIR

class Frame(NamedTuple):
    surface : pygame.Surface
    foot : int #y of the lowest visible pixel inside the surface
    
@lru_cache(maxsize=None)
def load_frame(rel_path: str, scale : float = 1.0, flip : bool = False) -> Frame :
    img = pygame.image.load(str(ASSET_DIR/rel_path)).convert_alpha()
    
    #scale the image if necessary
    if scale != 1.0 :
        size = (max(1, round(img.get_width() * scale)),
                max(1, round(img.get_height() * scale)))
        img = pygame.transform.smoothscale(img, size)
        
    if flip: 
        img = pygame.transform.flip(img, True, False)
        
    foot = img.get_bounding_rect(min_alpha=64).bottom
    return Frame(img, foot)

def load_background(rel_path : str) -> pygame.Surface:
    return pygame.image.load(str(ASSET_DIR / rel_path)).convert()
    