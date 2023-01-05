from functools import cache
from operator import index
import string
import pandas as pd
import numpy as np
from difflib import get_close_matches
from tqdm import tqdm
# from googlesearch import search
from bs4 import BeautifulSoup
import requests
# import lxml
import json

import requests
import urllib
import pandas as pd
# from requests_html import HTML
# from requests_html import HTMLSession

import http.client
import json
from serpapi import GoogleSearch
import re


def urlScrape(url):
    try:
        page = requests.get(url)
    except:
        print("error in" + url)
        return ["","","","","",""]
    soup = BeautifulSoup(page.content,'html.parser')

    try:
        no_of_employees_raw = [a.text for a in soup.select("p.company-header-subtitle")][0]
        no_of_employees =  re.findall("[0-9,<]+ Employees",no_of_employees_raw)[0].replace(' Employees','')
        # print(no_of_employees)
    except:
        no_of_employees = "NAN"
    
    try:
        hq = [a.text for a in soup.select("app-icon-text.first div.icon-text-wrapper")][0].replace('Headquarters:','').strip()
    # print(hq)
    except:
        hq = "NAN"

    try:
        sic = [a.text for a in soup.select("div.codes-content-wrapper:-soup-contains('SI')")][0]
        sic = sic.replace("SIC Code ","").strip()    
    except:
        sic = "NAN"
    # print(sic)

    try:
        naics =[a.text for a in  soup.select("div.codes-content-wrapper:-soup-contains('NA')")][0]
        naics = naics.replace("NAICS Code ","").strip()
    except:
        naics = "NAN"
    # print(naics)

    try:
        revenue = [a.text for a in soup.select("app-icon-text.vertical-gap:-soup-contains('Reven')")][0]
        revenue = revenue.replace("Revenue:","").strip()
    except:
        revenue = "NAN"
    # print(revenue)
    try:
        website = [a.text for a in soup.select("a.content")][0]
    except:
        website = "NAN"

    return [website,hq,sic,naics,revenue,no_of_employees] 

companies = pd.read_excel("websites.xlsx")
companies_cache = pd.DataFrame(columns=['domain','cached'])
final_data = pd.DataFrame(columns=['domain','headquaters','SIC Code','NAICS Code','revenue','number of employees'])
for i in companies.index:
    c_name = companies["domain"][i] 
    params = {
        #   "api_key": "b8000c3fa301ad68ea2ebdf7caa7f1532c89cc4b23e18296bc2e7ea7d4fd6023",
          "api_key":"a03af2b4c85efaa0a4c82a9648d4d199d31d4bc434cbb9a42e97d7d9be93bc7d",
          "engine": "google",
          "q": c_name + " revenue \"zoominfo\"",
          "google_domain": "google.com",
          "gl": "us",
          "hl": "en"
        }
    try:
        search = GoogleSearch(params)
        response = search.get_dict()
    except:
        print("Error occured in serp for" , c_name)
        continue

    if 'organic_results' in response:        
        # Organic Reponse    
        organic_response = pd.DataFrame(response['organic_results']).query("position<=3")
        # print(organic_response.to_dict())
        if organic_response.empty == False:
            for og_resp in organic_response.iterrows():
                try:
                    cached_url = og_resp[1]['cached_page_link']
                    data_point = urlScrape(cached_url)

                    data2 = {'domain':c_name, 'cached':cached_url}
                    companies_cache = companies_cache.append(data2,ignore_index=True)

                    data = {'domain':data_point[0],'headquaters':data_point[1],'SIC Code':data_point[2],'NAICS Code':data_point[3],
                    'revenue':data_point[4],'number of employees':data_point[5]} 
                    final_data = final_data.append(data,ignore_index=True)

                    break
                except:
                    print("using non top res for :"+ c_name)
                    continue
# urlScrape("https://webcache.googleusercontent.com/search?q=cache:dB9UWN-O18QJ:https://www.zoominfo.com/c/broad-horizon/357240237&cd=1&hl=en&ct=clnk&gl=us")
final_data.to_excel("result.xlsx")
companies_cache.to_excel("cached_urls.xlsx")
print(urlScrape("https://webcache.googleusercontent.com/search?q=cache:KlY6gwNSxgUJ:https://www.zoominfo.com/c/smile-co/348668444&cd=1&hl=en&ct=clnk&gl=us"))
