# from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import requests

import requests
import pandas as pd 
import os

import re
import google_cache_generator as cg

DATA_COLUMNS =['website','headquarters','SIC Code','NAICS Code','revenue','Number of Employees','LinkedIn url' ] 
FINAL_COLUMNS = DATA_COLUMNS + ['company_name','domain_name','zoom_link']

def appendKeyWise(dict_of_lists, dict):
    for key in dict:
        if key in dict_of_lists:
            dict_of_lists[key].append(dict[key])
        else:
            print("WARNING: key not in dict_of_lists, but found in dict")

def initialiseDictFromColumns(dicti, columns, default_val = None):
    for key in columns:
        dicti[key] = default_val

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

    res = {
        'website': website,
        'headquarters':hq,
        'SIC Code':sic,
        'NAICS Code':naics,
        'revenue':revenue,
        'Number of Employees':no_of_employees,
        'LinkedIn url' : linkedIn
    }

    # return [website,hq,sic,naics,revenue,no_of_employees,linkedIn] 
    return res

def scrape_data(link_files_path, save_progress_every=20, start=0, end=-1):
    save_stamp = save_progress_every//2
    if not os.path.exists("final_results/"):
        os.mkdir("final_results/")
    search_results = pd.read_excel(link_files_path)
    num_search_results = len(search_results)

    start = start%num_search_results
    end = end%num_search_results
    # search_results = pd.read_excel("serp_dump.xlsx")
    # final_data = {
    #     'company_name':[],
    #     'domain_name':[],
    #     'website':[],
    #     'zoom_link':[],
    #     'headquarters':[],
    #     'SIC Code':[],
    #     'NAICS Code':[],
    #     'revenue':[],
    #     'Number of Employees':[],
    #     'LinkedIn url' :[]
    # }
    final_data = dict()
    final_data = initialiseDictFromColumns(final_data, FINAL_COLUMNS, default_val=[])


    # for i in search_results.index:
    for i in range(start, end + 1):
        google_top_res_url = search_results['url1'][i]
        # print(google_top_res_url)
        if google_top_res_url!= "(null)":
            try:
                # google_cache_url = cg.generateCacheUrl(google_top_res_url)
                data = urlScrape(cg.generateCacheUrl(google_top_res_url))
            except:
                print(google_top_res_url) 
                google_top_res_url = "!site-not-indexed"
                # data = ["!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed"]
                data = initialiseDictFromColumns(data, DATA_COLUMNS, "!site-not-indexed")

        else:
            # data = ["(null)","(null)","(null)","(null)","(null)""(null)","(null)","(null)"]
            data = initialiseDictFromColumns(data, DATA_COLUMNS, "(null)")

        final_data["company_name"].append(search_results["company_name"][i])
        final_data['domain_name'].append(search_results['domain_name'][i])
        final_data['zoom_link'].append(google_top_res_url)
        # for key in data:
        #     final_data[key].append(data[key])
        appendKeyWise(final_data, data)

# progress saver
        # if i%save_progress_every == 0:
        #     pd.DataFrame(final_data).to_excel(f"save_ScrapeProgress_{i}.xlsx")
        # if os.path.isfile(f"save_ScrapeProgress_{i-save_progress_every}.xlsx"):
        #     os.remove(f"save_ScrapeProgress_{i-save_progress_every}.xlsx")
        if i%save_progress_every == save_stamp:
            pd.DataFrame(final_data).to_excel(f"final_results/scrape_{max(start+1,i-save_progress_every+1)}-{i+1}")
            initialiseDictFromColumns(final_data, FINAL_COLUMNS, default_val=[])

    # pd.DataFrame(final_data).to_excel(f"final_results.xlsx") 
    if len(final_data['company_name']) > 0:
        pd.DataFrame(final_data).to_excel(f"final_results/scrape_{((end-save_stamp)//save_progress_every)*save_progress_every + save_stamp + 1}-{end+1}")

# scrape_data('dump.xlsx')