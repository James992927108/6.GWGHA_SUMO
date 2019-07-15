import os
from os import listdir
from os.path import join
import shutil
import re

version_list = ["0.0","0.25","0.5","0.75","1"]
need_add_version_algo_list = ["gwgha", "gwogoaha"]

change_dict = {
    "0.0":"0",
    "0.25":"025",
    "0.5":"05",
    "0.75":"075",
    "1":"1",
    "gwo_mgoaha":"gwgha"
}
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

def get_version(text,version_list):
    version = 0
    for v in version_list:
        if v in text:
            version = v
            break
    return version

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def get_new_filename(filename ,version):
    temp = filename.split("_",1)[0]
    new_filename = ""
    for algo in need_add_version_algo_list:
        if temp == algo:
            new_filename = temp + "_" + change_dict[version]
            new_filename = new_filename + "_" + filename.split("_",1)[1]
            break
        else:
            new_filename = filename
    return new_filename

if __name__ == "__main__":
    path = os.getcwd()
    txt_path_list = get_all_txt_path(path)
    for txt_path in txt_path_list:
        print "----------"
        print txt_path
        version = get_version(txt_path,version_list)

        new_txt_path =  replace_all(txt_path,change_dict)
        new_folder_path = new_txt_path.rsplit("/",1)[0]
        new_txt_name = get_new_filename(new_txt_path.rsplit("/",1)[1],version)
        
        if not os.path.isdir(new_folder_path):
            os.makedirs(new_folder_path)

        new_txt_path = join(new_folder_path,new_txt_name)
        print new_txt_path

        os.rename(txt_path,new_txt_path)

    # this still some problem
    for _ in range(4):
        for f in get_last_level_folder_path(os.getcwd()):
            if "gwo_mgoaha" in f:
                print f
                shutil.rmtree(f, ignore_errors=True)
