import sys
import os
import subprocess

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

def demo(gui):
    if gui == "1":
        sumoCmd = [checkBinary('sumo-gui'), "osm.sumocfg"]
    else:
        sumoCmd = [checkBinary('sumo'), "osm.sumocfg"]

    subprocess.call(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)

if __name__ == "__main__":
    check_sumo_version()
    gui = sys.argv[1]
    demo(gui)

