import pygame
import random
import math
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

def is_intersect(L1, L2):
    #intersection b/w line segments
    (x1,y1),(x2,y2) = L1
    (x3,y3),(x4,y4) = L2
    
    try:
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        u = ((x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    except:
        t=u=0

    px = x1 + t*(x2-x1)
    py = y1 + t*(y2-y1)

    return (0<t<=1 and 0<u<=1), (px,py)

def is_intersect2(pair1,pair2):
    # intersection b/w line and line segment
    (x1,y1),(x2,y2) = pair1
    (x3,y3),(x4,y4) = pair2

    try:
        px = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        py = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    except:
        return False, ()

    d1 = ((px-x4)**2 + (py-y4)**2) ** 0.5
    d2 = ((px-x3)**2 + (py-y3)**2) ** 0.5
    dl = ((x3-x4)**2 + (y3-y4)**2) ** 0.5

    eps = 1e-3

    # ensure point is on the correct side of the ray
    try:
        m1 = (y2-y1) / abs(x2-x1)
        m2 = (py-y1) / abs(px-x1)
    except:
        m1 = (y2-y1)
        m2 = (py-y1)

    if abs(m1)<eps:
        m1 = (x2-x1)
        m2 = (px-x1)
        
    return abs(dl-d1-d2) < eps and sgn(m1) == sgn(m2), (px,py)

def sgn(x):
    return ((x>=0) << 1) - 1


def main():

    # lines = [
    #     ((random.randint(100,500), random.randint(100,500)),
    #     (random.randint(100,500), random.randint(100,500))) for _ in range(15)]

    lines = [((77, 101), (79, 427)), ((43, 420), (216, 540)), ((236, 479), (498, 426)), ((73, 73), (351, 119)), ((199, 217), (212, 403)), ((160, 282), (351, 411)), ((295, 176), (566, 94)), ((479, 49), (554, 378)), ((18, 569), (585, 567)), ((585, 567), (582, 19)), ((582, 19), (21, 17)), ((21, 17), (18, 573))]

    p_pos = pygame.Vector2(surface_2d.get_rect().center)
    cam_angle = 0
    move_speed = 2
    angle_speed = 2
    FPS = 60

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #clear the screen
        surface_2d.fill(BLACK)
        surface_3d.fill(BLACK)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            cam_angle -= angle_speed/FPS
        if keys[pygame.K_d]:
            cam_angle += angle_speed/FPS

        m_dir = pygame.Vector2(math.cos(cam_angle), math.sin(cam_angle))
        if keys[pygame.K_w]:
            p_pos += m_dir * move_speed
        if keys[pygame.K_s]:
            p_pos -= m_dir * move_speed
    
        ## surface 2d

        rays = []
        # r_len = 200
        fov = 60
        for ang in range(-fov//2, fov//2):   
            ray = m_dir.rotate(ang)
            if ray.magnitude() > 0:
                # ray.scale_to_length(r_len)
                rays.append(ray)
        
        all_intersections = []

        for r in rays:
            intersections = []
            for L in lines: 
                pygame.draw.line(surface_2d, WHITE, L[0], L[1], 2) 
                res, p = is_intersect2((p_pos, p_pos+r),  L)
                if res:
                    intersections.append(p)

            sorted_intersections = sorted(intersections, key=lambda p: (p_pos[0]-p[0])**2 + (p_pos[1]-p[1])**2)
            if len(sorted_intersections)>0:
                pygame.draw.line(surface_2d, (100,100,100), p_pos, sorted_intersections[0], 1)
                pygame.draw.circle(surface_2d, RED, sorted_intersections[0], 5)
                all_intersections.append(pygame.Vector2(sorted_intersections[0] - p_pos))
            
        pygame.draw.circle(surface_2d, WHITE, p_pos, 10)

        ## surface 3d
        s3_rect = surface_3d.get_rect()
        for i in range(len(all_intersections)):
            euclid_d = all_intersections[i].magnitude()
            perp_d = euclid_d * all_intersections[i].normalize().dot(m_dir)
            c = min(1/perp_d * (1.5 * surface_3d.get_rect().w) * 20, 255)
            h = min(1/perp_d * (1.5 * surface_3d.get_rect().w) * 20, 300)
            pygame.draw.line(surface_3d, (c,)*3, 
                (s3_rect.w//fov*i,s3_rect.w//2+h//2), 
                (s3_rect.w//fov*i,s3_rect.w//2-h//2), 
                s3_rect.w//fov)

        # flip() updates the screen to make our changes visible
        screen.blit(surface_2d, (0,0))
        screen.blit(surface_3d, (screen_rect.w//2,0))
        pygame.display.flip()
        
        # maintain framerate
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    screen_size = (1200, 600)
    
    # create a window
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    surface_2d = pygame.Surface( (screen_rect.w//2, screen_rect.h) )
    surface_3d = pygame.Surface( (screen_rect.w//2, screen_rect.h) )
    pygame.display.set_caption("pygame Test")
    
    # clock is used to set a max fps
    clock = pygame.time.Clock()  
    main()