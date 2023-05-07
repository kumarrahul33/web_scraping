import os
# import scrapper_bd 
import sys
# import scrapper_bd_tor
import zoominfo_scraper

# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
# scrapper_bd.scrape_data(sys.argv[1],5,51,100)
if len(sys.argv) < 4:
    print(f"Usage: python cache_scraper.py <url-file-path> <start-index> <end-index>")
    exit(-1)

start = int(sys.argv[2])
end = int(sys.argv[3])
zoominfo_scraper.scrape_data(sys.argv[1],20,start,end)

# serp_bd.dump_links("Zoominfo_Search.xlsx",0,4)
# os.makedirs("a/b")

