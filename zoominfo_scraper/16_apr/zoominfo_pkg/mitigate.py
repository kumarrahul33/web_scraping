import os
import subprocess
# read file names in a directory
def read_file_names(path):
    file_names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_names.append(file)
    return file_names

# format of the file name is serp_dump_start_end.xlsx
def get_start_end(file_name):
    file_name = file_name.split('.')[0]
    file_name = file_name.split('_')
    start = int(file_name[2])
    end = int(file_name[3])
    return start, end

def get_start_end_list(file_names):
    start_end_list = []
    for file_name in file_names:
        start, end = get_start_end(file_name)
        start_end_list.append((start, end))
    return start_end_list


def possible_files():
    possible_files = []
    delta = 1158//100
    # for i in range(1158):
    i = 0 
    while i < 1158:
        possible_files.append((i, min(i+delta, 1158)))
        i = i + delta
    return possible_files

def get_missing_start_end(start_end_list):
    miss = []
    for elem in possible_files():
        if elem not in start_end_list:
            miss.append(elem)
    return miss

files = read_file_names("serp_dump_files") 
start_end_list = get_start_end_list(files)
missing_start_end = get_missing_start_end(start_end_list)

# print(missing_start_end)


for elem in missing_start_end:
    start = str(elem[0])
    end = str(elem[1])

    subprocess.call(f"python serp_scraper.py url.xlsx {start} {end}", shell=True)
    # print("python serp_scraper.py {} {} url.xlsx".format(start, end))