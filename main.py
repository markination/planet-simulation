import sys
sys.dont_write_bytecode = True
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from planet import Planet
import numpy as np
pygame.init()

def render_text(text, x, y, z):
    """
    Render text using a pygame font and OpenGL texture.
    """
    font = pygame.font.Font(None, 50)
    img = font.render(text, True, (255, 255, 255))
    w, h = img.get_size()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    data = pygame.image.tostring(img, "RGBA", 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(x, y, z)
    glTexCoord2f(1, 0); glVertex3f(x + w, y, z)
    glTexCoord2f(1, 1); glVertex3f(x + w, y + h, z)
    glTexCoord2f(0, 1); glVertex3f(x, y + h, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)

    glDeleteTextures([texture])

def draw_planet(planet):
    glMaterialfv(GL_FRONT, GL_DIFFUSE, planet.color)  
    glMaterialfv(GL_FRONT, GL_AMBIENT, (planet.color[0] * 1.2, planet.color[1] * 1.2, planet.color[2] * 1.2)) 

    glPushMatrix() 
    glTranslatef(
        planet.x / (Planet.astronomical_unit * 2), 
        planet.y / (Planet.astronomical_unit * 2), 
        planet.z / (Planet.astronomical_unit * 2)  
    )
    
    quadric = gluNewQuadric()
    gluSphere(quadric, planet.radius / 1000, 50, 50)  
    gluDeleteQuadric(quadric)  
    
    glPopMatrix() 

    glBegin(GL_LINE_STRIP)
    for x, y, z in planet.orbit:  
        glVertex3f(
            x / (Planet.astronomical_unit * 2),  
            y / (Planet.astronomical_unit * 2), 
            z / (Planet.astronomical_unit * 2)  
        )
    glEnd()

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 1, 0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def main():
    glutInit()  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    
    screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, 1, 0.1, 1000) 

    setup_lighting()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    sun = Planet(0, 0, 0, 30, (1.0, 1.0, 0), 1.98892 * 10**30)  
    sun.is_sun = True
    sun.name = "Sun"

    earth = Planet(-1 * Planet.astronomical_unit, 0, 0, 16, (0.2, 0.4, 1.0), 5.9742 * 10**24)  
    earth.y_velocity = 29.783 * 1000
    earth.name = "Earth"
    earth.color_name = "BLUE"

    mars = Planet(-1.524 * Planet.astronomical_unit, 0, 0, 12, (1.0, 0.2, 0.2), 6.39 * 10**23)  
    mars.y_velocity = 24.077 * 1000
    mars.name = "Mars"
    mars.color_name = "RED"

    mercury = Planet(0.387 * Planet.astronomical_unit, 0, 0, 8, (0.6, 0.6, 0.6), 0.330 * 10**23) 
    mercury.y_velocity = -47.4 * 1000
    mercury.name = "Mercury"
    mercury.color_name = "GRAY"

    venus = Planet(0.723 * Planet.astronomical_unit, 0, 0, 14, (1.0, 1.0, 0.8), 4.8685 * 10**24)  
    venus.y_velocity = -35.02 * 1000
    venus.name = "Venus"
    venus.color_name = "WHITE"
    planets = [sun, earth, mars, mercury, venus]

    glTranslatef(0, -50, -50)  

    running = True
    while running:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glRotatef(0.1, 0, 1, 0) 

        for planet in planets:
            planet.update_position(planets) 
            draw_planet(planet)  

        render_text(f"Earth ({earth.color_name}): {earth.distance_sun / Planet.astronomical_unit:.2f} AU", 10, 10, 0)  
        render_text(f"Mars ({mars.color_name}): {mars.distance_sun / Planet.astronomical_unit:.2f} AU", 10, 40, 0)
        render_text(f"Mercury ({mercury.color_name}): {mercury.distance_sun / Planet.astronomical_unit:.2f} AU", 10, 70, 0)
        render_text(f"Venus ({venus.color_name}): {venus.distance_sun / Planet.astronomical_unit:.2f} AU", 10, 100, 0)

        y_offset = 250  
        pygame.display.flip() 
        pygame.time.wait(10)  

    pygame.quit()

main()