import os
import sys
import subprocess
import numpy as np

def get_last_level_folder_path(path):
    dirPath_list = []
    for dirPath, dirNames, fileNames in os.walk(path):
        if dirNames == []:
            dirPath_list.append(dirPath)
    return sorted(dirPath_list)


def get_all_txt_path(path):
    txt_path_list = []
    dirPath_list = get_last_level_folder_path(path)
    for dirPath in dirPath_list:
        for f in os.listdir(dirPath):
            if f.find(".txt") > 0:
                txt_path_list.append(os.path.join(dirPath, f))
    return txt_path_list

def get_txt_context(txt_path):
    values = [float(value.replace('[','').replace(']','')) for value in open(txt_path).read().split(
    ) if filter(lambda ch: ch in '0123456789.', value) != ""]
    if "_complete_veh_num.txt" in txt_path:
        values = get_reconvergence_list(values)
    else:
        values = get_convergence_list(values)     
    return values

def get_convergence_list(values_list):
    temp_convergence_list = []
    temp = float("inf")
    for x in values_list:
        if x < temp:
            temp = x
        temp_convergence_list.append(temp)
    return np.asarray(temp_convergence_list)

def get_reconvergence_list(values_list):
    temp_convergence_list = []
    temp = 0
    for x in values_list:
        if x > temp:
            temp = x
        temp_convergence_list.append(temp)
    return np.asarray(temp_convergence_list)

def write_file(output_path, values):
    with open(output_path, "w") as det_file:
        for index, value in enumerate(values):
            det_file.write("{} {}\n".format(index, value))


def get_in_folder_algo_name(path):
    attributes_list = ["_best_position.dat",
                       "_complete_veh_duration_time.dat",
                       "_complete_veh_num.dat",
                       "_convergence.dat",
                       "_incomplete_veh_duration_time.dat",
                       "_Round.dat",
                       "_SimulateResult_List.dat",
                       "_summary.dat",
                       "_total_veh_duration_time.dat",
                       "_waiting_time.dat"]
    algo_name_list = []
    for f in os.listdir(path):
        algo_name = [f.replace(attr, "")
                     for attr in attributes_list if f.find(attr) > 0]
        if len(algo_name) == 1:
            algo_name_list.append(algo_name[0])
    return list(sorted(set(algo_name_list)))


def run_gnuplot():
    Cmd = ["gnuplot", "gpconfig.gp"]
    subprocess.call(Cmd, stdout=sys.stdout, stderr=sys.stderr)


def get_map_name(path):
    map_list = ["alameda",
                "kaohsiung",
                "rivadavia",
                "taichung",
                "taipei"]
    map_name = ""
    for map in map_list:
        if path.find(map) > 0:
            map_name = map
    return map_name


def get_road_name(path):
    road_list = ["500", "500second"]
    road_name = ""
    for road in road_list:
        if path.find(road) > 0:
            road_name = road
    return road_name


def get_title(path, gnuplot=False):
    if gnuplot == True:
        map_name = get_map_name(path)
        first_char = map_name[0].upper()
        last_char = map_name[1:]
        map_name = first_char + last_char
        title = map_name + "\\-" + get_road_name(path)
    else:
        title = get_map_name(path) + "_" + get_road_name(path)
    return title

def get_output_filename(path, title, attr):
    return os.path.join(path, (title + attr + ".pdf").replace(".dat", ""))


def draw_gnuplot(title, ylabel, output_filename, input_file_list, input_algo_name_list):
    modifty_gp_file(title, ylabel, output_filename,
                    input_file_list, input_algo_name_list)
    run_gnuplot()


