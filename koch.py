#! /usr/bin/env python
# AXIOM = 'F',  START_RULE = 'F',       RULE = 'F+F--F+F' -> Koch Curve
# AXIOM = 'F',  START_RULE = 'F--F--F', RULE = 'F+F--F+F' -> Koch Snowflake

import pygame
import math 
import os

WIDTH=640
HEIGHT=480
DELAY_MS = 500
GEN = 5 
ANGLE = 60
LENGTH_LINE = WIDTH / 0.6
FACTOR = 3

# AXIOMS = ['F']
# START_RULE = 'F--F--F'
# RULES = {'F': 'F+F--F+F'}

AXIOMS = ['A', 'B']
START_RULE = 'A'
RULES = {'A': 'ABA', 'B': 'BBB'}

offset_x = LENGTH_LINE / (FACTOR * 2)
offset_y = 0

cursor = {'x': WIDTH/2 - offset_x, 
          'y': HEIGHT/2 - offset_y, 
          'angle': 0, 
          'factor': FACTOR}

black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)

def generator(rule, gen=1):
    #Recursive function to replace the original axiom with rule (which changes over generations).
    if gen == 0:
        return rule
    else:
        rule_aux = ''
        for c in rule:
            i = AXIOMS.index(c)
            rule_aux += c.replace(AXIOMS[i], RULES[c])
        return generator(rule_aux, gen-1)

def update_cursor(screen, color, cursor, rule, l):
    #Updates cursor and draw the fractal
    cursor_aux = cursor.copy()
    for c in rule:
        color = white
        if c == 'F':
            cursor_aux['x'] = cursor['x'] + l * math.cos(math.radians(cursor['angle']))
            cursor_aux['y'] = cursor['y'] + l * math.sin(math.radians(cursor['angle']))
        if c == '+':
            cursor_aux['angle'] -=  ANGLE
        if c == '-':
            cursor_aux['angle'] +=  ANGLE
        if c == 'A' or c == 'B':
            cursor_aux['x'] = cursor['x'] + l
        if c == 'B':
            color = black
        
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
            pygame.time.delay(DELAY_MS) #Delay to be able to see differences between generations 
            rule = generator(START_RULE, gen)
            l /= cursor['factor'] 
            update_cursor(screen, white, cursor, rule, l)
            pygame.display.update()    
        
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()