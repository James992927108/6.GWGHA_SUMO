import numpy as np
class result():
    def __init__(self,position,SimulateResult_List):
        self.convergence_list = np.asarray([x[0] for x in SimulateResult_List])
        
        self.min_fitness = min(self.convergence_list)
        self.position = position

        self.complete_veh_num_list = np.asarray([x[1] for x in SimulateResult_List])
        self.complete_veh_duration_time_list = np.asarray([x[2] for x in SimulateResult_List])
        self.incomplete_veh_duration_time_list = np.asarray([x[3] for x in SimulateResult_List])
        self.total_veh_duration_time_list = np.asarray([x[4] for x in SimulateResult_List])
        self.waiting_time_list =  np.asarray([x[5] for x in SimulateResult_List])

    def _get_convergence_list(self):
        return self.convergence_list
    
    def _get_min_convergence_list(self):
        return min(self.convergence_list)

    def _get_position(self):
        return self.position