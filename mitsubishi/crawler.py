# open a firefox instance with selenium
# and navigate to a website

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import By
from selenium.webdriver.common.by import By
# import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
# import expected_conditions
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://les.mitsubishielectric.co.uk/find-an-installer"
BUTTONS = {
    'filter' : 'input.selector[value="2"]',
    'next' : 'a.pager-btn.pager-next',
}

CSS_SELECTOR = {
    'installer' : 'div.installer-result',
}

def scrape_data(driver):
    # get the installer html
    # select the h4 tag in it
    # get the text

    installer = driver.find_elements(By.CSS_SELECTOR,CSS_SELECTOR['installer'])
    for installer in installer:
        installer_name = installer.find_element(By.CSS_SELECTOR,'h4').text
        print(installer_name)

driver = webdriver.Firefox()
driver.get(BASE_URL)
# wait for filter button to be clickable
driver.implicitly_wait(3)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,BUTTONS['filter']))) 


# click on the filter button
driver.find_element(By.CSS_SELECTOR,BUTTONS['filter']).click()

scrape_data(driver)

#wait for few seconds

driver.close()