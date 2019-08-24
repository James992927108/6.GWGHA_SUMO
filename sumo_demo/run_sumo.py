import sys
import os
import subprocess
import numpy as np
from xml.etree import ElementTree as ET
import string

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


def vs_to_map_name(vs):
    return {
        'a':'alameda',
        'r':'rivadavia',
        'k':'kaohsiung',
        'tc':'taichung',
        'tp':'taipei',
        'undefined': 'undefined',
        }.get(vs,'undefined')

def map_name_to_vs(map_name):
        
    return {
        'alameda':'a',
        'rivadavia': 'r',
        'kaohsiung': 'k',
        'taichung': 'tc',
        'taipei': 'tp',
        'undefined': 'undefined',
    }.get(map_name, 'undefined')

class simulate_sumo_demo():
    def __init__(self, map, road, gui ,optimize):
        self.original_file = "input/map/{}/copy_{}.add.xml".format(map, map)

        self.sumocfg_file = "osm.sumocfg"
        
        net_file_path = "{}/{}.net.xml".format(map, map)
        route_file_path = "{}/{}{}.rou.xml".format(map, map, road)

        if optimize == "original":
            add_file_path = "{}/original_{}.add.xml".format(map, map)
        elif optimize == "optimize":
            position_file_path = "{}/Position.txt".format(map)
            position = self.read_position_txt(position_file_path)
            add_file_path = "{}/optimize_{}.add.xml".format(map, map)
            self._modify_add_xml_phase_duration(position, add_file_path)
        else:
            print "optimize error input use 'origin' as default"
            add_file_path = "{}/original_{}.add.xml".format(map, map)

        if gui == "gui":
            self.sumoCmd = [checkBinary('sumo-gui'), self.sumocfg_file]
        elif gui == "no_gui":
            self.sumoCmd = [checkBinary('sumo'), self.sumocfg_file]
        else:
            print "gui error input"
        

        self.init_cfg_file(net_file_path, route_file_path, add_file_path)

    def read_position_txt(self, position_file_path):
        poistion_list = []
        fo = open(position_file_path, "r")
        line = fo.read()
        for x in line.split():
            if x == "position" or x == ":":
                pass
            else:
                poistion_list.append(x.replace("[","").replace("]",""))
        poistion_list = filter(None, poistion_list)
        position = np.array(poistion_list).astype(np.float)
        return position

    def init_cfg_file(self, net_file_path, route_file_path, add_file_path):
        """Used to rewrite the sumocfg file """
        tree = ET.parse(self.sumocfg_file)
        root = tree.getroot()
        for child in root.iter('net-file'):
            child.set('value', net_file_path)
        for child in root.iter('route-files'):
            child.set('value', route_file_path)
        for child in root.iter('additional-files'):
            child.set('value', add_file_path)
        tree.write(self.sumocfg_file)
    
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

    def demo(self):
        subprocess.call(self.sumoCmd, stdout=sys.stdout, stderr=sys.stderr)

if __name__ == "__main__":
    # check_sumo_version()
    gui = str(sys.argv[1])
    map_name = str(sys.argv[2])
    road_select = str(sys.argv[3])
    optimize = str(sys.argv[4])
    sumo = simulate_sumo_demo(map = map_name, road = road_select, gui = gui, optimize = optimize)
    sumo.demo()

