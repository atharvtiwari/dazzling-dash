import pygame
import pygame.freetype
from pygame.math import Vector2
import os.path

pygame.init()
clock = pygame.time.Clock()

WIDTH = 1152
HEIGHT = 648
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = pygame.Rect((0, 0),(WIDTH, HEIGHT))
filepath = os.path.dirname(__file__)

track_image = pygame.image.load(os.path.join(filepath+"/images", "track.png")).convert_alpha()


REDCAR_ORIGINAL = pygame.image.load(os.path.join(filepath+"/images", "car.png")).convert_alpha()
redangle = 0
redspeed = 0.0
pos_red = Vector2(210, 41)
vel_red = Vector2(redspeed, 0)

redcar = REDCAR_ORIGINAL

mask_red = pygame.mask.from_surface(redcar)
off_mask = pygame.mask.from_surface(track_image)
off_mask.invert()

font = pygame.freetype.SysFont(None, 42, True, True)
s=False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if redspeed >= 0.02:
        redspeed -= 0.02
    vel_red = Vector2(redspeed, 0)
    vel_red.rotate_ip(-redangle)
    redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
    mask_red = pygame.mask.from_surface(redcar)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if redspeed < 7:
            redspeed += 0.05
        vel_red = Vector2(redspeed, 0)
        vel_red.rotate_ip(-redangle)
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
        mask_red = pygame.mask.from_surface(redcar)
    
    if keys[pygame.K_DOWN]:
        if redspeed >= 0.10:
            redspeed -= 0.10
            vel_red = Vector2(redspeed, 0)
        vel_red.rotate_ip(-redangle)
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
        mask_red = pygame.mask.from_surface(redcar)

    elif keys[pygame.K_LEFT]:
        redangle += 2.5
        vel_red.rotate_ip(-2.5)
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
        mask_red = pygame.mask.from_surface(redcar)

    elif keys[pygame.K_RIGHT]:
        redangle -= 2.5
        vel_red.rotate_ip(2.5)
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
        mask_red = pygame.mask.from_surface(redcar)

    if (pos_red.x <= 0) or (pos_red.x >= WIDTH) or (pos_red.y <= 0) or (pos_red.y >= HEIGHT):
        redangle = 0
        redspeed = 0.0
        pos_red = Vector2(210, 41)
        vel_red = Vector2(redspeed, 0)
    
    pos_red += vel_red
    redcar_pos = list(int(v) for v in pos_red)

    offtrack = off_mask.overlap(mask_red, redcar_pos)

    screen.fill(pygame.Color('darkgreen'))
    screen.blit(track_image, (0, 0))

    if offtrack:
        redspeed = 0.5
        vel_red = Vector2(redspeed, 0)
        vel_red.rotate_ip(-redangle)
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle)
        mask_red = pygame.mask.from_surface(redcar)

    screen.blit(redcar, redcar_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
