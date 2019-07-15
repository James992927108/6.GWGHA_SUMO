import math
import random
import sys
from copy import deepcopy

import numpy as np


class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class vector_goa:
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
        self.SimulateResult_List = []

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
            sys.stdout.write("\riter %d / %d , %f%%" % (iter + 1, self.iteration, (iter + 1) * 100 / self.iteration))
            sys.stdout.flush()
            # (2.8)            
            """ use grey wolf optimization """
            c = self.cMax - (iter * ((self.cMax - self.cMin) / self.iteration))              

            for i in range(self.n_point):
                # (2.7)
                self.swarm[i].position = deepcopy(c * self.get_xi(i , c) + self.globle_point.position)

            for i in range(self.n_point):
                for j in range(self.dimension):
                    if(self.swarm[i].position[j]  > self.max_bound or self.swarm[i].position[j]  < self.min_bound):
                        self.swarm[i].position[j]  = np.random.uniform(self.min_bound, self.max_bound)

            self.sumo.sumo_multi_setting([x.position for x in self.swarm])            
            for i in range(self.n_point):      
                result = self.sumo._getSimulateResult_from_sumo(i)   
                self.swarm[i].fitness = result[0]   
                if self.swarm[i].fitness < self.globle_point.fitness:
                    best_result = deepcopy(result)
                    self.globle_point = deepcopy(self.swarm[i])
            
                self.SimulateResult_List.append(best_result)
                
            self.convergence_list[iter]= self.globle_point.fitness
            # print np.array(self.convergence_list)
        return self.globle_point.position , self.SimulateResult_List
        
    # @profile     
    def get_xi(self , i , c):
        temp = np.zeros(self.dimension)
        for j in range(self.n_point):
            r = 0
            if j is not i:    
                r = np.sqrt(np.square(self.swarm[j].position - self.swarm[i].position))
                # r is vector , if element is 0 , i set value as 1
                r[r == 0] = 1
                r_vector = (self.swarm[j].position - self.swarm[i].position) / r
                temp += c * ((self.max_bound - self.min_bound) / 2) * self.s_fun(r) * r_vector
        return temp
 
    # (2.3)
    # @profile
    def s_fun(self , r):
        part1 = self.f * np.exp((-r) / self.l)
        part2 = np.exp(-r)
        return part1 - part2
