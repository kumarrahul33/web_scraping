import scrapper_bd
import serp_bd
import sys
serp_bd.dump_links(sys.argv[1])
# scrapper_bd.scrape_data('serp_dump.xlsx')

#usage : main_scrapper.py file_path_containing_websites 
# column name should be "Company Name" and "Domain"
