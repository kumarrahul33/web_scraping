import os
import sys
import excel_combiner
import subprocess

# take command line input from the user 
file_name = sys.argv[1]
final_index = sys.argv[2]
no_of_terminals_serp = sys.argv[3]
no_of_terminals_tor = sys.argv[4]
# print(len(sys.argv))
# if not given 4 inputs, then exit and print usage
if(len(sys.argv) != 5):
    print("Usage: python3 setup.py <file_name> <final_index> <no_of_terminals_serp> <no_of_terminals_tor>")
    exit(1)

# subprocess.run(['bash', 'url_scraper.sh', '0', final_index, no_of_terminals_serp, file_name])
# excel_combiner.combineExcelInDirectory("serp_dump_files")
# subprocess.run(["bash", "websites_scraper.sh", "0", final_index, no_of_terminals_tor, "serp_dump_files.xlsx"])
excel_combiner.combineExcelInDirectory("scraped_data")



 