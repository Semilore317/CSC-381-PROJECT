import argparse
import os

def parse_args():
    p = argparse.ArgumentParser(description="UI main gate traffic animation")
    p.add_argument("--debug", action="store_true", help="start with the debug overlay on")
    p.add_argument("--headless", action="store_true", help="no window; for automated testing")
    p.add_argument("--frames", type=int, default=0, help="quit after N frames (0 = run until closed)")
    p.add_argument("--screenshot", default="", help="save the final frame to this path on exit")
    return p.parse_args()

def main():
    args = parse_args()
    if args.headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"   # must be set before pygame opens a display
        
    import pygame
    from game import settings as S
    from game.scene import Scene
    
    pygame.init()
    # TODO(sound): initialise the mixer here (pygame.mixer.init()) once audio files exist.
    screen = pygame.display.set_mode((S.SCREEN_W, S.SCREEN_H))
    pygame.display.set_caption(S.TITLE)
    clock = pygame.time.Clock()
    
    scene = Scene()
    # TODO(sound): start the looping background ambience here (distant traffic / campus noise).

    paused, debug, frame = False, args.debug, 0
    running = True
    while running:
        if args.headless:
            dt = 1 / S.FPS
        else:
            dt = min(clock.tick(S.FPS) / 1000, S.MAX_DT)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_F3:
                    debug = not debug
                elif event.key == pygame.K_s:
                    pygame.image.save(screen, "screenshot.png")
        if not paused:
            scene.update(dt)
        scene.draw(screen, debug=debug, fps=clock.get_fps())
        pygame.display.flip()

        frame += 1
        if args.frames and frame >= args.frames:
            running = False

    if args.screenshot:
        pygame.image.save(screen, args.screenshot)
    pygame.quit()
    

if __name__ == "__main__":
    main()
                

        