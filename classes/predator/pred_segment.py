import pyglet, math
from utils.general_utils import circles_touch
from utils.constants import *

class PredatorSegment(pyglet.shapes.Circle):
    def __init__(self, x=None, y=None, radius=None, velocity_x=0.0, velocity_y=0.0, look_direction=None, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)
        
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.look_direction = look_direction
        self.child_segment = None     
        self.simulated_x = x
        self.simulated_y = y   

    def update(self, dt, parent_x, parent_y, parent_radius):
        if not circles_touch(parent_x, parent_y, self.simulated_x, self.simulated_y, parent_radius, self.radius):
            dy = self.simulated_y - parent_y
            dx = self.simulated_x - parent_x
            self.look_direction = math.atan2(dy, dx)

            self.velocity_x = 0 - math.cos(self.look_direction) * 25
            self.velocity_y = 0 - math.sin(self.look_direction) * 25

            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt
            self.simulated_x += self.velocity_x * dt
            self.simulated_y += self.velocity_y * dt

        if self.child_segment is not None:
           self.child_segment.update(
                dt=dt, 
                parent_x=self.simulated_x, 
                parent_y=self.simulated_y,
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

    def add_segment(self):
        if self.child_segment is None:
            self.child_segment = PredatorSegment(self.x, self.y+10, 5, self.velocity_x, self.velocity_y, color=self.color, batch=self.batch)
        else:
            self.child_segment.add_segment()

    def set_velocity(self, new_x, new_y):
        self.velocity_x = new_x
        self.velocity_y = new_y