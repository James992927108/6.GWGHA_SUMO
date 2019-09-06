from __future__ import division

import random
from copy import deepcopy

import numpy as np


class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class goa:
    def __init__(self,sumo,min_bound,max_bound,dimension,n_point,iteration):
        self.sumo = sumo
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration
        
        self.l = 1.5
        self.f = 0.5
        self.cMax = 0.1
        self.cMin = 0.00004

        self.globle_point = Agent(np.finfo(np.float32).max ,  np.random.uniform(self.min_bound, self.max_bound,self.dimension))
        self.swarm = self.init_swarm()
        self.convergence_list=np.zeros(self.iteration)

    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound,self.dimension)
            swarm.append(Agent(np.finfo(np.float32).max, position))
        return swarm     

    # kernprof -l -v run.py  

    # @profile
    def move_swarm(self):
        for iter in range(self.iteration):
            # (2.8)            
            """ use grey wolf optimization """
            a = self.cMax - (iter * ((self.cMax - self.cMin) / self.iteration))              

            for i in range(self.n_point):
                # (2.7)
                for j in range(self.dimension):
                    self.swarm[i].position[j] = a * self.get_xi(i , a , j)  + self.globle_point.position[j]

            for i in range(self.n_point):
                for j in range(self.dimension):
                    if(self.swarm[i].position[j]  > self.max_bound or self.swarm[i].position[j]  < self.min_bound):
                        self.swarm[i].position[j]  = np.random.uniform(self.min_bound, self.max_bound)

            self.sumo.sumo_multi_setting(self.swarm)            
            for i in range(self.n_point):            
                self.swarm[i].fitness = self.sumo._getFitness_from_sumo(i)
                if self.swarm[i].fitness < self.globle_point.fitness:
                    self.globle_point = deepcopy(self.swarm[i])

            self.convergence_list[iter]= self.globle_point.fitness
            
            print np.array(self.convergence_list)
        return self.convergence_list , self.globle_point.position
        
    # @profile     
    def get_xi(self , i , a , j):
        temp = 0
        for point in range(self.n_point):
            if point != i:    
                r = np.sqrt(np.square(self.swarm[point].position[j] - self.swarm[i].position[j]))
                if r == 0:
                    r = 1
                r = (self.swarm[point].position[j] - self.swarm[i].position[j]) / r
                temp += a * ((self.max_bound - self.min_bound) / 2) * self.s_fun(r) * r  
        return temp
 
    # (2.3)
    # @profile
    def s_fun(self , r):
        part1 = self.f * np.exp((-r) / self.l)
        part2 = np.exp(-r)
        return part1 - part2
