import pygame
import random
import math
import time
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)


def main():

    lines = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #clear the screen
        screen.fill(BLACK)

        if any(pygame.mouse.get_pressed()):
            p1 = pygame.mouse.get_pos()
            while any(pygame.mouse.get_pressed()): pygame.event.get()
            while not any(pygame.mouse.get_pressed()): pygame.event.get()
            p2 = pygame.mouse.get_pos()
            while any(pygame.mouse.get_pressed()): pygame.event.get()
            lines.append((p1,p2))

        if len(lines) >= 1:
            for pair in lines:
                pygame.draw.line(screen, WHITE, pair[0], pair[1], 2)
        
        # flip() updates the screen to make our changes visible
        pygame.display.flip()
        
        # maintain framerate
        clock.tick(60)

    print(lines)
    
    pygame.quit()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen_size = (600, 600)
    
    # create a window
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("pygame Test")
    
    # clock is used to set a max fps
    clock = pygame.time.Clock()  
    main()