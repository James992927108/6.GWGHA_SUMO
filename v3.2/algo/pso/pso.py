from __future__ import division

import random

import numpy as np
import math
from copy import deepcopy

class Particle:
    def __init__(self, position, velocity):
        self.position = position         
        self.velocity = velocity          
        self.best_position = position        
        self.best_fitness = -1          
        self.fitnesses = -1            

class pso():
    def __init__(self, sumo, min_bound, max_bound, dimension, n_point, iteration):
        self.sumo = sumo
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.w = 1.0 / (2.0 * np.log(2.0))
        self.c1 = 0.5 + np.log(2.0)
        self.c2 = 0.5 + np.log(2.0)

        self.global_fitness = float("inf")
        self.global_position = np.zeros(self.dimension)
        
        self.convergence_list = np.zeros(self.iteration)
        self.SimulateResult_List = []

        self.swarm = self.init_swarm()

    def init_swarm(self):
        swarm = []
        for _ in range(0, self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            velocity = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            swarm.append(Particle(position, velocity))
        return swarm

    def move_swarm(self):
        for iter in range(self.iteration):

            for i in range(self.n_point):
                p = self.swarm[i]

                for j in range(self.dimension):
                    r1 = random.random()
                    r2 = random.random()

                    vel_cognitive = self.c1 * r1 * (p.best_position[j] - p.position[j])
                    vel_social = self.c2 * r2 * (self.global_position[j] - p.position[j])
                    p.velocity[j] = self.w * p.velocity[j] + vel_cognitive + vel_social
                    p.position[j] += p.velocity[j]
                    
                for j in range(self.dimension):
                    if p.position[j] > self.max_bound:
                        p.position[j] = np.random.uniform(self.min_bound, self.max_bound)
                        p.velocity[j] = np.random.uniform(self.min_bound, self.max_bound)
                    if p.position[j] < self.min_bound:
                        p.position[j] = np.random.uniform(self.min_bound, self.max_bound)
                        p.velocity[j] = np.random.uniform(self.min_bound, self.max_bound)

            self.sumo.sumo_multi_setting([x.position for x in self.swarm])

            for i in range(self.n_point):
                p = self.swarm[i]
                result = self.sumo._getSimulateResult_from_sumo(i)
                p.fitnesses = result[0]
                
                if p.fitnesses < p.best_fitness or p.best_fitness == -1:
                    p.best_position = p.position
                    p.best_fitness = p.fitnesses

                if p.fitnesses < self.global_fitness or self.global_fitness == -1:
                    self.global_position = deepcopy(p.position)
                    self.global_fitness = deepcopy(p.fitnesses)

            self.SimulateResult_List.append(result)
            self.convergence_list[iter] = self.global_fitness
            print np.array(self.convergence_list)
        return self.global_position, self.SimulateResult_List
