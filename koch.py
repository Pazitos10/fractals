#! /usr/bin/env python
# AXIOM = 'F' -> Koch Curve
# AXIOM = 'F--F--F' -> Koch Snowflake

import pygame
import math 
import os

WIDTH=1024
HEIGHT=768
GEN = 5 
ANGLE = 60
LENGTH_LINE = WIDTH//1.2
FACTOR = 3
AXIOM = 'F'
RULE = 'F+F--F+F'

white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

cursor = {'x': WIDTH//2 - LENGTH_LINE//6, 
          'y': HEIGHT//2 - LENGTH_LINE//10, 
          'angle': 0}

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
    running = 1

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        l = LENGTH_LINE
        for gen in range(GEN):
            screen.fill([0, 0, 0])
            #pygame.draw.line(screen, red, (0, HEIGHT/2), (WIDTH, HEIGHT/2)) # half screen line over X axis
            #pygame.draw.line(screen, green, (WIDTH/2, 0), (WIDTH/2, HEIGHT)) # half screen line over Y axis
            pygame.time.delay(500) #Delay to be able to see differences between generations 
            rule = generator(AXIOM, gen)
            l /= FACTOR 
            update_cursor(screen, white, cursor, rule, l)
            pygame.display.update()    
        
        pygame.display.flip()

if __name__ == '__main__':
    main_loop()