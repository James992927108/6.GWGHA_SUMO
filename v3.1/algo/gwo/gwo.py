import random
import numpy as np
import time
from copy import deepcopy
import sys

class Agent:
    def __init__(self, fitness, position):
        self.fitness = fitness
        self.position = position

class gwo:
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
        self.convergence_list=np.zeros(self.iteration)
        
        self.SimulateResult_List = []
    
    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            swarm.append(Agent(np.finfo(np.float32).max, position))
        return swarm

    def move_swarm(self): 
        for iter in range(self.iteration):
            sys.stdout.write("\riter %d / %d , %f%%" % (iter + 1, self.iteration, (iter + 1) * 100 / self.iteration))
            sys.stdout.flush()

            a = 2 * (1 - (iter/self.iteration))
            for i in range(self.n_point):
                
                for j in range(self.dimension):
                    A1 = (2 * a * random.random()) - a
                    C1 = 2 * random.random()
                    A2 = (2 * a * random.random()) - a
                    C2 = 2 * random.random()
                    A3 = (2 * a * random.random()) - a
                    C3 = 2 * random.random()
                
                    D_alpha = abs(C1 * self.Alpha.position[j] - self.swarm[i].position[j]) 
                    X1 = self.Alpha.position[j] - A1 * D_alpha 
                    D_beta = abs(C2 * self.Beta.position[j] - self.swarm[i].position[j])
                    X2 = self.Beta.position[j] - A2 * D_beta    
                    D_delta = abs(C3 * self.Delta.position[j] - self.swarm[i].position[j])
                    X3 = self.Delta.position[j] - A3 * D_delta           
                    self.swarm[i].position[j] = ( X1 + X2 + X3 ) / 3
            
            for i in range(self.n_point):
                for j in range(self.dimension):
                    if(self.swarm[i].position[j] > self.max_bound or self.swarm[i].position[j] < self.min_bound):
                        self.swarm[i].position[j] = np.random.uniform(self.min_bound, self.max_bound)
            
            self.sumo.sumo_multi_setting([x.position for x in self.swarm])
            for i in range(self.n_point):
                result = self.sumo._getSimulateResult_from_sumo(i)
                self.swarm[i].fitness = result[0]
                fitness = result[0]
                if fitness <= self.Alpha.fitness:
                    best_result = deepcopy(result)
                    self.Alpha = deepcopy(self.swarm[i])
                if(fitness > self.Alpha.fitness and fitness <= self.Beta.fitness):
                    self.Beta = deepcopy(self.swarm[i])
                if(fitness > self.Alpha.fitness and fitness > self.Beta.fitness and fitness < self.Delta.fitness):
                    self.Delta = deepcopy(self.swarm[i])

                self.SimulateResult_List.append(best_result)
                
            self.convergence_list[iter]= self.Alpha.fitness
            # print np.array(self.convergence_list)
        return self.Alpha.position , self.SimulateResult_List
