from logging import exception
from operator import imod
from bs4 import BeautifulSoup
import requests
import urllib

from tor_proxy import NotIndexedError, Retriever

import requests
import pandas as pd 
import os

import re
import google_cache_generator as cg

class BlockedIpException(Exception):
    pass

DATA_COLUMNS =['company_name_zoominfo','website','headquarters','SIC Code','NAICS Code','revenue','Number of Employees','LinkedIn url' ] 
FINAL_COLUMNS = DATA_COLUMNS + ['domain_name','zoom_link']
# WAIT_GET = 3 
USE_PROXY = True 
proxy = Retriever()

def appendKeyWise(dict_of_lists, dict):
    for key in dict:
        if key in dict_of_lists:
            dict_of_lists[key].append(dict[key])
        else:
            print("WARNING: key not in dict_of_lists, but found in dict")

def initialiseDictFromColumns(dicti, columns, default_val = []):
    for key in columns:
        dicti[key] = default_val

# NAME_DOMAIN_COL = 'domain_name'
# NAME_COMPANY_COL = 

CSS_SELECTORS = {
    'company_name_zoominfo' : 'h1.company-name',
    'number_of_employees': "p.company-header-subtitle",
    'hq': "app-icon-text.first div.icon-text-container div span.icon-text-content",
    'linkedin' : 'a#social-media-icon',
    'revenue': "app-icon-text.vertical-gap:-soup-contains('Reven')",
    'sic' : "div.codes-content-wrapper:-soup-contains('SI')",
    'naics' : "div.codes-content-wrapper:-soup-contains('NA')",
    'website' : "a.content",
}
# X_PATH = {
    # 'hq':"//p[@class='icon-label'][contains(text(),'Headquarters')]/parent::div/following-sibling::div//span"
# }

