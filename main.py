import pygame
from pygame.math import Vector2
from pygame.locals import *
import os.path

pygame.init()
pygame.display.set_caption('Dazzling Dash')
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)
fake_screen = screen.copy()

filepath = os.getcwd()
track_image = pygame.image.load(os.path.join(filepath+"/images", "track.png")).convert_alpha()
REDCAR_ORIGINAL = pygame.image.load(os.path.join(filepath+"/images", "car.png")).convert_alpha()

redangle = 0
redspeed = 0.0
pos_red = Vector2(277,87.5)
vel_red = Vector2(redspeed, 0)

redcar = REDCAR_ORIGINAL
mask_red = pygame.mask.from_surface(redcar)
off_mask = pygame.mask.from_surface(track_image)
off_mask.invert()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

    vel_red = Vector2(redspeed, 0)
    vel_red.rotate_ip(-redangle)
    redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
    mask_red = pygame.mask.from_surface(redcar)

    if redspeed >= 0.02:
        redspeed -= 0.02
    elif redspeed < -0.01:
        redspeed += 0.01
    else:
        redspeed = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        break

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if redspeed <= 9.95:
            redspeed += 0.05
    
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if redspeed >= 0.1:
            redspeed -= 0.1
        elif redspeed >= -2.975:
            redspeed -= 0.025

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if vel_red.magnitude_squared() > 0.004:
            redangle += 2.5
            vel_red.rotate_ip(-2.5)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if vel_red.magnitude_squared() > 0.004:
            redangle -= 2.5
            vel_red.rotate_ip(2.5)
    
    if keys[pygame.K_SPACE]:
        redspeed = 0

    if (pos_red.x <= 0) or (pos_red.x >= WIDTH) or (pos_red.y <= 0) or (pos_red.y >= HEIGHT) or keys[pygame.K_e]:
        redangle = 0
        redspeed = 0
        pos_red = Vector2(277,87.5)
    
    pos_red += vel_red
    redcar_pos = list(int(v) for v in pos_red)

    offtrack = off_mask.overlap(mask_red, redcar_pos)

    fake_screen.fill(pygame.Color('darkgreen'))
    fake_screen.blit(track_image, (0, 0))

    if offtrack:
        if vel_red.magnitude_squared() > 0.25:
            if redspeed > 0:
                redspeed -= 0.25
            else:
                redspeed += 0.25

    if redspeed != 0:
        print(pos_red, vel_red)

    fake_screen.blit(redcar, redcar_pos)
    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
