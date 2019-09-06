export SUMO_HOME="/mnt/c/sumo-0.30.0"
# python netconvert.py "map.osm.xml" "map.net.xml"
# python randomTrips.py  -n map/kaohsiung.net.xml -r map.rou.xml -e 500 -p 0.2 --trip-attributes="departLane=\"best\" type=\"passenger\"" --additional-file type.add.xml
# check_500.py need to run multi time
python check_500.py 1000
# python run_sumo.py 0