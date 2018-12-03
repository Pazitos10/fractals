#! /usr/bin/env python
# AXIOM = 'F',  START_RULE = 'F',       RULE = 'F+F--F+F' -> Koch Curve
# AXIOM = 'F',  START_RULE = 'F--F--F', RULE = 'F+F--F+F' -> Koch Snowflake

import pygame
import math 
import os

WIDTH=640
HEIGHT=480
DELAY_MS = 500
GEN = 8 
ANGLE = 60
LENGTH_LINE = WIDTH/0.6
FACTOR = 3
AXIOM = 'F'
START_RULE = 'F--F--F'
#START_RULE = 'F'
RULE = 'F+F--F+F'

black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)

fs_in_rule = len([f for f in RULE if f == 'F'])
offset_x = LENGTH_LINE/(fs_in_rule+FACTOR-1)
offset_y = LENGTH_LINE/(ANGLE/(fs_in_rule+FACTOR-1))

cursor = {'x': WIDTH/2 - offset_x, 
          'y': HEIGHT/2 - offset_y, 
          'angle': 0, 
          'factor': FACTOR}

def generator(rule, gen=1):
    #Recursive function to replace the original axiom with rule (which changes over generations).
    if gen == 0:
        return rule
    else:
        return generator(rule.replace(AXIOM, RULE), gen-1)

def update_cursor(screen, color, cursor, rule, l):
    #Updates cursor and draw the fractal
    cursor_aux = cursor.copy()
    for c in rule:
        if c == 'F':
            cursor_aux['x'] = cursor['x'] + l * math.cos(math.radians(cursor['angle']))
            cursor_aux['y'] = cursor['y'] + l * math.sin(math.radians(cursor['angle']))
        if c == '+':
            cursor_aux['angle'] -=  ANGLE
        if c == '-':
            cursor_aux['angle'] +=  ANGLE
        
        pygame.draw.line(screen, color, (cursor['x'], cursor['y']), (cursor_aux['x'], cursor_aux['y']))
        cursor = cursor_aux.copy()

def main_loop():
    #Loops "infinitely" starting from axiom and applying rules until gen==GEN.
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    running = 1

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        l = LENGTH_LINE
        for gen in range(GEN):
            screen.fill(black)
            #pygame.draw.line(screen, red, (0, HEIGHT/2), (WIDTH, HEIGHT/2)) # half screen line over X axis
            #pygame.draw.line(screen, green, (WIDTH/2, 0), (WIDTH/2, HEIGHT)) # half screen line over Y axis
            pygame.time.delay(DELAY_MS) #Delay to be able to see differences between generations 
            rule = generator(START_RULE, gen)
            l /= cursor['factor'] 
            update_cursor(screen, white, cursor, rule, l)
            pygame.display.update()    
        
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()