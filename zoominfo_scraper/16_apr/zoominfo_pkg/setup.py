import os
import time
import sys
import excel_combiner
import subprocess
import pandas as pd

# take command line input from the user 
file_name = sys.argv[1]
# final_index = sys.argv[2]
no_of_terminals_serp = sys.argv[2]
no_of_terminals_tor = sys.argv[3]
# print(len(sys.argv))
# if not given 4 inputs, then exit and print usage

if(len(sys.argv) != 4):
    print("Usage: python3 setup.py <file_name> <no_of_terminals_serp> <no_of_terminals_tor>")
    exit(1)

# find the last index of the file below
df = pd.read_excel(file_name)
last_index = len(df.index)
final_index = str(int(last_index) + 3)



subprocess.run(['bash', 'url_scraper.sh', '0', final_index, no_of_terminals_serp, file_name])
time.sleep(3)
excel_combiner.combineExcelInDirectory("serp_dump_files")
time.sleep(3)
subprocess.run(["bash", "websites_scraper.sh", "0", final_index, no_of_terminals_tor, "serp_dump_files.xlsx"])
# wait for 3 sec
time.sleep(3)
excel_combiner.combineExcelInDirectory("scraped_data")



 