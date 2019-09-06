from __future__ import division

import random
import time
from copy import deepcopy

import numpy as np


class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class vector_gwo_m:
    def __init__(self,sumo,min_bound,max_bound,dimension,n_point,iteration):
        self.sumo = sumo
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.Alpha = Agent(float("inf"), np.zeros(self.dimension))
        self.Beta = Agent(float("inf"), np.zeros(self.dimension))
        self.Delta = Agent(float("inf"), np.zeros(self.dimension))

        self.swarm = self.init_swarm()
        self.global_fitness_array=np.zeros(self.iteration)
    
    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            swarm.append(Agent(np.finfo(np.float32).max, position))
        return swarm

    def move_swarm(self): 
        for iter in range(self.iteration):     
            a = 2 * (1 - (iter**2 /self.iteration**2))
            for i in range(self.n_point):
                A1 = (2 * a * random.random()) - a
                C1 = 2 * random.random()
                A2 = (2 * a * random.random()) - a
                C2 = 2 * random.random()
                A3 = (2 * a * random.random()) - a
                C3 = 2 * random.random()
                # use numpy operation , so every dimension element can calculate together
                # it can imporve the proformance about 4 times.
                D_alpha = abs(C1 * self.Alpha.position - self.swarm[i].position)
                X1 = self.Alpha.position - A1 * D_alpha
                D_beta = abs(C2 * self.Beta.position - self.swarm[i].position)
                X2 = self.Beta.position - A2 * D_beta
                D_delta = abs(C3 * self.Delta.position - self.swarm[i].position)
                X3 = self.Delta.position - A3 * D_delta
                self.swarm[i].position = (X1 + X2 + X3) / 3
            
            for i in range(self.n_point):
                for j in range(self.dimension):
                    if(self.swarm[i].position[j]  > self.max_bound or self.swarm[i].position[j]  < self.min_bound):
                        self.swarm[i].position[j]  = np.random.uniform(self.min_bound, self.max_bound)

            self.sumo.sumo_multi_setting(self.swarm)
            for i in range(self.n_point):
                # Calculate objective function for each search agent
                self.swarm[i].fitness = self.sumo._getFitness_from_sumo(i)
                fitness = self.swarm[i].fitness
                
                if fitness <= self.Alpha.fitness:
                    self.Alpha = deepcopy(self.swarm[i])
                if(fitness > self.Alpha.fitness and fitness <= self.Beta.fitness):
                    self.Beta = deepcopy(self.swarm[i])
                if(fitness > self.Alpha.fitness and fitness > self.Beta.fitness and fitness < self.Delta.fitness):
                    self.Delta = deepcopy(self.swarm[i])

            self.global_fitness_array[iter]= self.Alpha.fitness

            print np.array(self.global_fitness_array)
        print np.array(self.Alpha.position)
        return self.global_fitness_array
