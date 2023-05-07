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
}

results = {
    'location': [],
    'name': [],
    'profile_link': [],
}

def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        names = soup.select(CSS_SELECTOR['name'])
        locations = soup.select(CSS_SELECTOR['location'])
        profile_links = soup.select(CSS_SELECTOR['profile_link'])

        # for name in names:
        for i in range(len(names)):
            results['name'].append(names[i].text)
            results['location'].append(locations[i].text.strip())
            results['profile_link'].append(profile_links[i]['href'])

for i in range(1, 112):
    if i == 1 :
        url = BASE_URL + '.htm'
    else: 
        url = BASE_URL + '-' + str(i) + '.htm'
    scrape_data(url) 

    if i%10 == 0 and i > 0:
        # print('Scraped {} pages'.format(i))
        pd.DataFrame(results).to_excel(f'progress/result_{i}.xlsx', index=False)

pd.DataFrame(results).to_excel('result.xlsx', index=False)




