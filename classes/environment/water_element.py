import pyglet

class WaterElement(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)