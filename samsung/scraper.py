import requests
import pandas as pd

final_data = {
    'name': [],
    'address': [],
    'cityName': [],
    'area': [],
    'type': [],
    'zipCode': [],
    'phone': [],
    'homepageUrl': [],
    'productName': [],
    'industryName': [],
    'description': [],
    'latitude': [],
    'longitude': [],
    'id': [],
    'tier': [],
    'cert': [],
    'logoURL': [],
}

data_fields = ['name', 'address', 'cityName', 'area', 'type', 'zipCode', 'phone', 'homepageUrl', 'productName', 'industryName', 'description', 'latitude', 'longitude', 'id', 'tier', 'cert', 'logoURL']

def get_json_data(start):
    # url = f"https://searchapi.samsung.com/v6/front/b2b/partnerlocator/list?siteCode=in&start={start}&num=100&latitude=&longitude=&sortType=R&textFil=&tierFil=&typeFil=&industryFil=&productFil=aGN2y000002NzWtGAK&onlyFilterInfoYN=N&pageNum=1&prmYN=Y" 
    url = f"https://searchapi.samsung.com/v6/front/b2b/partnerlocator/list?siteCode=th&start={start}&num=100&latitude=&longitude=&sortType=R&textFil=&tierFil=&typeFil=&industryFil=&productFil=aGN2y000002NzWtGAK&onlyFilterInfoYN=N&pageNum=1&prmYN=Y"
    data = requests.get(url).json()
    for comp in data['response']['resultData']['partnerlocator']['partners']:
        # print(comp['name'], comp['address'], comp['phone'],  comp['homepageUrl']) 
        for field in data_fields:
            final_data[field].append(comp[field])

for i in range(0, 2):
    start = i * 100
    get_json_data(start)
    if(i%8 == 0):
        pd.DataFrame(final_data).to_excel(f'progress_{i}.xlsx', index=False)

pd.DataFrame(final_data).to_excel('samsung_thai.xlsx', index=False)