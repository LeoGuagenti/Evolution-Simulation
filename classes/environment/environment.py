import random
import numpy as np
from shapely.geometry import Point, Polygon
from classes.environment.water_element import WaterElement
from classes.environment.vegetation import Vegetation
from utils.general_utils import *
from utils.constants import *

class Environment:
    def __init__(self, batch=None) -> None:
        print("[DEBUG] Initializing Environment.")
        self.water_objects      = []
        self.land_objects       = []
        self.vegetation_objects = []
        self.batch              = batch
    
        self.generate_water_elements()
        # self.generate_vegetation()

    def generate_water_elements(self):
        print("[DEBUG] Generating Water Elements.")
        # generates clusters of WaterElements with <= 'count' in the cluster
        def generate_water_cluster(count, mx, my, dx, dy):
            for i in range(count):
                x = random.gauss(mx, dx)    # x in cluster
                y = random.gauss(my, dy)    # y in cluster
                self.water_objects.append(WaterElement(x, y, random.randrange(WATER_ELEMENT_MIN_RAD, WATER_ELEMENT_MAX_RAD), color=(0, 0, 255, 255), batch=self.batch))

        # generate 'num_water_elements' clusters
        for i in range(WATER_ELEMENTS):
            generate_water_cluster(
                WATER_ELEMENT_CLUSTER_SIZE, 
                random.randrange(SCREEN_WIDTH), 
                random.randrange(SCREEN_HEIGHT), 
                random.randrange(15, 35), 
                random.randrange(15, 35)
            )


    def generate_vegetation(self):
        print("[DEBUG] Generating Vegetation.")
        # generates clusters of Vegetation with <= 'count' in the cluster
        def generate_vegetation_cluster(count, mx, my, dx, dy):
            for i in range(count):
                x = random.gauss(mx, dx)    # x in cluster
                y = random.gauss(my, dy)    # y in cluster

                # determine if point is in water
                for w_element in self.water_objects:
                    if not in_circle(w_element.x, w_element.y, w_element.radius, x, y):
                        self.add_veg(x, y)                    
               
        # generate 'num_vegetation' clusters
        for i in range(VEGETATION):
            generate_vegetation_cluster(
                VEGETATION_CLUSTER_SIZE, 
                random.randrange(SCREEN_WIDTH), 
                random.randrange(SCREEN_HEIGHT), 
                random.randrange(MIN_RANGE, MAX_RANGE), 
                random.randrange(MIN_RANGE, MAX_RANGE)
            )

    def add_veg(self, x, y):
        self.vegetation_objects.append(Vegetation(
            x, y, 
            VEGETATION_RAD, 
            GENERIC_FOOD_VALUE, 
            color=(34, 139, 34, 255), 
            batch=self.batch
        ))

    def update(self):
        for veg in self.vegetation_objects:
            veg.update()