def urlScrape(url):
    try:
        page = proxy.get(url) 
        page_content = page.content
    except urllib.error.HTTPError as e:
        print(e)
        raise BlockedIpException()
    except NotIndexedError as e:
        raise NotIndexedError
    except Exception as e:
        print(type(e))
        print("error in " + url)

    soup = BeautifulSoup(page_content,'html.parser')


    try:
        company_name = soup.select_one(CSS_SELECTORS['company_name_zoominfo']).text
    except:
        company_name = '!not-found'

    try:
        # no_of_employees_raw = [a.text for a in soup.select(CSS_SELECTORS["number_of_employees"])][0]
        no_of_employees_raw = soup.select_one(CSS_SELECTORS['number_of_employees']).text
        no_of_employees =  re.findall("[0-9,<]+ Employees",no_of_employees_raw)[0].replace(' Employees','')
    except:
        no_of_employees = "!not-found"
    
    try:
        # hq = [a.text for a in soup.select(CSS_SELECTORS["hq"])][0].replace('Headquarters:','').strip()
        hq = soup.select_one(CSS_SELECTORS['hq']).text.replace('Headquarters','').strip()
    except:
        hq = "!not-found"

    try:
        # sic = [a.text for a in soup.select(CSS_SELECTORS['sic'])][0]
        sic = soup.select_one(CSS_SELECTORS['sic']).text
        sic = sic.replace("SIC Code ","").strip()    
    except:
        sic = "!not-found"

    try:
        # naics =[a.text for a in  soup.select(CSS_SELECTORS['naics'])][0]
        naics = soup.select_one(CSS_SELECTORS['naics']).text
        naics = naics.replace("NAICS Code ","").strip()
    except:
        naics = "!not-found"

    try:
        # revenue = [a.text for a in soup.select(CSS_SELECTORS['revenue'])][0]
        revenue = soup.select_one(CSS_SELECTORS['revenue']).text
        revenue = revenue.replace("Revenue","").strip()
    except:
        revenue = "!not-found"
    try:
        # website = [a.text for a in soup.select(CSS_SELECTORS['website'])][0]
        website = soup.select_one(CSS_SELECTORS['website']).text
    except:
        website = "!not-found"
    
    try:
        # linkedIn = [a['href'] for a in soup.select("div.vertical-icons div div a")][0] 
        linkedIn = "!not-found"
        linkedIncards = soup.select(CSS_SELECTORS["linkedin"])
        for card in linkedIncards:
            # print(card['href'])
            if 'linkedin' in card['href']:
                linkedIn = card['href']
                break
            else:
                linkedIn = '!not-found'
    except:
        print(e)
        linkedIn = "!not-found"

    res = {
        'company_name_zoominfo' : company_name,
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
    if not os.path.exists("scraped_data/"):
        os.mkdir("scraped_data/")
    search_results = pd.read_excel(link_files_path)
    num_search_results = len(search_results)

    start = start%num_search_results
    end = end%num_search_results
    # search_results = pd.read_excel("serp_dump.xlsx")
    final_data = {
        'company_name' : [],
        'company_name_zoominfo':[],
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
    # final_data = dict()
    # final_data = initialiseDictFromColumns(final_data, FINAL_COLUMNS, default_val= [])


    # for i in search_results.index:
    for i in range(start, end):
        data=dict()
        google_top_res_url = search_results['url1'][i]
        # print(google_top_res_url)
        if google_top_res_url!= "NotAvailable":
            try:
                # google_cache_url = cg.generateCacheUrl(google_top_res_url)
                data = urlScrape(cg.generateCacheUrl(google_top_res_url))
                # data = google_top_res_url
                # data = urlScrape(google_top_res_url)
            except BlockedIpException:
                # sys.exit("blocked")
                pd.DataFrame(final_data).to_excel(f"final_results/final_scrape_{start}_{i-1}.xlsx")
                pd.DataFrame(final_data).to_excel(f"scraped_data/final_scrape_{start}_{i-1}.xlsx")

                print("blocked")
                #TODO: Add code to save whatever was scraped
                return
            except NotIndexedError:
                print(exception)
                print(google_top_res_url) 
                google_top_res_url = "!site-not-indexed"
                # data = ["!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed"]
                initialiseDictFromColumns(data, DATA_COLUMNS, "!site-not-indexed")
            except Exception as e:
                print(e)
                print(google_top_res_url) 
                # google_top_res_url = "!site-not-indexed"
                # data = ["!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed","!site-not-indexed"]
                initialiseDictFromColumns(data, DATA_COLUMNS, "!unknown-error")
            # data = urlScrape(cg.generateCacheUrl(google_top_res_url))

        else:
            # data = ["(null)","(null)","(null)","(null)","(null)""(null)","(null)","(null)"]
            initialiseDictFromColumns(data, DATA_COLUMNS, "NotAvailable")
        # print(search_results["company_name"][i])
        # print(search_results["domain_name"][i])
        # print(type(final_data))

        final_data["company_name"].append(search_results['company_name'][i])
        final_data['domain_name'].append(search_results['domain_name'][i])
        final_data['zoom_link'].append(google_top_res_url)
        print(data)
        # for key in data:
        #     final_data[key].append(data[key])
        appendKeyWise(final_data, data)

# progress saver
        # if i%save_progress_every == 0:
        #     pd.DataFrame(final_data).to_excel(f"save_ScrapeProgress_{i}.xlsx")
        # if os.path.isfile(f"save_ScrapeProgress_{i-save_progress_every}.xlsx"):
        #     os.remove(f"save_ScrapeProgress_{i-save_progress_every}.xlsx")
        if i%save_progress_every == save_stamp:
            pd.DataFrame(final_data).to_excel(f"final_results/scrape_{max(start+1,i-save_progress_every+1)}-{i+1}.xlsx")
            # initialiseDictFromColumns(final_data, FINAL_COLUMNS, default_val=[])

    # pd.DataFrame(final_data).to_excel(f"final_results.xlsx") 
    if len(final_data['company_name']) > 0:
        pd.DataFrame(final_data).to_excel(f"final_results/scrape_{((end-save_stamp)//save_progress_every)*save_progress_every + save_stamp + 1}-{end+1}.xlsx")
    pd.DataFrame(final_data).to_excel(f"final_results/final_scrape_{start}_{end}.xlsx")
    pd.DataFrame(final_data).to_excel(f"scraped_data/final_scrape_{start}_{end}.xlsx")

# scrape_data('dump.xlsx')