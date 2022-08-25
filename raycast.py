import pygame
import random
import math
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

def is_intersect(L1, L2):
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


def is_intersect_circle(L, center, r):

    def sgn(x):
        return ((x>=0) << 1) - 1

    cx, cy = center
    (x1,y1),(x2,y2) = L
    x1 -= cx # adjust for origin of circle
    x2 -= cx
    y1 -= cy
    y2 -= cy

    dx = x2-x1
    dy = y2-y1

    dr = (dx**2 + dy**2) ** 0.5

    D = x1*y2 - x2*y1

    eps = 1e-3

    points = []

    discriminant = r**2*dr**2 - D**2    
    if discriminant<0:
        return points  

    px1 = (D*dy + sgn(dy)*dx*(discriminant)**0.5) / dr**2
    px2 = (D*dy - sgn(dy)*dx*(discriminant)**0.5) / dr**2

    py1 = (-D*dx + abs(dy)*(discriminant)**0.5) / dr**2
    py2 = (-D*dx - abs(dy)*(discriminant)**0.5) / dr**2

    ## check if intersection point is within the line segment
    d11 = ((px1-x1)**2+(py1-y1)**2)**0.5
    d12 = ((px1-x2)**2+(py1-y2)**2)**0.5

    px1 += cx # un-adjust point from circle orgin
    py1 += cy

    if abs(dr-d11-d12) < eps:
        points.append((px1,py1))

    d21 = ((px2-x1)**2+(py2-y1)**2)**0.5
    d22 = ((px2-x2)**2+(py2-y2)**2)**0.5

    px2 += cx
    py2 += cy

    if abs(dr-d21-d22) < eps:
        points.append((px2,py2))

    return points


def main():

    lines = [
        ((random.randint(100,500), random.randint(100,500)),
        (random.randint(100,500), random.randint(100,500))) for _ in range(10)]
    
    circles = [
        ((random.randint(100,500), random.randint(100,500)), 
        random.randint(20,200)) for _ in range(2)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #clear the screen
        screen.fill(BLACK)

        m_pos = pygame.mouse.get_pos()

        rays = []
        r = 200
        n_rays = 50
        for ang in range(n_rays):
            rays.append((
                m_pos,
                (m_pos[0]+r*math.cos(2*math.pi/n_rays * ang),
                 m_pos[1]+r*math.sin(2*math.pi/n_rays * ang))
            ))

        for r in rays:
            pygame.draw.line(screen, (100,100,100), *r, 1)

            intersections = []
            for L in lines: 
                pygame.draw.line(screen, WHITE, L[0], L[1], 2) 
                res, p = is_intersect(r,  (L[0], L[1]))
                if res:
                    intersections.append(p)

            for circle in circles:
                pygame.draw.circle(screen, WHITE, *circle, 2)
                points = is_intersect_circle(r, *circle)
                for p in points:
                    intersections.append(p)

            sorted_intersections = sorted(intersections, key=lambda p: (m_pos[0]-p[0])**2 + (m_pos[1]-p[1])**2)
            if len(sorted_intersections)>0:
                pygame.draw.circle(screen, RED, sorted_intersections[0], 5)
            
        pygame.draw.circle(screen, BLACK, m_pos, 10)
        
        # flip() updates the screen to make our changes visible
        pygame.display.flip()
        
        # maintain framerate
        clock.tick(60)
    
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