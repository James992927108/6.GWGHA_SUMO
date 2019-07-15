# export SUMO_HOME="/usr/local/src/sumo-0.30.0"
export SUMO_HOME="/mnt/d/sumo-0.30.0"
# export SUMO_HOME="/home/oslab/Desktop/sumo-0.30.0"
# alameda rivadavia kaohsiung taichung taipei
map_list="alameda rivadavia kaohsiung taichung taipei"
road_list="500" 
# pso pso_TL spso2011 gwo goa 
# gwo_m gwogoaha
# gwgha_0 gwgha_025 gwgha_05 gwgha_075 gwgha_1
algo_list="pso_TL spso2011 gwo goa gwgha_025"
roundtime=1
iteration=750
n_point=40

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
