
# 將環境加入到terminal中
# export SUMO_HOME="/mnt/c/sumo-0.30.0"

# Step 1
# python netconvert.py "map.osm.xml" "map.net.xml"

# Step 2
# python randomTrips.py  -n map/kaohsiung.net.xml -r map.rou.xml -e 500 -p 0.2 --trip-attributes="departLane=\"best\" type=\"passenger\"" --additional-file type.add.xml

# Step 3
# python check_car_num.py 1000

# Step 4
# python run_sumo.py 0