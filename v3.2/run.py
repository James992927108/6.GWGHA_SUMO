from __future__ import division

import sys
import os
import time
import numpy as np

from datetime import datetime as dt
sys.dont_write_bytecode = True
from operator import attrgetter

from algo.pso.spso2011 import spso2011
from algo.pso.pso_TL import pso_TL
from algo.pso.pso import pso

from algo.goa.goa import goa
from algo.goa.vector_goa import vector_goa

from algo.gwo.gwogoaha_0 import gwogoaha_0
from algo.gwo.gwogoaha_025 import gwogoaha_025
from algo.gwo.gwogoaha_05 import gwogoaha_05
from algo.gwo.gwogoaha_075 import gwogoaha_075
from algo.gwo.gwogoaha_1 import gwogoaha_1

from algo.gwo.gwgha_0 import gwgha_0
from algo.gwo.gwgha_025 import gwgha_025
from algo.gwo.gwgha_05 import gwgha_05
from algo.gwo.gwgha_075 import gwgha_075
from algo.gwo.gwgha_1 import gwgha_1

from algo.gwo.gwgha_025_single import gwgha_025_single

from algo.gwo.gwo import gwo
from algo.gwo.gwo_m import gwo_m

from simulate import simulate_sumo

from result import result as rt

    
def write_file(file_name,value):
    fp = open(file_name, "a")
    fp.write(np.array2string(value))
    fp.close()

def creat_result_folder(directory):
    print "\n{}".format(directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def algo_map(algo_name):
    return {
        'pso':pso,
        'pso_TL': pso_TL,
        'spso2011': spso2011,
        'gwo': gwo,
        'goa': vector_goa,
        'gwgha_0': gwgha_0,
        'gwgha_025': gwgha_025,
        'gwgha_05': gwgha_05,
        'gwgha_075': gwgha_075,
        'gwgha_1': gwgha_1,
        'gwo_m': gwo_m,
        'gwogoaha_0': gwogoaha_0,
        'gwogoaha_025': gwogoaha_025,
        'gwogoaha_05': gwogoaha_05,
        'gwogoaha_075': gwogoaha_075,
        'gwogoaha_1': gwogoaha_1,
        'gwgha_025_single': gwgha_025_single,
    }.get(algo_name, 'gwo_mgoaha')

def map_name_vs(map_name):
        
    return {
        'alameda':'a',
        'rivadavia': 'r',
        'kaohsiung': 'k',
        'taichung': 'tc',
        'taipei': 'tp',
        'undefined': 'undefined',
    }.get(map_name, 'undefined')

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    """
    map :
        alameda , rivadavia , kaohsiung , taichung , taipei
    """
    map_name = sys.argv[1]
    """
    road :
        500 , 500second
    """
    road_select =  sys.argv[2]

    roundtime = int(sys.argv[3])

    iteration = int(sys.argv[4])
    n_point = int(sys.argv[5])

    min_bound = 5
    max_bound = 60
    
    sumo = simulate_sumo(size=n_point, map=map_name, road=road_select)
    dimension = sumo.get_p_dim()
    # model = simulate_model()
    print dimension

    """
    algo :
    pso_TL , spso2011
    goa , vector_goa

    gwogoaha , gwo_mgoaha

    gwo , gwo_m    
    """
    select_algo = algo_map(str(sys.argv[6]))

    Round_list = []
    start = time.time()

    map_name_vs = map_name_vs(map_name)

    foldername = "{}-{}-{}-{}-{}-{}-{}".format(select_algo.__name__,map_name_vs,road_select,roundtime,iteration,n_point,dt.now().strftime('%Y%m%d'))
    directory_path = "result/{}/{}/{}".format(map_name, road_select,foldername)
    creat_result_folder(directory_path)

    Round_evaluation_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_Round_evaluation")
    Round_position_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_Round_position")
    SimulateResult_List_txt = "{}/{}.txt".format(directory_path , select_algo.__name__ + "_SimulateResult_List")

    summary_txt = "{}/{}.txt".format(directory_path , select_algo.__name__ + "_summary")
    best_position_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_best_position")
    ave_convergence_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_convergence")
    ave_complete_veh_num_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_complete_veh_num")
    ave_complete_veh_duration_time_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_complete_veh_duration_time")
    ave_incomplete_veh_duration_time_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_incomplete_veh_duration_time")
    ave_total_veh_duration_time_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_total_veh_duration_time")
    ave_waiting_time_txt = "{}/{}.txt".format(directory_path, select_algo.__name__ + "_waiting_time")

    print("algo : {}").format(select_algo.__name__)

    for round in range(roundtime):
        print "\nRound: {}".format( round + 1)
        
        algo = select_algo(sumo, min_bound, max_bound, dimension, n_point, iteration)
        position , SimulateResult_List = algo.move_swarm()
        
        result = rt(position , SimulateResult_List)

        fp = open(Round_evaluation_txt, "a")
        fp.write("{}\n{}\n min : {} \n".format(round, np.array2string(result.evaluation_list),result.min_fitness))
        fp.close()
        fp = open(Round_position_txt, "a")
        fp.write("{}\n{}\n".format(round, np.array2string(result.position)))
        fp.close()
        
        fp = open(SimulateResult_List_txt, "a")
        fp.write("{}\n{}\n".format(round, SimulateResult_List))
        fp.close()
        
        Round_list.append(result)

    end = time.time()
    time_taken = (end - start)

    round_max = max(Round_list,key = attrgetter('min_fitness')).min_fitness
    round_ave = sum([Round_list[i].min_fitness for i in range(len(Round_list))]) / len(Round_list)
    round_min = min(Round_list,key = attrgetter('min_fitness')).min_fitness
    round_std = np.std([Round_list[i].min_fitness for i in range(len(Round_list))])
    
    fp = open(summary_txt, "a")
    fp.write("foldername : {}\n\n{}\n{}\n{}\n{} \n \ntime : {}\n".format(foldername, round_max, round_ave, round_min, round_std , time_taken))
    fp.close()

    best_position = min(Round_list,key = attrgetter('min_fitness')).position
    ave_convergence = sum([Round_list[i].convergence_list for i in range(len(Round_list))]) / len(Round_list)
    ave_complete_veh_num = sum([Round_list[i].complete_veh_num_list for i in range(len(Round_list))]) / len(Round_list)
    ave_complete_veh_duration_time = sum([Round_list[i].complete_veh_duration_time_list for i in range(len(Round_list))]) / len(Round_list)
    ave_incomplete_veh_duration_time = sum([Round_list[i].incomplete_veh_duration_time_list for i in range(len(Round_list))]) / len(Round_list)
    ave_total_veh_duration_time = sum([Round_list[i].total_veh_duration_time_list for i in range(len(Round_list))]) / len(Round_list)
    ave_waiting_time = sum([Round_list[i].waiting_time_list for i in range(len(Round_list))]) / len(Round_list)

    write_file(best_position_txt,best_position)
    write_file(ave_convergence_txt,ave_convergence)
    write_file(ave_complete_veh_num_txt,ave_complete_veh_num)
    write_file(ave_complete_veh_duration_time_txt,ave_complete_veh_duration_time)
    write_file(ave_incomplete_veh_duration_time_txt,ave_incomplete_veh_duration_time)
    write_file(ave_total_veh_duration_time_txt,ave_total_veh_duration_time)
    write_file(ave_waiting_time_txt,ave_waiting_time)

    print("\ncost time : {}".format(time_taken))

    # print np.array(best_position)
    # sumo.sumo_single_setting(best_position)
    # result = sumo._getSimulateResult_from_sumo(0)
    # print result


