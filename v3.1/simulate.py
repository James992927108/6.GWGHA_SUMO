from __future__ import division

import time
import random
import os
import shutil
import string
import subprocess
import sys
import numpy as np
import multiprocessing as mp
from xml.etree import ElementTree as ET

# import tensorflow as tf
# from tensorflow import Graph
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

def check_sumo_version():
    print os.environ.get("SUMO_HOME")
    sumoCmd = [checkBinary('sumo'), "-V"]
    subprocess.call(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)

def run_simulate(i, sumoCmd):
    # print('Run task %s ...' % i)
    subprocess.call(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)
    # print('Task %s finish ' % i)

def _getCr(i):
    tree = ET.parse("input/addfile/%d_osm.add.xml" % i)
    root = tree.getroot()
    Cr = 0
    for child in root.iter('phase'):
        duration = int(child.get('duration'))
        state = child.get('state').lower().translate(None, "y")
        if state != 0:
            r_count = state.count('r') if state.count('r') is not 0 else 1
            g_count = state.count('g')
            rate = g_count / r_count
            Cr += duration * rate
            # print "duration = {} , g_count = {} , r_count = {} , rate = {} Cr = {} , t_Cr = {}".format(duration , g_count , r_count , rate , duration * rate , Cr)
    return Cr

def creat_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

class simulate_sumo():
    def __init__(self, size, map, road):
        self.size = size
        self.original_file = "input/map/{}/copy_{}.add.xml".format(map, map)

        self.creat_InOut_file()
        self.sumocfg_file = "osm.sumocfg"
        
        net_file_path = "input/map/{}/{}.net.xml".format(map, map)
        route_file_path = "input/road/{}/{}{}.rou.xml".format(map, map, road)

        self.init_cfg_file(net_file_path, route_file_path)

    def init_cfg_file(self, net_file_path, route_file_path):
        """Used to rewrite the sumocfg file """
        tree = ET.parse(self.sumocfg_file)
        root = tree.getroot()
        for child in root.iter('net-file'):
            child.set('value', net_file_path)
        for child in root.iter('route-files'):
            child.set('value', route_file_path)
        tree.write(self.sumocfg_file)

    def get_p_dim(self):
        """ get how phase in map, usually is equal the dimension use in algorithm """
        tree = ET.parse(self.original_file)
        root = tree.getroot()
        size = 0
        for child in root.iter('phase'):
            checkhasyellow = string.find(child.get('state').lower(), 'y') != -1
            if checkhasyellow != 1:
                size += 1
        return size

    def creat_InOut_file(self):
        creat_folder("output")
        self.inputfile = []
        self.outputfile = []
        for i in range(self.size):
            self.inputfile.append("input/addfile/%d_osm.add.xml" % i)
            self.outputfile.append("output/%d_out.xml" % i)
            shutil.copyfile(self.original_file, self.inputfile[i])

    def _modify_add_xml_phase_duration(self, population_i, inputfile_i):
        tree = ET.parse(inputfile_i)
        root = tree.getroot()
        index = 0
        for child in root.iter('phase'):
            checkhasyellow = string.find(child.get('state').lower(), 'y') != -1
            if checkhasyellow == 1:
                child.set('duration', '5')
            else:
                child.set('duration', str(int(round(population_i[index]))))
                index += 1
        tree.write(inputfile_i)

    def sumo_single_setting(self, population_i):
        self._modify_add_xml_phase_duration(population_i, self.inputfile[0])
        sumoCmd = [checkBinary('sumo'), "-c", self.sumocfg_file, "-a",
                   self.inputfile[0], "--tripinfo-output", self.outputfile[0]]
        run_simulate(0, sumoCmd)

    def sumo_multi_setting(self, population):

        p = mp.Pool(self.size)
        for i in range(self.size):
            self._modify_add_xml_phase_duration(population[i] , self.inputfile[i])
            sumoCmd = [checkBinary('sumo'), "-c", self.sumocfg_file,
                       "-a", self.inputfile[i], "--tripinfo-output", self.outputfile[i]]
            p.apply_async(run_simulate, args=(i, sumoCmd))
            sys.stdout.flush()

        # close pool ,do not accept new task
        p.close()
        # let parent wait ,after child all have finish will open
        p.join()
        # print("all done")

    def _getSimulateResult_from_sumo(self, index):
        tree = ET.parse(self.outputfile[index])
        root = tree.getroot()

        complete_veh_duration_time = 0
        incomplete_veh_duration_time = 0
        total_veh_duration_time = 0

        complete_veh_num = 0
        incomplete_veh_num = 0

        waiting_time = 0
        simulationTime = 500
        carNum = 500

        for child in root.iter('tripinfo'):
            # vaporized = 0 mean vehicle's not finish on journey
            if child.get('arrival') != "-1.00":
                complete_veh_duration_time += float(child.get('duration'))
                complete_veh_num += 1
            waiting_time += int(child.get('waitSteps'))
            # SUMO Version 1.1.0 -> waiting_time, int -> float
            # SUMO Version 0.30.0 -> waitSteps

        incomplete_veh_num = carNum - complete_veh_num

        incomplete_veh_duration_time = incomplete_veh_num * simulationTime
        
        Cr = _getCr(index)
        sqar_complete_Veh_num = np.square(complete_veh_num)

        fitness = self.calFitness(complete_veh_duration_time, waiting_time, incomplete_veh_duration_time, Cr, sqar_complete_Veh_num)
        
        total_veh_duration_time = complete_veh_duration_time + incomplete_veh_duration_time

        return fitness, complete_veh_num, complete_veh_duration_time, incomplete_veh_duration_time, total_veh_duration_time, waiting_time

    def calFitness(self, complete_veh_duration_time, waiting_time, incomplete_veh_duration_time, Cr, sqar_complete_Veh_num):
        numerator = complete_veh_duration_time + waiting_time + incomplete_veh_duration_time
        denominator = sqar_complete_Veh_num + Cr
        fitness = numerator / denominator
        return fitness
    
