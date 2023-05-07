import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
df = pd.read_csv("uk.csv")

# iterate over the dataframe
CSV_SELECTORS = {
    "company_name" : ".appx-page-header-2_title",
    "languages" : "div.appx-extended-detail-subsection>div>span",
    "top_2_countries" : "span.appx-detail-subsection-values-title", # only take the first two
    "country_count" : "span.appx-detail-subsection-values-title:-soup-contains('International') + a",
    "countries" : "span.appx-detail-subsection-values-title:-soup-contains('International')+a",
}

XPATH_SELECTORS = {
    "projects_completed" : "//span[@class='appx-summary-bar_facts-label'][contains(text(),'Projects Completed')]/following-sibling::span",
    "certified_experts" : "//span[@class='appx-summary-bar_facts-label'][contains(text(),'Certified')]/following-sibling::span",
    "founded" : "//span[@class='appx-summary-bar_facts-label'][contains(text(),'Founded')]/following-sibling::span",
    "hq" : "//div[@class='appx-extended-detail-subsection-label'][contains(text(),'Headquarters')]/following-sibling::div", 
    "website" : "//div[@class='appx-extended-detail-subsection-label'][contains(text(),'Website')]/following-sibling::div/a",
    "email" : "//div[@class='appx-extended-detail-subsection-label'][contains(text(),'Email')]/following-sibling::div/a",
    "phone" : "//div[@class='appx-extended-detail-subsection-label'][contains(text(),'Phone')]/following-sibling::div",
    "country_count":"//span[@class='appx-detail-subsection-values-title'][contains(text(),'International')]",
    "countries":"//span[@class='appx-detail-subsection-values-title'][contains(text(),'International')]/following-sibling::span",
}

data = {
    "projects_completed" : [],
    "certified_experts" : [],
    "founded" :[],
    "company_name" : [],
    "hq" : [],
    "website" :[], 
    "email" : [],
    "phone" :[],
    "languages" : [],
    "top_2_countries" : [],
    "country_count":[],
    "sf_link" : [],
    "countries" : [],
}

def scrape_data(website):
    # get the html and parse it using beatuiful soup
    html = requests.get(website).text
    soup = BeautifulSoup(html, "html.parser")
    dom = etree.HTML(str(soup))
    # get the number of projects completed
    data["sf_link"].append(website)
    try:
        projects_completed = dom.xpath(XPATH_SELECTORS["projects_completed"])[0].text
        data["projects_completed"].append(projects_completed)
    # except Exception as e:
    except:
        data["projects_completed"].append("not found")
    
    try:
        # certified_experts = soup.select_one(CSV_SELECTORS["certified_experts"]).text
        certified_experts = dom.xpath( XPATH_SELECTORS["certified_experts"])[0].text
        data["certified_experts"].append(certified_experts)
    except:
        data["certified_experts"].append("not found")
    
    try: 
        # founded = soup.select_one(CSV_SELECTORS["founded"]).text
        founded = dom.xpath( XPATH_SELECTORS["founded"])[0].text
        data["founded"].append(founded)
    except:
        data["founded"].append("not found")
    
    try:
        company_name = soup.select_one(CSV_SELECTORS["company_name"]).text
        data["company_name"].append(company_name)
    except:
        data["company_name"].append("not found")
    
    try:
        # hq = soup.select_one(CSV_SELECTORS["hq"]).text
        hq = dom.xpath( XPATH_SELECTORS["hq"])[0].text
        data["hq"].append(hq)
    except:
        data["hq"].append("not found")
    
    try:
        # website = soup.select_one(CSV_SELECTORS["website"])["href"]
        website = dom.xpath( XPATH_SELECTORS["website"])[0]["href"]
        data["website"].append(website)
    except:
        data["website"].append("not found")
    
    try:
        # email = soup.select_one(CSV_SELECTORS["email"])["href"]
        email = dom.xpath( XPATH_SELECTORS["email"])[0]["href"]
        data["email"].append(email)
    except:
        data["email"].append("not found")
    
    try:
        # phone = soup.select_one(CSV_SELECTORS["phone"]).text
        phone = dom.xpath( XPATH_SELECTORS["phone"])[0].text
        data["phone"].append(phone)
    except:
        data["phone"].append("not found")
    
    try:
        languages = soup.select(CSV_SELECTORS["languages"])
        languages = [language.text for language in languages]
        data["languages"].append(languages)
    except:
        data["languages"].append("not found")
        
    try:
        top_2_countries = soup.select(CSV_SELECTORS["top_2_countries"])
        top_2_countries = [top_2_countries[i].text for i in range(2)]
        data["top_2_countries"].append(top_2_countries)
    except:
        data["top_2_countries"].append("not found") 
    
    try:
        country_count = soup.select_one(CSV_SELECTORS["country_count"]).text
        # country_count = dom.xpath( XPATH_SELECTORS["country_count"])[0].text
        # data["country_count"].append(country_count)
        country_count = country_count.split(',')
        country_count = [country_count[i].strip() for i in range(len(country_count))]
        # countries_count = countries_count[-1].split(" ")
        # countries_count = countries_count[-2]
        country_count = country_count[-1].split(" ")[-2]
        # print(country_count)
        # data["country_count"].append(country_count.join(","))
        data["country_count"].append(country_count)
        # print(country_count)

        # print(country_count)
    # except Exception as e:
    except:
        data["country_count"].append("not found")
    try:
        # countries = dom.xpath(XPATH_SELECTORS["countries"])[0].text
        countries = soup.select_one(CSV_SELECTORS["countries"]).text
        countries = countries.split(',')
        countries = [countries[i].strip() for i in range(len(countries))]
        # countries = countries[-1].split(" ")
        # print(countries)
        countries[-1] = countries[-1].split(" ")[-3]
        countries = ",".join(countries)
        # print(countries) 
        
        
        # co
        # data["countries"].append(countries.join(","))
        data["countries"].append(countries)
    except:
        print("not found")
        data["countries"].append("not found")

for index, row in df.iterrows():
    print(f"Scraping {row['company_links']}")
    scrape_data(row["company_links"])
    if(index >= 0):
        break

pd.DataFrame(data).to_excel("uk_data.xlsx")