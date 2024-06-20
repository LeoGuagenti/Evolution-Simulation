import pyglet
import numpy as np
import random, math
from utils.constants import *

class Prey(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, food_repro_threshold, food_repro_cost, water_repro_threshhold, water_repro_cost, food_loss_rate, water_loss_rate, speed, view_distance, twitch_range, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)

        # reproduction vars
        self.food_repro_threshold = food_repro_threshold
        self.food_repro_cost = food_repro_cost
        self.water_repro_threshhold = water_repro_threshhold
        self.water_repro_cost = water_repro_cost
        self.food_loss_rate = food_loss_rate
        self.water_loss_rate = water_loss_rate
        self.speed = speed
        self.view_distance = view_distance

        # movement
        self.look_direction = random.randrange(0, 360)
        self.velocity_x = 0 - math.cos(self.look_direction) * self.speed
        self.velocity_y = 0 - math.sin(self.look_direction) * self.speed
        self.twitch_range = 0.2
        self.look_indicator = pyglet.shapes.Line(self.x, self.y, self.x + (self.velocity_x/2), self.y + (self.velocity_y/2), 1, color=(0,0,0,255), batch=self.batch)
        self.view_indicator = pyglet.shapes.Circle(self.x, self.y, self.view_distance, color=(255, 255, 255, 55), batch=self.batch)

        # internal variables
        self.food_lvl = 2
        self.water_lvl = 2
        self.food_in_range = False

    def eat(self, value):
        self.food_lvl += value

    def drink(self, value):
        self.water_lvl += value

    def update_look_direction(self):
        # if self.food_in_range is True:
        self.look_direction += random.random() * (self.twitch_range - -self.twitch_range) + -self.twitch_range
        self.velocity_x = 0 - math.cos(self.look_direction) * self.speed
        self.velocity_y = 0 - math.sin(self.look_direction) * self.speed

    def update(self, dt):
        self.update_look_direction()
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if self.x > SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH
        
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

        self.look_indicator = pyglet.shapes.Line(self.x, self.y, self.x + (self.velocity_x), self.y + (self.velocity_y), 1, color=(0,0,0,255), batch=self.batch)
        self.view_indicator = pyglet.shapes.Circle(self.x, self.y, self.view_distance, color=(255, 255, 255, 55), batch=self.batch)
        self.food_lvl -= self.food_loss_rate
