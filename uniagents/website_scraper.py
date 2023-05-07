import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'https://www.uniagents.com/en/consultants-india/index'

XPATH_SELECTOR = {
    'location': '//div[@class="hover-consultants"]/span[@class="con-location"]',
    'name' : '//div[@class="hover-consultants"]/span[@class="con-name"]',
    'profile_link': '//div[@class="hover-consultants"]/a[@class="con-profile"]',
}

CSS_SELECTOR = {
    'location' : 'div.hover-consultants>span.con-location',
    'name' : 'div.hover-consultants>span.con-name',
    'profile_link': 'div.hover-consultants>a.view-con-pro',
    'mission_staement' : 'td.upper1',
    'services_offered' : 'ul.list-col2 li',
    'countries': 'div.service-offered2 > ul.square > li',
    'address' : "ul.clearfix li:-soup-contains('Address :')",
    'agency_name' : "ul.clearfix li:-soup-contains('Agency Name :')",
    'established' : "div.right-body > div.other-details > span.details",

}

results = {
    'location': [],
    'name': [],
    'profile_link': [],
    'mission_statement': [],
    'services_offered' : [],
    'countries' : [],
    'address' : [],
    'agency_name' : [],
    'established' : [],
}

def scrape_website(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result_for_page = dict()    

    try:
        mission_statement = soup.select(CSS_SELECTOR['mission_staement'])[0].text    
    except:
        mission_statement = '!not-found'
    
    try:
        services_offered = soup.select(CSS_SELECTOR['services_offered'])
        services_offered = [service.text for service in services_offered]
        services_offered = ', '.join(services_offered)
    except:
        services_offered = '!not-found'
    
    # countries = soup.select(CSS_SELECTOR['countries'])
    # print(countries[0].text)
    # countries = [country.text for country in countries]
    # print(countries)
    try:
        countries = soup.select(CSS_SELECTOR['countries'])
        countries = [country.text for country in countries]
        countries = ', '.join(countries)

    except:
        countries = '!not-found'
    
    try:
        address = soup.select(CSS_SELECTOR['address'])[0].text
    except:
        address = '!not-found'
    
    try:
        agency_name = soup.select(CSS_SELECTOR['agency_name'])[0].text
    except:
        agency_name = '!not-found'
    
    try: 
        established = soup.select(CSS_SELECTOR['established'])[0].text
    except:
        established = '!not-found'

    result_for_page['mission_statement'] = mission_statement
    result_for_page['services_offered'] = services_offered
    result_for_page['countries'] = countries
    result_for_page['address'] = address
    result_for_page['agency_name'] = agency_name
    result_for_page['established'] = established
    return result_for_page


def scrape_data():
    urls = pd.read_excel('result.xlsx')

    for i in range(1801,len(urls)):
        url = urls['profile_link'][i]
        name = urls['name'][i]
        location = urls['location'][i]

        results['profile_link'].append(url)
        results['name'].append(name)
        results['location'].append(location)

        page_data = scrape_website(url)
        for key, value in page_data.items():
            results[key].append(value)

        if(i%100 == 0):
            print(i)
            pd.DataFrame(results).to_excel(f'progress/website_results_{i}.xlsx', index=False)
    
    pd.DataFrame(results).to_excel('website_results.xlsx', index=False)

scrape_data()
        