def modifty_gp_file(title, ylabel, output_filename, input_file_list, input_algo_name_list):
    x_range = sum(1 for line in open(input_file_list[0]))
    print output_filename, x_range
    with open("gpconfig.gp", "w") as file:
        file.write("reset\n")
        file.write("set title font \",16\"\n")
        file.write("set title \"{}\"\n".format(title))
        file.write("set xlabel \"Evaluation\"\n")
        file.write("set ylabel \"{}\"\n".format(ylabel))
        file.write("set xrange [0:{}]\n".format(x_range))
        # file.write("set yrange [0.5:3]\n")
        file.write("set terminal pdf\n")
        file.write("set output \"{}\"\n".format(output_filename))

        file.write("set size 1.0,1.0\n")
        file.write("set pointsize 0.2\n")
        file.write("set ylabel offset character 1,0,0\n")
        file.write("set grid xtics ytics\n")

        file.write("set key outside horizontal center bottom Left reverse\n")
        file.write("set key spacing 1\n")
        file.write("set key width 2\n")

        file.write("set terminal pdf font \"Times New Roman, 12\"\n")
        # pt 7 pi -100
        # pt 2 pi -100
        # pt 4 pi -100
        # pt 6 pi -100
        # pt 8 pi -100
        if len(input_file_list) > 0:
            file.write(
                "set style line 1 lc rgb 'blue'     lt 1 lw 1 pt 7 pi -5000 ps 1\n")
        if len(input_file_list) > 1:
            file.write(
                "set style line 2 lc rgb 'red'      lt 1 lw 1 pt 2 pi -5000 ps 1\n")
        if len(input_file_list) > 2:
            file.write(
                "set style line 3 lc rgb 'green'    lt 1 lw 1 pt 4 pi -5000 ps 1\n")
        if len(input_file_list) > 3:
            file.write(
                "set style line 4 lc rgb 'black'    lt 1 lw 1 pt 6 pi -5000 ps 1\n")
        if len(input_file_list) > 4:
            file.write(
                "set style line 5 lc rgb 'orange'   lt 1 lw 1 pt 8 pi -5000 ps 1\n")

        if len(input_file_list) > 0:
            file.write("plot \"{}\" using 1:2 with linespoints title '   {}'   ls 1,\\\n".format(
                os.path.join(path, input_file_list[0]), input_algo_name_list[0]))
        if len(input_file_list) > 1:
            file.write("     \"{}\" using 1:2 with linespoints title '   {}'   ls 2,\\\n".format(
                os.path.join(path, input_file_list[1]), input_algo_name_list[1]))
        if len(input_file_list) > 2:
            file.write("     \"{}\" using 1:2 with linespoints title '   {}'   ls 3,\\\n".format(
                os.path.join(path, input_file_list[2]), input_algo_name_list[2]))
        if len(input_file_list) > 3:
            file.write("     \"{}\" using 1:2 with linespoints title '   {}'   ls 4,\\\n".format(
                os.path.join(path, input_file_list[3]), input_algo_name_list[3]))
        if len(input_file_list) > 4:
            file.write("     \"{}\" using 1:2 with linespoints title '   {}'   ls 5,\\\n".format(
                os.path.join(path, input_file_list[4]), input_algo_name_list[4]))
    file.close()


def get_input_file(path, algos, attr):
    input_file_list = []
    for algo in algos:
        input_file_list.append(os.path.join(path, algo+attr))
    return input_file_list

def get_ylabel(attr):
    if attr == "_convergence.dat":
        ylabel = "Fitness"
    elif attr == "_total_veh_duration_time.dat" or attr == "_waiting_time.dat":
        ylabel = "Seconds"
    elif attr == "_complete_veh_num.dat":
        ylabel = "Number of Vehicles"
    return ylabel


def algo_map(algo_name):
    return {
        'pso': "PSO",
        'pso_TL': "PSO\\_TL",
        'spso2011': "SPSO2011",
        'gwo': "GWO",
        'vector_goa': "GOA",
        'gwgha_0': "GWGHA",
        'gwgha_025': "GWGHA",
        'gwgha_05': "GWGHA",
        'gwgha_075': "GWGHA",
        'gwgha_1': "GWGHA",
        'gwo_m': "GWO\\_M",
        'gwogoaha_0': "GOA-GWO",
        'gwogoaha_025': "GOA-GWO",
        'gwogoaha_05': "GOA-GWO",
        'gwogoaha_075': "GOA-GWO",
        'gwogoaha_1': "GOA-GWO",
    }.get(algo_name, "GWGHA\\_M")


def get_input_algo_name(algo_name_list):
    input_algo_name_list = []
    for algo_name in algo_name_list:
        input_algo_name_list.append(algo_map(algo_name))
    return input_algo_name_list


attributes_list = [ "convergence.txt",
                    "complete_veh_num.txt",
                    "total_veh_duration_time.txt",
                    "waiting_time.txt"]

if __name__ == "__main__":
    path = os.getcwd()
    txt_path_list = get_all_txt_path(path)

    for index, txt_path in enumerate(txt_path_list):
        filename = str(txt_path.rsplit("/", 1)[1])
        for attributes in attributes_list:
            if filename.find(attributes) > 0:
                os.chmod(txt_path, 0o777) 
                sys.stdout.write("\r %d / %d , %f%%" % (index + 1, len(txt_path_list), (index + 1) * 100 / len(txt_path_list)))
                sys.stdout.flush()
                values = get_txt_context(txt_path)
                file_output_path = str(txt_path.rsplit(
                    "/", 2)[0])+"/"+str(txt_path).split("/")[-1].replace(".txt", ".dat")
                write_file(file_output_path, values)

    data = sorted(set([txt_path.rsplit("/", 2)[0] for txt_path in txt_path_list]))
    for index, path in enumerate(data):

        print "---------------------"
        attributes_list = [ "_convergence.dat",
                            "_complete_veh_num.dat",
                            "_total_veh_duration_time.dat",
                            "_waiting_time.dat"]
            
        algo_name_list = get_in_folder_algo_name(path)
        input_algo_name_list = get_input_algo_name(algo_name_list)
        # for i in input_algo_name_list:
        #     print i

        for attr in attributes_list:
            title = get_title(path, True)

            ylabel = get_ylabel(attr)
            output_filename = get_output_filename(path, get_title(path, False), attr)
            input_file_list = get_input_file(path, algo_name_list, attr)
    
            # for input in input_file_list:
            #     print input

            draw_gnuplot(get_title(path, True), ylabel,
                            output_filename, input_file_list, input_algo_name_list)
