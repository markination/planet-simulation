import math

class Planet:
    astronomical_unit = 149.6e6 * 1000
    gravitational_constant = 6.67428e-11
    timestep = 3600 * 24  

    def __init__(self, x, y, z, radius, color, mass):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.is_sun = False
        self.distance_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0
        self.z_velocity = 0

    def calculate_attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance_z = other.z - self.z
        distance = math.sqrt(distance_x**2 + distance_y**2 + distance_z**2)

        if other.is_sun:
            self.distance_sun = distance

        force = self.gravitational_constant * self.mass * other.mass / distance**2
        theta_xy = math.atan2(distance_y, distance_x)
        theta_z = math.atan2(distance_z, math.sqrt(distance_x**2 + distance_y**2))

        force_x = math.cos(theta_xy) * math.cos(theta_z) * force
        force_y = math.sin(theta_xy) * math.cos(theta_z) * force
        force_z = math.sin(theta_z) * force

        return force_x, force_y, force_z

    def update_position(self, planets):
        total_fx = total_fy = total_fz = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy, fz = self.calculate_attraction(planet)
            total_fx += fx
            total_fy += fy
            total_fz += fz

        self.x_velocity += total_fx / self.mass * self.timestep
        self.y_velocity += total_fy / self.mass * self.timestep
        self.z_velocity += total_fz / self.mass * self.timestep

        self.x += self.x_velocity * self.timestep
        self.y += self.y_velocity * self.timestep
        self.z += self.z_velocity * self.timestep

        self.orbit.append((self.x, self.y, self.z))