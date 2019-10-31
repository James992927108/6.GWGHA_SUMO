import numpy as np
import re
import ast
import os
import sys

def str2array(s):
    # Remove space after [
    s=re.sub('\[ +', '[', s.strip())
    # Replace commas and spaces
    s=re.sub('[,\s]+', ', ', s)
    return np.array(ast.literal_eval(s))

def read_txt(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    data = 0
    for index, i in enumerate(range(len(lines))):
        if i == 1:
            data = str2array(lines[i])
        if i % 2 == 1 and i != 1:
            data = np.concatenate((data, str2array(lines[i])), axis=0)
    return data

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


def classfity_data_txt_path(txt_path_list):   
    a_list = []
    r_list = []
    k_list = []
    tc_list = []
    tp_list = []

    for txt_path in txt_path_list:
        if txt_path.find("-a-") > 0 and txt_path.find("SimulateResult_List.txt") > 0:
            a_list.append(txt_path)
        if txt_path.find("-r-") > 0 and txt_path.find("SimulateResult_List.txt") > 0:
            r_list.append(txt_path)
        if txt_path.find("-k-") > 0 and txt_path.find("SimulateResult_List.txt") > 0:
            k_list.append(txt_path)
        if txt_path.find("-tc-") > 0 and txt_path.find("SimulateResult_List.txt") > 0:
            tc_list.append(txt_path)
        if txt_path.find("-tp-") > 0 and txt_path.find("SimulateResult_List.txt") > 0:
            tp_list.append(txt_path)
   
    return [a_list, r_list, k_list, tc_list, tp_list]

def concatenate_data(dataset_txt_path_list):
    data = 0
    for index, dataset_txt_path in enumerate(dataset_txt_path_list):
        sys.stdout.write("\rNumber of data %d / %d " % (index + 1, len(dataset_txt_path_list)))
        sys.stdout.flush()
        print dataset_txt_path
        if index == 0:
            data = read_txt(dataset_txt_path)
        else:
            data = np.concatenate((data, read_txt(dataset_txt_path)), axis=0)
        print data.shape
        # remove the same column
        data = np.unique(data,axis=0)
        print data.shape
    return data

if __name__ == "__main__":
    
    path = os.getcwd().split("/")[:-1]
    path = "/".join(path)
    path = path + "/draw/evlution/"
    txt_path_list = get_all_txt_path(path)
    dataset_txt_path_all_list = classfity_data_txt_path(txt_path_list)

    dataset_list = ['a','r','k','tc','tp']
    for index, dataset_txt_path_list in enumerate(dataset_txt_path_all_list):
        print "dataset: {}".format(dataset_list[index])
        data = concatenate_data(dataset_txt_path_list)
        print data.shape
        np.savetxt(dataset_list[index]+".csv", data, delimiter=",")
        print "success output"