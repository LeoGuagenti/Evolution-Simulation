import pyglet, random
from classes.environment.environment import Environment
from classes.environment.vegetation import Vegetation
from classes.predator.pred_body import PredatorBody
from classes.prey.prey import Prey
from utils.constants import *
from utils.general_utils import *

class Simulator:
    def __init__(self) -> None:
        print("[DEBUG] Starting Simulation.")
        self.window      = pyglet.window.Window(1280, 720)
        self.batch       = pyglet.graphics.Batch()
        self.prey_batch  = pyglet.graphics.Batch()
        self.env         = Environment(batch=self.batch)
        self.predators   = []
        self.prey        = []
        
        self.generate_prey()

        @self.window.event
        def on_draw():
            self.window.clear()
            pyglet.shapes.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color=(64, 47, 29)).draw()
            self.batch.draw()
            self.prey_batch.draw()
            
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol is pyglet.window.key.SPACE:
                self.predators.append(PredatorBody(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT), 5, color=(255, 0, 0), batch=self.batch))

        pyglet.clock.schedule_interval(self.update, 1/120.0)
        pyglet.app.run()

    def generate_prey(self):
        for i in range(PREY_COUNT):
            generate = True
            randx = random.randrange(SCREEN_WIDTH)
            randy = random.randrange(SCREEN_HEIGHT)
            for element in self.env.water_objects:
                if circles_touch(randx, randy, element.x, element.y, PREY_RAD+1, element.radius):
                   generate = False

            if generate is True:
                self.prey.append(Prey(
                    randx,                      # start position x
                    randy,                      # start position y
                    PREY_RAD,                   # size
                    random.uniform(3, 5),    # food repro threshold
                    random.uniform(1, 5),     # food repro cost   
                    random.randrange(5, 10),    # water repro threshold
                    random.randrange(1, 4),     # water repro cost
                    random.uniform(0.001, 0.009), # food loss rate
                    random.random() / 20,       # WATER loss rate
                    random.randrange(20, 40),          # speed
                    random.randrange(PREY_RAD+1, 20),   # view distance
                    random.uniform(0.0, 0.3),
                    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
                    batch=self.prey_batch               # render batch
                )) 

    def update_prey(self, dt):
        new_prey = []
        for i, prey in enumerate(self.prey):
            if prey.food_lvl <= 0:         
                # print(f'prey died of starvation at {(prey.x, prey.y)}')      
                # self.env.add_veg(prey.x, prey.y)
                del self.prey[i]
            
            # prey vs water
            for element in self.env.water_objects:
                if circles_touch(prey.x, prey.y, element.x, element.y, prey.radius, element.radius):
                    # turn away from water after drinking
                    prey.drink(1)
                    prey.look_direction = 30 + ((prey.look_direction + 180) % 360)
                    vx = 0 - math.cos(prey.look_direction) * 25
                    vy = 0 - math.sin(prey.look_direction) * 25
                    prey.x += vx * 1/30.0
                    prey.y += vy * 1/30.0

            distances = {}
            for veg in self.env.vegetation_objects:
                # prey vs vegetation
                if circles_touch(prey.x, prey.y, veg.x, veg.y, prey.radius, VEGETATION_RAD) and veg.alive is True:
                    prey.eat(GENERIC_FOOD_VALUE)
                    veg.unalive()

                # # prey vs visible vegetation
                # if circles_touch(prey.x, prey.y, veg.x, veg.y, prey.view_distance, VEGETATION_RAD):
                #     distances[math.dist((prey.x, prey.y), (veg.x, veg.y))] = i

            # if len(distances) > 0:
            #     prey.food_in_range = False
            #     keys = list(distances.keys())
            #     keys.sort()

            #     if keys[0] <= prey.view_distance:
            #         angle = math.atan2(
            #             abs(self.env.vegetation_objects[distances[keys[0]]].y-prey.y),
            #             abs(self.env.vegetation_objects[distances[keys[0]]].x-prey.x)
            #         )
            #         if prey.y > self.env.vegetation_objects[distances[keys[0]]].y:
            #             prey.look_direction = angle
            #         else:
            #             prey.look_direction = -angle
            #         # p1 = prey
            #         # p2 = self.env.vegetation_objects[distances[keys[0]]]
            #         # p3 = Object()
            #         # p3.x = 10
            #         # p3.y = 0 

            #         # d1 = math.sqrt(math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2))
            #         # d2 = math.sqrt(math.pow(p1.x - p3.x, 2) + math.pow(p1.y - p3.y, 2))
            #         # d3 = math.sqrt(math.pow(p2.x - p3.x, 2) + math.pow(p2.y - p3.y, 2))
            #         # val = math.pow(d1, 2) + math.pow(d2, 2) - math.pow(d3, 2) / (2*d1*d2)
            #         # print(val)
            #         # angle = math.acos(val)
            #         # prey.look_direction = angle
                    
            # else:
            #     prey.food_in_range = False

            # Prey Reproduction 
            if prey.food_lvl >= prey.food_repro_threshold:              
                prey.food_lvl -= prey.food_repro_cost
                prey.water_lvl -= prey.water_repro_cost
                rand_angle = random.random()*math.pi*2
                new_prey.append(Prey(
                    x                           = prey.x + math.cos(rand_angle) * prey.radius,
                    y                           = prey.y + math.sin(rand_angle) * prey.radius,
                    radius                      = PREY_RAD,
                    food_repro_threshold        = max(1, random.uniform(prey.food_repro_threshold - 0.1, prey.food_repro_threshold + 0.1)),
                    food_repro_cost             = abs(random.uniform(max(prey.food_repro_cost - 0.1, 5), prey.food_repro_cost + 0.2)), 
                    water_repro_threshhold      = random.randrange(5, 10),  
                    water_repro_cost            = random.randrange(4, 7),  
                    food_loss_rate              = max(0, random.uniform(max(prey.food_loss_rate - (0.4 / 20), 0.015), prey.food_loss_rate + (0.1/ 20))),  
                    water_loss_rate             = random.random(), 
                    speed                       = abs(random.randrange(prey.speed-5, prey.speed+5)),
                    view_distance               = abs(random.randrange(prey.view_distance-1, prey.view_distance+1)),
                    twitch_range                = random.uniform(prey.twitch_range-0.1, prey.twitch_range+0.1),
                    color                       = prey.color,
                    batch                       = self.prey_batch
                ))
            prey.update(dt)
        self.prey += new_prey
        
    def update(self, dt):
        for pred in self.predators:
            pred.update(dt)   

        self.update_prey(dt) 
        self.env.update()

        