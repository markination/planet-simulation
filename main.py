import pygame
import math
from planet import Planet

pygame.init()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("planets simulator")
font = pygame.font.SysFont("comicsans", 16)

def main():
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10 ** 30) # is the sun even a planet or is it a star
    sun.is_sun = True

    earth = Planet(-1 * Planet.astronomical_unit, 0, 16 , (0, 0, 255), 5.9742 * 10 **24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * Planet.astronomical_unit, 0, 12, (255,0,0), 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = Planet(0.387 * Planet.astronomical_unit, 0, 8, (99,99,99), 0.330 * 10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.astronomical_unit, 0, 14, (255, 255, 255), 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    while running is True:


        clock.tick(60)
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(win)
        
        pygame.display.update()

    pygame.quit()



main()