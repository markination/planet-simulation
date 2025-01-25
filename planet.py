import math
import pygame
pygame.init()

class Planet:
    astronomical_unit = 149.6e6 * 1000
    gravitational_constant = 6.67428e-11
    scale = 200 / astronomical_unit 
    # each astronomical_unit is like 100 ish pixels

    timestep = 3600 * 24


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.is_sun = False
        self.distance_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, window, font):
        x = self.x * self.scale + 800 / 2 
        y = self.y * self.scale + 800 / 2

        if len(self.orbit) > 2:
            points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + 800 / 2
                y = y * self.scale + 800 / 2
                points.append((x, y))
            
            pygame.draw.lines(window, self.color, False, points, 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if not self.is_sun:
            distance_text = font.render(f"{round(self.distance_sun / 1000, 1)}km", 1, (255, 255, 255))
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
    def calculate_attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y **2)

        if other.is_sun:
            self.distance_sun = distance
        
        force_of_attraction = self.gravitational_constant * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force_of_attraction
        force_y = math.sin(theta) * force_of_attraction
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.calculate_attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * self.timestep
        self.y_velocity += total_fy / self.mass * self.timestep

        self.x += self.x_velocity * self.timestep
        self.y += self.y_velocity * self.timestep
        self.orbit.append((self.x, self.y))