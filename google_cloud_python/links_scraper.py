from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Create a new instance of the Firefox driver
XPATH = {
    # "expand_regions" : "//div[@class='gmat-headline-6'][contains(text(),'Regions')]",
    # "asia-pacific" : "//label[@class='mdc-label'][contains(text(),'Asia Pacific')]"
    "load_more" : "//span[contains(text(),'Load')]"
}
CSS_SELECTOR = {
    "links" : "div.partner-card-container>app-partner-card>a",
}

data = {
    "links" : []
}
# options = webdriver.FirefoxOptions()
# options.add_argument('-remote-debugging-port=9222')
# options.add_argument('-start-debugger-server')
# driver = webdriver.Remote(
#     command_executor='http://localhost:9222',
#     options=options)
driver = webdriver.Firefox()

# get the href from the links and put in data
def get_links():
    links = driver.find_elements(By.CSS_SELECTOR, CSS_SELECTOR["links"])
    for link in links:
        data["links"].append(link.get_attribute("href"))
    pd.DataFrame(data).to_excel("links.xlsx", index=False) 

def click_load_more():
    # wait for load more button to appear
    load_more = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, XPATH["load_more"])))
    # click load more button
    load_more.click()

driver.get("https://cloud.google.com/find-a-partner/?regions=APAC_REGION")

num_of_load_more = 5567/12
for i in range(5):
    click_load_more()

get_links()

