import pygame
import random
import math
import numpy as np


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)


def compute_circle_sdf(circles, screen_dim):
    x_dim, y_dim = screen_dim
    res = np.zeros((y_dim, x_dim), dtype=np.float64)
    for x in range(x_dim):
        for y in range(y_dim):
            min_d = math.inf
            for c in circles:
                r, (cx,cy) = c
                d = ((x-cx)**2 + (y-cy)**2) ** 0.5 - r
                min_d = min(min_d, d)
            res[y,x] = min_d
    return res            


def draw_sdf_to_surf(sdf):
    sdf_surf = pygame.Surface((screen_rect.w, screen_rect.h))
    sdf_pixel_arr = pygame.PixelArray(sdf_surf)
    for y in range(sdf.shape[0]):
        for x in range(sdf.shape[1]):
            color = min(255, int(sdf[y,x] / 300 * 255))
            if color>=0:
                sdf_pixel_arr[x,y] = (color,)*3
            else:
                color = abs(color)
                sdf_pixel_arr[x,y] = (color, 0, 0)
    sdf_pixel_arr.close()

    return sdf_surf


def main():

    circles = [(random.randint(10,100),(random.randint(0,screen_rect.w),random.randint(0,screen_rect.h))) for _ in range(10)]
    player_pos = (screen_rect.w//2, screen_rect.h//2)
    dir_scale = 100
    eps = 1

    sdf_circles = compute_circle_sdf(circles, (screen_rect.w, screen_rect.h))
    sdf_surf = draw_sdf_to_surf(sdf_circles)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #clear the screen
        screen.fill(BLACK)

        screen.blit(sdf_surf, (0,0))

        mouse_pos = pygame.mouse.get_pos()

        if any(pygame.mouse.get_pressed()):
            player_pos = mouse_pos

        for c in circles:
            radius, center = c
            pygame.draw.circle(screen, WHITE, center, radius, width=3)

        pygame.draw.circle(screen, RED, player_pos, 5)

        v_mpos = pygame.Vector2(mouse_pos)
        v_ppos = pygame.Vector2(player_pos)

        v_pdir = v_mpos - v_ppos
        if any(v_pdir):
            v_pdir.normalize_ip()
        else:
            v_pdir = pygame.Vector2(1,0) #default

        march_radius = sdf_circles[player_pos[1], player_pos[0]]
        ray_pos = player_pos
        ray_march_data = []
        while march_radius > eps and (ray_pos[0]<screen_rect.w and ray_pos[1]<screen_rect.h and ray_pos[0]>0 and ray_pos[1]>0):
            march_radius = sdf_circles[int(ray_pos[1]), int(ray_pos[0])]
            ray_march_data.append((ray_pos,march_radius))
            ray_pos = (
                ray_pos[0] + (march_radius * v_pdir[0]),
                ray_pos[1] + (march_radius * v_pdir[1])
            )
        
        if len(ray_march_data):
            prev_pos, _ = ray_march_data[0]
        for i in range(1,len(ray_march_data)):
            (x,y), radius = ray_march_data[i]
            pygame.draw.line(screen, RED, (int(x),int(y)), prev_pos, 3)
            pygame.draw.circle(screen, RED, (int(x),int(y)), radius, 3)

            prev_pos = (int(x),int(y))
        
        # flip() updates the screen to make our changes visible
        pygame.display.flip()
        
        # maintain framerate
        clock.tick(60)
    
    pygame.quit()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen_size = (800, 600)
    
    # create a window
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("pygame Test")
    
    # clock is used to set a max fps
    clock = pygame.time.Clock()  

    main()