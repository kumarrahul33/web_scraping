import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
data = {
    "company_name" : [],
    "google_partner_link" : [],
    "specialzation" : [],
    "description" : [],
    "industry" : [],
    "prod_tech": [],
    "solutions" : [],
    "website" : [],
    "email" : [],
    "location_on_map" :   [], 
    "awards" : [],
    "initiative" : [],
    "partner_type" : [],
    "language" : [],
    "country" : [],
    "hq" : [],
    "tagline" : [],
    "phone" : [],
    "country_card" : [],
}


CSS_SELECTOR = {
    "company_name" : "h1.title",
    "specialzation" : "p.content",
    "description" : "div.partner-detail-description",
    "awards" : "div.contact-detail-text[data-test-id='contact-detail-awards-data']",
    "website" : "a.detail-links[aria-label='Partner website']",
    "tagline" : "p.subtitle.ng-star-inserted",
    "country_card" : "h3.mat-mdc-card-title.gmat-headline-6",
    "email" : "a.detail-links[aria-label='Partner email address']",
    "location_on_map" : "a.detail-links[aria-label='Partner address']",
    "phone" : "a.detail-links[aria-label='Partner phone number']",
}
X_PATH = {
    "industry" : "//h3[contains(text(),'Industry')]/following-sibling::*[1]",
    "prod_tech" : "//h3[contains(text(),'Product')]/following-sibling::*[1]",
    "solutions" : "//h3[contains(text(),'Industry')]/following-sibling::*[1]",
    "partner_type" : "//h2[contains(text(),'Partner type')]/following-sibling::*[1]",
    "language" : "//h2[contains(text(),'Supported Languages')]/following-sibling::*[1]",
    "country" : "//h2[contains(text(),'Countries')]/following-sibling::*[1]",
    "initiative" : "//h2[contains(text(),'Initiatives')]/following-sibling::*[1]",
}

def get_data(link):
    driver.get(link)
    # wait for description to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTOR["description"])))

    data["google_partner_link"].append(link)
    try:
        company_name = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["company_name"]).text
        data["company_name"].append(company_name)
    except:
        data["company_name"].append("not found")

    try:
        specialzation = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["specialzation"]).text
        data["specialzation"].append(specialzation)
    except:
        data["specialzation"].append("not found")
    
    try:
        description = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["description"]).text
        data["description"].append(description)
    except:
        data["description"].append("not found")
    
    try:
        industry = driver.find_element(By.XPATH, X_PATH["industry"]).text
        data["industry"].append(industry)
    except:
        data["industry"].append("not found")
    
    try:
        prod_tech = driver.find_element(By.XPATH, X_PATH["prod_tech"]).text
        data["prod_tech"].append(prod_tech)
    except:
        data["prod_tech"].append("not found")
    
    try:
        solutions = driver.find_element(By.XPATH, X_PATH["solutions"]).text
        data["solutions"].append(solutions)
    except:
        data["solutions"].append("not found")
    
    try:
        website = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["website"]).get_attribute("href")
        data["website"].append(website)
    except:
        data["website"].append("not found")
    
    try:
        email = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["email"]).get_attribute("href")
        data["email"].append(email)
    except:
        data["email"].append("not found")
    
    try:
        awards = driver.find_elements(By.CSS_SELECTOR, CSS_SELECTOR["awards"])
        awards = [award.text for award in awards]
        data["awards"].append(awards)
    except:
        data["awards"].append("not found")
    
    try:
        initiative = driver.find_elements(By.XPATH, X_PATH["initiative"])
        initiative = [initiative.text for initiative in initiative]
        data["initiative"].append(initiative)
    except:
        data["initiative"].append("not found")
    
    try: 
        partner_type = driver.find_element(By.XPATH, X_PATH["partner_type"]).text
        data["partner_type"].append(partner_type)
    except:
        data["partner_type"].append("not found")
    
    try:
        language = driver.find_element(By.XPATH, X_PATH["language"]).text
        data["language"].append(language)
    except:
        data["language"].append("not found")
    
    try: 
        country = driver.find_element(By.XPATH, X_PATH["country"]).text
        data["country"].append(country)
    except:
        data["country"].append("not found")
    
    # try:
    #     hq = driver.find_element(By.XPATH, X_PATH["hq"]).text
    #     data["hq"].append(hq)
    # except:
    #     data["hq"].append("not found")
    
    try:
        tagline = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["tagline"]).text
        data["tagline"].append(tagline)
    except:
        data["tagline"].append("not found")

    # try:
    #     location_on_map = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["location_on_map"]).text
    #     data["location_on_map"].append(location_on_map)
    # except:
    #     data["location_on_map"].append("not found")
    
    try:
        phone = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["phone"]).get_attribute("href")
        data["phone"].append(phone)
    except:
        data["phone"].append("not found")
    
    try: 
        country_card = driver.find_elements(By.CSS_SELECTOR, CSS_SELECTOR["country_card"])
        country_card = [country.text for country in country_card]
        data["country_card"].append(country_card)
    except:
        data["country_card"].append("not found")
    
    try:
        location_on_map = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["location_on_map"]).get_attribute("href")
        data["location_on_map"].append(location_on_map)
    except:
        data["location_on_map"].append("not found")
    
    try:
        hq = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR["country_card"]).text
        data["hq"].append(hq)
    except:
        data["hq"].append("not found")
    


    


# df = pd.read_csv("links.csv")
df = pd.read_excel("links.xlsx")

links = df["links"].tolist()



# iterate over the links
for link in links:
    get_data(link)

# get_data("https://cloud.google.com/find-a-partner/partner/quantiphi-inc")
# # print(data)
# for key in data.keys():
#     if len(data[key]) != 1:
#         # data[keys].append("not found")
#         print(key)
pd.DataFrame(data).to_excel("data.xlsx", index=False)
