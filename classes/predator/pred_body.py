import pyglet, math, random
from classes.predator.pred_segment import PredatorSegment
from utils.constants import *

class PredatorBody(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)
        
        self.look_direction = random.randrange(0, 360)
        self.velocity_x = 0 - math.cos(self.look_direction)*25
        self.velocity_y = 0 - math.sin(self.look_direction)*25
        self.look_indicator = pyglet.shapes.Line(self.x, self.y, self.x + self.velocity_x, self.y + self.velocity_y, 3, color=(0,0,0,255), batch=self.batch)
        self.twitch_range = 0.4
        self.water_lvl = 0
        self.food_lvl = 59
        self.child_segment = None
        
    
    def update_look_direction(self):
        self.look_direction += random.random() * (self.twitch_range - -self.twitch_range) + -self.twitch_range
        self.velocity_x = 0 - math.cos(self.look_direction)*25
        self.velocity_y = 0 - math.sin(self.look_direction)*25

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.update_look_direction()

        if self.food_lvl > 5:
            self.food_lvl -= 3
            self.add_segment()

        if self.child_segment is not None:
            self.child_segment.update(
                dt=dt, 
                parent_x=self.x, 
                parent_y=self.y,
                parent_radius=self.radius
            )

        if self.x > SCREEN_WIDTH:
            self.x = 0
        elif self.x <= 0:
            self.x = SCREEN_WIDTH
        
        if self.y > SCREEN_HEIGHT:
            self.y = 0
        elif self.y <= 0:
            self.y = SCREEN_HEIGHT

        self.look_indicator = pyglet.shapes.Line(self.x, self.y, self.x + (self.velocity_x/2), self.y + (self.velocity_y/2), 1, color=(0,0,0,255), batch=self.batch)

    def add_segment(self):
        if self.child_segment is None:
            self.child_segment = PredatorSegment(self.x, self.y+10, 5, self.velocity_x, self.velocity_y, color=self.color, batch=self.batch)
        else:
            self.child_segment.add_segment()

    def draw(self):
        return super().draw()