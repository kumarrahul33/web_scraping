# import time
import pandas as pd
# from selenium import webdriver
# # import By.cssSelector
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

# Start a WebDriver server on the default port

BASE_URL = "https://appexchange.salesforce.com/consulting/top"


CSS_SELECTORS = {
    "company_card" : "li>a.appx-tile-consultant",
    "country_dropdown" : "select[id='select_country']",
    # "country_dropdown" : "div#country-select",
    "france" : "select[id='select_country']>option[value='co=co-FR']",
    "apply_filter" : "span.appx-button-filter-apply-long",
    "load_more" : "div.appx-load-more-button-container>button",
}

data = {
    "company_links" : [] 
}
# driver = webdriver.Firefox()
# driver.get(BASE_URL)


# def select_country(country):
#     # wait for the button country_dropdown to appear
#     # driver.implicitly_wait(10)
#     # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS["country_dropdown"]))) 
#     # # click the dropdown
#     # # driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS["country_dropdown"]).click()
#     # # click the country
#     # driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS[country]).click()
#     # # implicit wait of 2 seconds
#     # driver.implicitly_wait(2)
#     # # click on apply filter
#     # driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS["apply_filter"]).click()

#     time.sleep(10)
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS["country_dropdown"]))) 
#     dropdown = Select(driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS["country_dropdown"]))
#     dropdown.select_by_value("co=co-FR")
    
with open("spain.html") as fp:
    soup = BeautifulSoup(fp,"html.parser")
def get_company_links():
    # company_links = []
    for company in soup.select(CSS_SELECTORS["company_card"]):
        data["company_links"].append(company["href"])
        # print(company["href"])
    # return company_links
get_company_links()
pd.DataFrame(data).to_csv("spain.csv", index=False)





