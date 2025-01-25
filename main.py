import sys
sys.dont_write_bytecode = True
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from planet import Planet

pygame.init()

def draw_planet(planet):
    glMaterialfv(GL_FRONT, GL_DIFFUSE, planet.color)  
    glMaterialfv(GL_FRONT, GL_AMBIENT, (planet.color[0] * 1.2, planet.color[1] * 1.2, planet.color[2] * 1.2)) 

    glPushMatrix() 
    glTranslatef(
        planet.x / Planet.astronomical_unit,
        planet.y / Planet.astronomical_unit,
        planet.z / Planet.astronomical_unit  
    )
    
    quadric = gluNewQuadric()
    gluSphere(quadric, planet.radius / 1000, 50, 50)  
    gluDeleteQuadric(quadric)  
    
    glPopMatrix() 

    glBegin(GL_LINE_STRIP)
    for x, y, z in planet.orbit:  
        glVertex3f(
            x / Planet.astronomical_unit,
            y / Planet.astronomical_unit,
            z / Planet.astronomical_unit
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

def draw_text(text, position):
    font = pygame.font.Font(None, 36)  
    text_surface = font.render(text, True, (255, 255, 255))  
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    width, height = text_surface.get_size()
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glPushMatrix()
    glLoadIdentity()  
    glTranslatef(position[0], position[1], 0)  

    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(0, 0)
    glTexCoord2f(1, 1)
    glVertex2f(width, 0)
    glTexCoord2f(1, 0)
    glVertex2f(width, height)
    glTexCoord2f(0, 0)
    glVertex2f(0, height)
    glEnd()

    glPopMatrix()

def main():
    glutInit()  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    
    pygame.display.set_mode((800, 800), pygame.DOUBLEBUF | pygame.OPENGL)
    gluPerspective(45, 1, 0.1, 1000) 

    setup_lighting()
    glEnable(GL_DEPTH_TEST)

    sun = Planet(0, 0, 0, 30, (1, 1, 0), 1.98892 * 10**30)
    sun.is_sun = True

    earth = Planet(-1 * Planet.astronomical_unit, 0, 0, 16, (0, 0, 1), 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * Planet.astronomical_unit, 0, 0, 12, (1, 0, 0), 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = Planet(0.387 * Planet.astronomical_unit, 0, 0, 8, (0.4, 0.4, 0.4), 0.330 * 10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.astronomical_unit, 0, 0, 14, (1, 1, 1), 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

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
        
        earth_distance = f"Earth Distance: {earth.distance_sun / Planet.astronomical_unit:.2f} AU"
        
        glMatrixMode(GL_PROJECTION) 
        glPushMatrix()  
        glLoadIdentity() 
        glOrtho(0, 800, 800, 0, -1, 1)

        glMatrixMode(GL_MODELVIEW)  
        draw_text(earth_distance, (20, 20))  
        
        glMatrixMode(GL_PROJECTION) 
        glPopMatrix()  

        glMatrixMode(GL_MODELVIEW)  

        pygame.display.flip() 
        pygame.time.wait(10)

    pygame.quit()

main()