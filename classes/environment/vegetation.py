import pyglet, random

class Vegetation(pyglet.shapes.Circle):
    def __init__(self, x, y, radius, food_value=None, color=..., batch=[], group=None):
        super().__init__(x, y, radius, color, batch, group)
        self.reserve_batch = batch
        self.alive = True 
        self.regen_chance = 1
        self.food_value = food_value

    def unalive(self):
        self.alive = False
        self.batch = None

    def try_regen(self):
        roll = random.randrange(0, 3000)
        if roll <= self.regen_chance:
            self.alive = True
            self.batch = self.reserve_batch

    def update(self):
        self.try_regen()

# diff type of veg that has higher food value and bright color (berries)