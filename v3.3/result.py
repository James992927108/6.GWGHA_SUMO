import numpy as np
class result():
    def __init__(self,position,SimulateResult_List):
        self.position = position
        self.SimulateResult_List = SimulateResult_List

        self.evaluation_list = np.asarray([x[0] for x in SimulateResult_List])
        self.convergence_list = self.get_convergence_list()

        self.min_fitness = min(self.evaluation_list)

        self.complete_veh_num_list = np.asarray([x[1] for x in SimulateResult_List])
        self.complete_veh_duration_time_list = np.asarray([x[2] for x in SimulateResult_List])
        self.incomplete_veh_duration_time_list = np.asarray([x[3] for x in SimulateResult_List])
        self.total_veh_duration_time_list = np.asarray([x[4] for x in SimulateResult_List])
        self.waiting_time_list =  np.asarray([x[5] for x in SimulateResult_List])

    def get_convergence_list(self):
        temp_convergence_list = []
        temp = float("inf")
        for x in self.SimulateResult_List:
            if x[0] < temp:
                temp = x[0]
            temp_convergence_list.append(temp)
        return np.asarray(temp_convergence_list)
