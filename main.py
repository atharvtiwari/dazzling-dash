import pygame
from pygame.math import Vector2
from pygame.locals import *
import os.path
import sys

pygame.init() #initialization
pygame.display.set_caption('Dazzling Dash') #window title
clock = pygame.time.Clock() #clock
font = pygame.font.SysFont(None, 50) #font
small_font = pygame.font.SysFont(None, 30) #smaller font

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE|DOUBLEBUF, 32) #screen dimensions

filepath = os.getcwd() #directory of main.py
track_image = pygame.image.load(os.path.join(filepath+"/media", "track.png")).convert_alpha() #importing track image
REDCAR_ORIGINAL = pygame.image.load(os.path.join(filepath+"/media", "car.png")).convert_alpha() #importing car image
pygame.mixer.music.load(os.path.join(filepath+"/media", 'dsfs.mp3')) #importing music

pygame.mixer.music.play(-1, 0.0) #starts music

click = False

def draw_text(text, font, color, surface, x, y): #pygame print text to screen
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():

    while True:

        click = False

        for event in pygame.event.get(): #particular event cases
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
                if event.key == K_RETURN:
                    game()

        screen.fill(pygame.Color('darkgreen')) #background colour
        screen.blit(track_image, (0, 0)) #background image

        draw_text('Main Menu', font, pygame.Color('white'), screen, WIDTH/2 - 73, 95)
        draw_text('Press ENTER to begin', small_font, pygame.Color('red'), screen, WIDTH/2 - 90, 165)

        #defining buttons
        button1 = pygame.Rect(WIDTH/2 - 140, 250, 300, 50)
        button2 = pygame.Rect(WIDTH/2 - 140, 350, 300, 50)
        button3 = pygame.Rect(WIDTH/2 - 140, 450, 300, 50)
        pygame.draw.rect(screen, pygame.Color('white'), button1)
        draw_text('Start', small_font, pygame.Color('black'), screen, WIDTH/2 - 9, 265)
        pygame.draw.rect(screen, pygame.Color('white'), button2)
        draw_text('Controls', small_font, pygame.Color('black'), screen, WIDTH/2 - 30, 365)
        pygame.draw.rect(screen, pygame.Color('white'), button3)
        draw_text('Exit', small_font, pygame.Color('black'), screen, WIDTH/2 - 7, 465)
        
        mx, my = pygame.mouse.get_pos() #get position of cursor

        #defining cursor clicks 
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

        pygame.display.flip() #screen update
        clock.tick(60) #frames per second

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
        pygame.draw.rect(screen, pygame.Color('white'), back)

        draw_text('Controls', font, pygame.Color('white'), screen, WIDTH/2 - 60, 120)
        draw_text('W/UP - Accelerate', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 250)
        draw_text('S/DOWN - Brake & Reverse', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 300)
        draw_text('A/LEFT - Turn Left', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 350)
        draw_text('D/RIGHT - Turn Right', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 400)
        draw_text('SPACE - Handbrake    ', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 450)
        draw_text('E - Reset', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 500)
        draw_text('ESC - Main Menu', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 550)
        draw_text('Q - Quit', small_font, pygame.Color('black'), screen, WIDTH/2 - 120, 600)

        pygame.display.flip()
        clock.tick(60)

def score(laps, time):
    
    score_run = True

    while score_run:

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    score_run = False

        screen.fill(pygame.Color('darkgreen'))
        screen.blit(track_image, (0, 0))

        draw_text('Total laps: '+str(laps), small_font, pygame.Color('white'), screen, WIDTH/2 - 45, 95)
        draw_text('Average lap time: '+str(round(time, 2))+'s', small_font, pygame.Color('white'), screen, WIDTH/2 - 85, 165)

        button1 = pygame.Rect(WIDTH/2 - 140, 250, 300, 50)
        button2 = pygame.Rect(WIDTH/2 - 140, 350, 300, 50)
        pygame.draw.rect(screen, pygame.Color('white'), button1)
        draw_text('Restart', small_font, pygame.Color('black'), screen, WIDTH/2 - 20, 265)
        pygame.draw.rect(screen, pygame.Color('white'), button2)
        draw_text('Main Menu', small_font, pygame.Color('black'), screen, WIDTH/2 - 40, 365)
        
        mx, my = pygame.mouse.get_pos()

        if button1.collidepoint((mx, my)):
            if click:
                game()

        if button2.collidepoint((mx, my)):
            if click:
                main_menu()

        pygame.display.flip()
        clock.tick(60)

