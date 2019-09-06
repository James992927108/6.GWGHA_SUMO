rm -r result/ output/
# export SUMO_HOME="/usr/local/src/sumo-0.30.0"
export SUMO_HOME="/mnt/c/sumo-0.30.0"
# export SUMO_HOME="/home/oslab/Desktop/sumo-0.30.0"
# export SUMO_HOME="/home/foroslab/Desktop/sumo-0.30.0"
# alameda rivadavia kaohsiung taichung taipei
map_list="rivadavia"
# 500 , 500second, 1000
road_list="500" 
# pso pso_TL spso2011 gwo goa 
# gwo_m gwogoaha_025
# gwgha_0 gwgha_025 gwgha_05 gwgha_075 gwgha_1
# gwogoaha_0 gwogoaha_025 gwogoaha_05 gwogoaha_075 gwogoaha_1
# gwgha_025_single
# gwgha_auto
algo_list="gwgha_auto"
roundtime=1
iteration=100
n_point=1

for map in $map_list;
do
    for road in $road_list;
    do
        for algo in $algo_list;
        do
            python run.py $map $road $roundtime $iteration $n_point $algo
        done
        # sleep 3600s
    done
done
