import requests
from bs4 import BeautifulSoup
import pandas as pd

# BASE_URL = "https://les.mitsubishielectric.co.uk/find-an-installer/JsonInstallersList"
BASE_URL = "https://les.mitsubishielectric.co.uk/find-an-installer/AjaxInstallersList"

CSS_SELECTOR = {
    'installer' : 'div.installer-result',
    # 'installer_result_title' : 'h4.installer-result__title',
    'installer_name' : 'h4.installer-result__title',
    'installer-details' : 'div.installer-result__detail',
    'installer-type' : 'div.installer-result__types span',
    'installer-capabilites' : 'div.installer-result__capabilities',
    # 'installer_name' : 'h4',
    # 'installer_address' : 'p',
}

final_data= {
    'installer_name' : [],
    'installer_address' : [], 
    'installer_type' : [],
    'installer_contact' : [],
    'installer_services' : [],
    'installer_products' : [],
}
final_data_all = {
    'installer_name' : [],
    'installer_address' : [], 
    'installer_type' : [],
    'installer_contact' : [],
    'installer_services' : [],
    'installer_products' : [],
}
# def get_data():
#     pass

def scrape_data():
    for i in range(0,205):
        url = BASE_URL + "?start=" + str(i*7)
        data = requests.get(url)
        # parse data as json
        data = BeautifulSoup(data.text,'html.parser') 
        # select all installer
        installer = data.select(CSS_SELECTOR['installer'])
        # select the installer name in the installer
        for installer in installer:
            try:
                installer_name = installer.select(CSS_SELECTOR['installer_name'])[0].text
            except:
                continue

            try:
                installer_address = installer.select(CSS_SELECTOR['installer-details'])[0].text.strip()
            except:
                installer_address = "No Address Found"

            try:
                installer_type = installer.select_one(CSS_SELECTOR['installer-type']).text.strip()
            except:
                installer_type = "No Type Found"
            try: 
                installer_contact = installer.select(CSS_SELECTOR['installer-details'])[1].find('a').get('href')
            except:
                installer_contact = "No Contact Found"

            try:
                installer_services = installer.select(CSS_SELECTOR['installer-capabilites'])[0].select('li')
                installer_services = list(map(lambda x: x.text.strip(),installer_services))
            except:
                
                installer_services = "No Services Found"
            
            try:
                installer_products = installer.select(CSS_SELECTOR['installer-capabilites'])[1].find_all('li')
                installer_products = list(map(lambda x: x.text.strip(),installer_products))
            except:
                installer_products = "No Products Found"
            
            if("Heating (Commercial)" in installer_products or "Heating (Domestic)" in installer_products):
                final_data['installer_name'].append(installer_name.strip())
                final_data['installer_address'].append(installer_address.strip())
                final_data['installer_type'].append(installer_type)
                final_data['installer_contact'].append(installer_contact)
                final_data['installer_services'].append(installer_services)
                final_data['installer_products'].append(installer_products)

            final_data_all['installer_name'].append(installer_name.strip())
            final_data_all['installer_address'].append(installer_address.strip())
            final_data_all['installer_type'].append(installer_type)
            final_data_all['installer_contact'].append(installer_contact)
            final_data_all['installer_services'].append(",".join(installer_services))
            final_data_all['installer_products'].append(",".join(installer_products))
            
            # print(installer_name.strip())
            # print(installer_address.strip())
            # print(installer_services)
            # print(installer_products)
            # print(len(installer_name))
            # print(installer_services.select('li'))




scrape_data()
pd.DataFrame(final_data).to_excel('data.xlsx',index=False)
pd.DataFrame(final_data_all).to_excel('data_all.xlsx',index=False)

# pd.DataFrame(final_data).to
         
        