def game():

    redcar = REDCAR_ORIGINAL
    mask_red = pygame.mask.from_surface(redcar) #outline of car sprite
    off_mask = pygame.mask.from_surface(track_image) #outline of track sprite
    off_mask.invert() 

    redangle = 0 #initial angle
    redspeed = 0.0 #initial speed
    pos_red = Vector2(277, 87.5) #initial location w.r.t. top left corner
    vel_red = Vector2(redspeed, 0) #initial velocity vector

    counter = 0
    lap = 0 
    start_time = pygame.time.get_ticks()
    lap_time = 0
    total_time = 0
    avg_time = 0

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
                    score(lap, avg_time)
        
        vel_red = Vector2(redspeed, 0) #change length of velocity vector w.r.t. speed
        vel_red.rotate_ip(-redangle) #change direction of velocity vector w.r.t. angle
        redcar = pygame.transform.rotate(REDCAR_ORIGINAL, redangle) #rotate sprite w.r.t. angle
        mask_red = pygame.mask.from_surface(redcar) #update car outline

        #simple friction
        if redspeed >= 0.02:
            redspeed -= 0.02
        elif redspeed < -0.01:
            redspeed += 0.01
        else:
            redspeed = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]: #acceleration
            if redspeed <= 9.95:
                redspeed += 0.05
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: #brake and reverse
            if redspeed >= 0.1:
                redspeed -= 0.1
            elif redspeed >= -2.975:
                redspeed -= 0.025

        if keys[pygame.K_LEFT] or keys[pygame.K_a]: #steer left
            if vel_red.magnitude_squared() > 0.004:
                redangle += 3
                vel_red.rotate_ip(-3)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #steer right
            if vel_red.magnitude_squared() > 0.004:
                redangle -= 3
                vel_red.rotate_ip(3)
        
        if keys[pygame.K_SPACE]: #handbrake
            redspeed = 0

        if (pos_red.x <= 0) or (pos_red.x >= WIDTH) or (pos_red.y <= 0) or (pos_red.y >= HEIGHT) or keys[pygame.K_e]: #reset
            redangle = 0
            redspeed = 0
            pos_red = Vector2(277, 87.5)
            counter = 0
            start_time = pygame.time.get_ticks()
        
        pos_red += vel_red #update position of car w.r.t. velocity
        redcar_pos = list(int(v) for v in pos_red) #store position

        if redcar_pos[0] in range(650, 700) and redcar_pos[1] in range(290, 431): #checkpoint
            if vel_red[0] <= 0:
                counter = 1
            else:
                counter = 0

        if redcar_pos[0] in range(350,380) and redcar_pos[1] in range(70, 180): #lap finish
            if vel_red[0] >= 0:
                if counter == 1: #check if checkpoint crossed
                    lap += 1 #increase lap count
                    if start_time:
                        lap_time = (pygame.time.get_ticks() - start_time)/1000 #lap time
                        total_time += lap_time
                        avg_time = total_time / lap #average time per lap
                        start_time = pygame.time.get_ticks()
                    counter = 0
                else:
                    counter = 0
                    start_time = pygame.time.get_ticks()

        offtrack = off_mask.overlap(mask_red, redcar_pos) #grassy area

        screen.fill(pygame.Color('darkgreen'))
        screen.blit(track_image, (0, 0))

        if offtrack: #slowdown if offtrack
            if vel_red.magnitude_squared() > 0.25:
                if redspeed > 0:
                    redspeed -= 0.25
                else:
                    redspeed += 0.25

        if redspeed != 0:
            print(redcar_pos, vel_red) #console

        screen.blit(redcar, redcar_pos) #draw car on screen
        draw_text('laps: '+str(lap), small_font, pygame.Color('red'), screen, WIDTH - 140, 15) #display lap count
        draw_text('last lap time: '+str(round(lap_time, 2))+'s', small_font, pygame.Color('red'), screen, WIDTH - 220, 40) #display lap time
        pygame.display.flip()
        clock.tick(60)

main_menu() #start game with main menu
