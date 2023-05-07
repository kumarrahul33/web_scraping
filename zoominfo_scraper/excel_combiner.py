import glob
import pandas as pd

# specifying the path to csv files

def combineExcelInDirectory(dir_name):
    file_list = glob.glob(dir_name + "/*.xlsx")
    pd.concat([pd.read_excel(file) for file in file_list]).to_excel(dir_name+".xlsx", index=False)
