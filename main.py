import sys
sys.dont_write_bytecode = True
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from planet import Planet

pygame.init()

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
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) 
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0)) 
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0)) 
    glEnable(GL_DEPTH_TEST)  

def render_text_3d(text, x, y, z):
    glDisable(GL_LIGHTING)  
    glColor3f(1, 1, 1) 

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 800)  

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos3f(x, y, z)  
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))  

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)  

def draw_key(planets):
    render_text_3d("HELLO", -300, 300, -500)

    y_offset = 250
    for planet in planets:
        if not planet.is_sun:
            distance_text = f"{planet.name}: {planet.distance_sun / Planet.astronomical_unit:.2f} AU"
            render_text_3d(distance_text, -300, y_offset, -500)
            y_offset -= 30

def main():
    glutInit()  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    
    screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, 1, 0.1, 1000) 

    setup_lighting()
    glEnable(GL_DEPTH_TEST)

    sun = Planet(0, 0, 0, 30, (1, 1, 0), 1.98892 * 10**30)
    sun.is_sun = True
    sun.name = "Sun"

    earth = Planet(-1 * Planet.astronomical_unit, 0, 0, 16, (0, 0, 1), 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000
    earth.name = "Earth"

    mars = Planet(-1.524 * Planet.astronomical_unit, 0, 0, 12, (1, 0, 0), 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000
    mars.name = "Mars"

    mercury = Planet(0.387 * Planet.astronomical_unit, 0, 0, 8, (0.4, 0.4, 0.4), 0.330 * 10**23)
    mercury.y_velocity = -47.4 * 1000
    mercury.name = "Mercury"

    venus = Planet(0.723 * Planet.astronomical_unit, 0, 0, 14, (1, 1, 1), 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000
    venus.name = "Venus"

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
        
        draw_key(planets)

        pygame.display.flip() 
        pygame.time.wait(10)

    pygame.quit()

main()

