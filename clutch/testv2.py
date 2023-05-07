from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from pprint import pprint
import numpy as np
import openpyxl
import sys
import random
import selenium.common.exceptions as ec
import os

def get_headers_url(driver,dict):
    urls=[]
    try:
        main = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list_wrap"))
        )

        headers=main.find_elements(By.CLASS_NAME,"provider")
        for header in headers:
            head=header.find_element(By.CSS_SELECTOR,"div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(2) > a:nth-child(1)")
            urls.append(head.get_attribute("href"))
            dict['location'].append(header.find_element(By.CLASS_NAME,"locality").text)
        
        

        
    finally:
        return urls

def get_linkdin(driver,dict):
    try:
        main=driver.find_element(By.CLASS_NAME,"linkedin")
        dict['Linkedin'].append(main.get_attribute("href"))
    except:
        dict['Linkedin'].append("Not found")


def get_location(driver):
    heads=[]
    
    main=driver.find_element((By.CLASS_NAME, "directory-list"))
    
    headers=main.find_elements(By.CLASS_NAME,"provider")
    for header in headers:
            head=header.find_element(By.CSS_SELECTOR,"div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > span:nth-child(2)")
            heads.append(head.text)
    return heads

def get_overview_section(driver,dict):
    lis=['Min. project size',
            'Avg. hourly rate',
            'Employees',
            'Founded',
            'HQ']
    try:
        
        main=driver.find_element(By.ID, "summary_section")
        
        dict['HQ'].append(main.find_element(By.CSS_SELECTOR,".location-name").text)
        rows=main.find_elements(By.CLASS_NAME,"list-item")
        for row in rows[0:4]:
            dict[row.get_attribute("data-content")[3:-4]].append(row.text)
    
    except ec.NoSuchElementException:
        for item in lis:

            dict[lis].append("")
        
def get_name(driver,dict):
    
    main=driver.find_element(By.CSS_SELECTOR, ".header-company--title > a:nth-child(1)")
    
    dict['company name'].append(main.text) 
    dict['company domain'].append(main.get_attribute('href'))
    
def get_key_clients(driver,dict):
    try:
        
        main=driver.find_element(By.CSS_SELECTOR, ".field-name-clients > div:nth-child(2) > p:nth-child(1)")
        
        dict['Key Clients'].append(main.text)
    except ec.NoSuchElementException:
        dict['Key Clients'].append("")

def get_bussness_entity(driver,dict):
    list=['BUSINESS ENTITY NAME','STATUS','JURISDICTION OF FORMATION',]
    try:
        
        main=driver.find_element(By.CSS_SELECTOR, ".col-lg-6 > div:nth-child(3) > div:nth-child(1) > div:nth-child(1)")
        
        rows=main.find_elements(By.CLASS_NAME,"field")
        for row in rows[0:3]:
            if row.find_element(By.CLASS_NAME,"field-label").text in list:
                dict[row.find_element(By.CLASS_NAME,"field-label").text].append(row.find_element(By.CLASS_NAME,"field-item").text)
                list.remove(row.find_element(By.CLASS_NAME,"field-label").text)
        for item in list:
            dict[item].append("")
    except ec.NoSuchElementException:
        for item in list:
            dict[item].append("")    

def get_client_review(driver,dict):
    lis=['VERIFIED CLIENT REVIEWS','OVERALL REVIEW RATING',
            'SOURCE',
            'LAST UPDATED']
    try:
        main=driver.find_element(By.CSS_SELECTOR, "div.row:nth-child(7)")
        
        rows=main.find_elements(By.CLASS_NAME,"field")
        for row in rows:
            dict[row.find_element(By.CLASS_NAME,"field-label").text].append(row.find_element(By.CLASS_NAME,"field-item").text)
    except ec.NoSuchElementException:
        try:
            main =driver.find_element(By.CSS_SELECTOR, "div.row:nth-child(5)")
            rows=main.find_elements(By.CLASS_NAME,"field")
            for row in rows:
                dict[row.find_element(By.CLASS_NAME,"field-label").text].append(row.find_element(By.CLASS_NAME,"field-item").text)
        except ec.NoSuchElementException:
            for item in lis:
                dict[item].append("")

