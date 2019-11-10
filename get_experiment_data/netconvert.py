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

def netconvert(input_osmfile,output_netfile):
    sumoCmd = [checkBinary('netconvert'),"--osm-files",input_osmfile,"--output-file",output_netfile]
    subprocess.call(sumoCmd, stdout=sys.stdout, stderr=sys.stderr)

if __name__ == "__main__":
    check_sumo_version()
    
    input_osmfile = sys.argv[1]
    output_netfile = sys.argv[2]
    netconvert(input_osmfile,output_netfile)