class simulate_model():
    def load_model(self):

        self.md_complete_Veh_num = tf.contrib.keras.models.load_model(
            "model/complete_veh_num.h5")
        self.md_incomplete_Veh_num = tf.contrib.keras.models.load_model(
            "model/incomplete_veh_num.h5")
        self.md_complete_duration = tf.contrib.keras.models.load_model(
            "model/complete_veh_duration_time.h5")
        self.md_waiting_time = tf.contrib.keras.models.load_model(
            "model/waiting_time.h5")

    def _getFitness_from_model(self, p, i):
        simulationTime = 500
        sqar_complete_Veh_num = np.square(self.md_complete_Veh_num.predict(p))
        incomplete_veh_duration_time = self.md_incomplete_Veh_num.predict(
            p) * simulationTime
        Cr = _getCr(i)
        complete_veh_duration_time = self.md_complete_duration.predict(p)
        waiting_time = self.md_waiting_time.predict(p)
        fitness = self.calFitness(complete_veh_duration_time, waiting_time, incomplete_veh_duration_time, Cr, sqar_complete_Veh_num)
        return fitness
    
    def calFitness(self, complete_veh_duration_time, waiting_time, incomplete_veh_duration_time, Cr, sqar_complete_Veh_num):
        numerator = complete_veh_duration_time + waiting_time + incomplete_veh_duration_time
        denominator = sqar_complete_Veh_num + Cr
        fitness = numerator / denominator
        return fitness

if __name__ == "__main__":
    check_sumo_version()

    # alameda rivadavia kaohsiung
    map_name = "rivadavia"
    road_select = "500"
    n_point = 40
    FileName = "testdata/test_r_position.txt"

    sumo = simulate_sumo(size=n_point, map=map_name, road=road_select)
    print sumo.get_p_dim()
    data = np.array([x for x in open(FileName).read().split()]
                    ).astype(np.float)
    print np.array(data)
    sumo.sumo_single_setting(data)
    Result = sumo._getSimulateResult_from_sumo(0)
    print Result[0]
