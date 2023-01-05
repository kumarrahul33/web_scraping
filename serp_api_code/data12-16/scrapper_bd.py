# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import requests

import requests
import pandas as pd 
import os

import re
import google_cache_generator as cg

save_progress_at = 10 

def urlScrape(url):
    try:
        page = requests.get(url)
    except:
        print("error in" + url)
        return ["!need-proxy","!need-proxy","!need-proxy","!need-proxy","!need-proxy","!need-proxy","!need-proxy","!need-proxy"]
    soup = BeautifulSoup(page.content,'html.parser')

    try:
        no_of_employees_raw = [a.text for a in soup.select("p.company-header-subtitle")][0]
        no_of_employees =  re.findall("[0-9,<]+ Employees",no_of_employees_raw)[0].replace(' Employees','')
    except:
        no_of_employees = "!not-found"
    
    try:
        hq = [a.text for a in soup.select("app-icon-text.first div.icon-text-wrapper")][0].replace('Headquarters:','').strip()
    except:
        hq = "!not-found"

    try:
        sic = [a.text for a in soup.select("div.codes-content-wrapper:-soup-contains('SI')")][0]
        sic = sic.replace("SIC Code ","").strip()    
    except:
        sic = "!not-found"

    try:
        naics =[a.text for a in  soup.select("div.codes-content-wrapper:-soup-contains('NA')")][0]
        naics = naics.replace("NAICS Code ","").strip()
    except:
        naics = "!not-found"

    try:
        revenue = [a.text for a in soup.select("app-icon-text.vertical-gap:-soup-contains('Reven')")][0]
        revenue = revenue.replace("Revenue:","").strip()
    except:
        revenue = "!not-found"
    try:
        website = [a.text for a in soup.select("a.content")][0]
    except:
        website = "!not-found"
    
    try:
        linkedIn = [a['href'] for a in soup.select("div.vertical-icons div div a")][0] 
    except:
        linkedIn = "!not-found"

    return [website,hq,sic,naics,revenue,no_of_employees,linkedIn] 






def scrape_data(link_files_path):
    search_results = pd.read_excel(link_files_path)
    # search_results = pd.read_excel("serp_dump.xlsx")
    final_data = {
        'company_name':[],
        'domain_name':[],
        'website':[],
        'zoom_link':[],
        'headquarters':[],
        'SIC Code':[],
        'NAICS Code':[],
        'revenue':[],
        'Number of Employees':[],
        'LinkedIn url' :[]

    }


    for i in search_results.index:
        google_top_res_url = search_results['url1'][i]
        # print(google_top_res_url)
        if google_top_res_url!= "(null)":
            try:
                google_cache_url = cg.generateCacheUrl(google_top_res_url)
                data = urlScrape(cg.generateCacheUrl(google_top_res_url))
            except:
                print(google_top_res_url) 
                google_top_res_url = "!site-not-indexed"
                data = ["!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed"]

        else:
            data = ["(null)","(null)","(null)","(null)","(null)""(null)","(null)","(null)"]

        final_data["company_name"].append(search_results["company_name"][i])
        final_data['domain_name'].append(search_results['domain_name'][i])
        final_data['website'].append(data[0])
        final_data['zoom_link'].append(google_top_res_url)
        final_data['headquarters'].append(data[1])
        final_data['SIC Code'].append(data[2])
        final_data['NAICS Code'].append(data[3])
        final_data['revenue'].append(data[4])
        final_data['Number of Employees'].append(data[5])
        final_data['LinkedIn url'].append(data[6])

# progress saver
        if i%save_progress_at == 0:
            pd.DataFrame(final_data).to_excel(f"save_ScrapeProgress_{i}.xlsx")
        if os.path.isfile(f"save_ScrapeProgress_{i-save_progress_at}.xlsx"):
            os.remove(f"save_ScrapeProgress_{i-save_progress_at}.xlsx")


    pd.DataFrame(final_data).to_excel("final_results.xlsx") 

# scrape_data('dump.xlsx')
