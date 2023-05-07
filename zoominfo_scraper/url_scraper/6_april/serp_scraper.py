import os
import serp_bd
import sys

# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
serp_bd.dump_links(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
# serp_bd.dump_links("Zoominfo_Search.xlsx",0,4)
# os.makedirs("a/b")

