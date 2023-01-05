import glob
import pandas as pd

# specifying the path to csv files
path = "serp_dump_files"

# csv files in the path
file_list = glob.glob(path + "/*.xlsx")

# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
# excl_list = []

# for file in file_list:
	# excl_list.append(pd.read_excel(file))
# create a new dataframe to store the
# merged excel file.
# excl_merged = pd.DataFrame()
excl_merged = pd.concat([pd.read_excel(file) for file in file_list])
# exports the dataframe into excel file with
# specified name.
# excl_merged.to_excel('}.xlsx', index=False)
