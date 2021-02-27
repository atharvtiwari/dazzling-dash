import pygame
from pygame.math import Vector2
from pygame.locals import *
import os.path

pygame.init()
pygame.display.set_caption('Dazzling Dash')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

filepath = os.getcwd()
track_image = pygame.image.load(os.path.join(filepath+"/images", "track.png")).convert_alpha()
REDCAR_ORIGINAL = pygame.image.load(os.path.join(filepath+"/images", "car.png")).convert_alpha()

def draw_text(text, font, color, size, surface, x, y):
    text_obj = font.render(text, size, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():

    menu_run = True
    while menu_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            game()

        if keys[pygame.K_q]:
            break

        screen.fill(pygame.Color('darkgreen'))
        draw_text('Main Menu', font, pygame.Color('white'), 2, screen, WIDTH/2, 50)
        pygame.display.flip()
        clock.tick(60)

def game():

    redcar = REDCAR_ORIGINAL
    mask_red = pygame.mask.from_surface(redcar)
    off_mask = pygame.mask.from_surface(track_image)
    off_mask.invert()

    redangle = 0
    redspeed = 0.0
    pos_red = Vector2(277, 87.5)
    vel_red = Vector2(redspeed, 0)

    game_run = True
    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
        
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

        if keys[pygame.K_ESCAPE]:
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
            pos_red = Vector2(277, 87.5)
        
        pos_red += vel_red
        redcar_pos = list(int(v) for v in pos_red)

        offtrack = off_mask.overlap(mask_red, redcar_pos)

        screen.fill(pygame.Color('darkgreen'))
        screen.blit(track_image, (0, 0))

        if offtrack:
            if vel_red.magnitude_squared() > 0.25:
                if redspeed > 0:
                    redspeed -= 0.25
                else:
                    redspeed += 0.25

        if redspeed != 0:
            print(pos_red, vel_red)

        screen.blit(redcar, redcar_pos)
        pygame.display.flip()
        clock.tick(60)

main_menu()

pygame.quit()