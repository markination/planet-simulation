import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math

angle_x = 0
angle_y = 0
last_x, last_y = 0, 0

def handle_mouse_movement():
    global angle_x, angle_y, last_x, last_y
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - last_x
    dy = mouse_y - last_y

    angle_x += dy * 0.1  
    angle_y += dx * 0.1  
    
    last_x, last_y = mouse_x, mouse_y

def apply_camera_rotation():
    glRotatef(angle_x, 1, 0, 0) 
    glRotatef(angle_y, 0, 1, 0) 

def update_orbit(planet, time_step):
    angle = time_step * planet.orbital_speed
    planet.x = planet.distance_sun * math.cos(angle)
    planet.z = planet.distance_sun * math.sin(angle)