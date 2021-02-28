import pygame
from pygame.math import Vector2
from pygame.locals import *
import os.path
import sys

pygame.init()
pygame.display.set_caption('Dazzling Dash')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

filepath = os.getcwd()
track_image = pygame.image.load(os.path.join(filepath+"/images", "track.png")).convert_alpha()
REDCAR_ORIGINAL = pygame.image.load(os.path.join(filepath+"/images", "car.png")).convert_alpha()

click = False

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():

    while True:

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill(pygame.Color('darkgreen'))
        screen.blit(track_image, (0, 0))
        draw_text('Main Menu', font, pygame.Color('white'), screen, WIDTH/2 - 80, 120)

        button1 = pygame.Rect(WIDTH/2 - 140, 250, 300, 50)
        button2 = pygame.Rect(WIDTH/2 - 140, 350, 300, 50)
        button3 = pygame.Rect(WIDTH/2 - 140, 450, 300, 50)
        pygame.draw.rect(screen, pygame.Color('white'), button1)
        draw_text('Start', small_font, pygame.Color('black'), screen, WIDTH/2 - 6, 265)
        pygame.draw.rect(screen, pygame.Color('white'), button2)
        draw_text('Controls', small_font, pygame.Color('black'), screen, WIDTH/2 - 26, 365)
        pygame.draw.rect(screen, pygame.Color('white'), button3)
        draw_text('Exit', small_font, pygame.Color('black'), screen, WIDTH/2 - 6, 465)
        
        mx, my = pygame.mouse.get_pos()

        if button1.collidepoint((mx, my)):
            if click:
                game()

        if button2.collidepoint((mx, my)):
            if click:
                controls()

        if button3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def controls():

    controls_run = True

    while controls_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    controls_run = False

        screen.fill(pygame.Color('darkgreen'))
        screen.blit(track_image, (0, 0))
        back = pygame.Rect(WIDTH/2 - 140, 220, 300, 420)
        pygame.draw.rect(screen, pygame.Color('black'), back)
        draw_text('Controls', font, pygame.Color('white'), screen, WIDTH/2 - 60, 120)
        draw_text('W/UP - Accelerate', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 250)
        draw_text('S/DOWN - Brake & Reverse', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 300)
        draw_text('A/LEFT - Turn Left', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 350)
        draw_text('D/RIGHT - Turn Right', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 400)
        draw_text('SPACE - Handbrake    ', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 450)
        draw_text('E - Reset', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 500)
        draw_text('ESC - Main Menu', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 550)
        draw_text('Q - Quit', small_font, pygame.Color('white'), screen, WIDTH/2 - 120, 600)
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
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_ESCAPE:
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