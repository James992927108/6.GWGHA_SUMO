1.map.osm.xml -> map.net.xml
                
2.type.add.xml --------------->
                 map.net.xml -> map.rou.xml
                 map.net.xml -> map.add.xml
                 
First, google "openstreetmap" download map
Second, use python run "netconvert.py" get net.xml
    example:
    python netconvert.py "map.osm.xml" "map.net.xml"
Third, need create map.rou.xml, use randomTrips.py 
    example:
    python randomTrips.py  -n map.net.xml -r map.rou.xml -e 500 -p 0.74 --trip-attributes="departLane=\"best\" type=\"passenger\"" --additional-file type.add.xml
