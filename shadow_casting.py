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

def is_intersect_circle(L, center, r):
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

    ## check if intersection is valid for the line segment (not just the infinite line)
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

    ## approach 1: cast out rays in 360 degrees - test for intersection
    ## approach 2: cast ray only to end points of lines (3 rays per vertex of slightly offset angle) - determine possible intersections for these rays - construct polygon from intersection points

    # lines = [
    #     ((random.randint(100,500), random.randint(100,500)),
    #     (random.randint(100,500), random.randint(100,500))) for _ in range(15)]

    lines = [((77, 101), (79, 427)), ((43, 420), (216, 540)), ((236, 479), (498, 426)), ((73, 73), (351, 119)), ((199, 217), (212, 403)), ((160, 282), (351, 411)), ((295, 176), (566, 94)), ((479, 49), (554, 378)), ((18, 569), (585, 567)), ((585, 567), (582, 19)), ((582, 19), (21, 17)), ((21, 17), (18, 573))]
    

    static_intersections = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            res, p = is_intersect(lines[i], lines[j])
            if res:
                static_intersections.append(p)

    points_of_interest = [p for L in lines for p in L] + static_intersections

    # circles = [
    #     ((random.randint(100,500), random.randint(100,500)), 
    #     random.randint(20,200)) for _ in range(5)
    # ]

    eps = 1

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
        n_rays = 100
        # for ang in range(n_rays):
        #     rays.append((
        #         m_pos,
        #         (m_pos[0]+r*math.cos(2*math.pi/n_rays * ang),
        #          m_pos[1]+r*math.sin(2*math.pi/n_rays * ang))
        #     ))
        for pairs in points_of_interest:
            # add line end points as well as slight CW and CCW rotated points (helps see around corner edges)
            ang = 1e-3
            px = pairs[0] - m_pos[0]
            py = pairs[1] - m_pos[1]
            rays.append( (m_pos, 
                ( (math.cos(ang)*px - math.sin(ang)*py) + m_pos[0], 
                  (math.sin(ang)*px + math.cos(ang)*py) + m_pos[1])) ) 
            rays.append( (m_pos, 
                ( (math.cos(-ang)*px - math.sin(-ang)*py) + m_pos[0], 
                (math.sin(-ang)*px + math.cos(-ang)*py) + m_pos[1] ) )) 
            rays.append( (m_pos, pairs))      

        all_intersections = []

        for r in rays:
            # pygame.draw.line(screen, (100,100,100), *r, 1)

            intersections = []
            for L in lines: 
                pygame.draw.line(screen, WHITE, L[0], L[1], 2) 
                # res, p = is_intersect(r,  L)
                res, p = is_intersect2(r, L)
                if res:
                    intersections.append(p)

            # for circle in circles:
            #     pygame.draw.circle(screen, WHITE, *circle, 2)
            #     points = is_intersect_circle(r, *circle)
            #     for p in points:
            #         intersections.append(p)

            sorted_intersections = sorted(intersections, key=lambda p: (m_pos[0]-p[0])**2 + (m_pos[1]-p[1])**2)
            if len(sorted_intersections)>0:
                # pygame.draw.circle(screen, RED, sorted_intersections[0], 5)
                all_intersections.append(sorted_intersections[0])
            
        pygame.draw.circle(screen, BLACK, m_pos, 10)

        # for p in static_intersections:
        #     pygame.draw.circle(screen, (0,255,0), p, 5)

        all_intersections = sorted(all_intersections, \
            key=lambda p: math.atan2((p[1]-m_pos[1]), (p[0]-m_pos[0])))
        pygame.draw.polygon(screen, (100,100,100), all_intersections)

        for L in lines: 
            pygame.draw.line(screen, WHITE, L[0], L[1], 2) 
        
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