def get_focus(driver,dict):
    
    
    main=driver.find_element(By.CLASS_NAME, "section-accordion")

    
    service_lines=main.find_element(By.CSS_SELECTOR,"div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
    graphs=main.find_elements(By.CLASS_NAME,"col-md-6")

    # .focus-charts-wrapper > div:nth-child(1) > div:nth-child(2)

    
    
    dict["Service lines"].append(get_lines(service_lines))
    get_graphs(graphs,dict)    
    
def get_graphs(graphs,dict):
    dict_list={}
    for graph in graphs:#/html/body/main/section[3]/div/div/div[2]/div[3]/div[1]/div[1]
        
        try:
            dict_list[graph.find_element(By.CLASS_NAME,"graph-title").text]=(get_lines(graph.find_element(By.XPATH,"div/div[2]/div")))
        except ec.NoSuchElementException:
            continue
    dict["Focus"].append(dict_list)

def get_lines(x_lines):
    lines=x_lines.find_elements(By.TAG_NAME,"div")
    li=""
    for line in lines:
        try:
            li=li+"("+line.get_attribute("data-content")[3:-4]+":"+line.text+");"
        except TypeError:
            continue
    return li
                   
def get_page(driver):
    main = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "profile-container"))
        )
    return main

url_dict={
    1:"https://clutch.co/agencies/digital-marketing",
    2:"https://clutch.co/seo-firms",
    3:"https://clutch.co/agencies/social-media-marketing",
    4:"https://clutch.co/agencies/content-marketing",
    5:"https://clutch.co/agencies/sem",
    6:"https://clutch.co/agencies",
    7:"https://clutch.co/agencies/branding",
    8:"https://clutch.co/agencies/creative",
    9:"https://clutch.co/agencies/video-production",
    10:"https://clutch.co/pr-firms",
    11:"https://clutch.co/agencies/media-buying"
}

url_name={
    1:"digital-marketing",
    2:"seo-firms",
    3:"social-media-marketing",
    4:"content-marketing",
    5:"search-marketing",
    6:"advertising",
    7:"branding",
    8:"creative",
    9:"video-production",
    10:"pr-firms",
    11:"media-buying"
}

industry_dict={
    1:"&industries=field_pp_if_bizservices",
    2:"&industries=field_pp_if_it"
}

name_dict={
    1:"Business-Services",
    2:"Information-Technology"
}

if __name__ == '__main__':
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    url_head=url_dict[int(sys.argv[1])]+"?agency_size=10+-+49&agency_size=1%2C000+-+9%2C999&agency_size=10%2C000%2B&agency_size=250+-+999&agency_size=50+-+249&agency_size=2+-+9"+industry_dict[int(sys.argv[2])]   
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    for pg_num in range(start, end+1):
        driver = webdriver.Firefox(options=options)
        url=url_head+f"&page={pg_num}"
        dict={'company name':[],
            'company domain':[],
            'Min. project size':[],
            'Avg. hourly rate':[],
            'Employees':[],
            'Founded':[],
            'location':[],
            'HQ':[],
            'Key Clients':[],
            'BUSINESS ENTITY NAME':[],
            'STATUS':[],
            'JURISDICTION OF FORMATION':[],
            'VERIFIED CLIENT REVIEWS':[],
            'OVERALL REVIEW RATING':[],
            'SOURCE':[],
            'LAST UPDATED':[],
            'Service lines':[],
            'Focus':[],
            'Linkedin':[],
            }
        driver.get(url)
        a=get_headers_url(driver,dict)
        driver.quit()
        for i in range(len(a)):
            driver= webdriver.Firefox(options=options)
            driver.get(a[i])
            try:
                page=get_page(driver)
            except ec.TimeoutException:
                for keys in dict:
                    if keys != 'location':
                        dict[keys].append("unhadled-profile-page")
                continue
            get_overview_section(page,dict)
            get_bussness_entity(page,dict)
            get_client_review(page,dict)
            get_key_clients(page,dict)
            get_name(page,dict)
            get_focus(page,dict)
            get_linkdin(page,dict)
            driver.quit()
            print(f"entry {i} of page {pg_num} done in {url_name[int(sys.argv[1])]} in {name_dict[int(sys.argv[2])]} name: {dict['company name'][-1]}")
            # pprint(dict)
        
        df=pd.DataFrame(dict)
        df.index = np.arange(1, len(df) + 1)
        path = url_name[int(sys.argv[1])]+"_"+name_dict[int(sys.argv[2])]
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        df.to_excel(f"{url_name[int(sys.argv[1])]}_{name_dict[int(sys.argv[2])]}/data_{pg_num}.xlsx")
        driver.quit()
