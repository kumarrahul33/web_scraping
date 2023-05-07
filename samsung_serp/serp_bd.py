import sys
import ssl
import json
import pandas as pd
import csv
import os

save_progress_at = 20 

domain_data = dict()

ssl._create_default_https_context = ssl._create_unverified_context
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
    opener = request.build_opener(
        request.ProxyHandler(
            {'http': 'http://brd-customer-hl_4933e401-zone-serp_zoominfo:w7i2uuekyf5a@zproxy.lum-superproxy.io:22225',
            'https': 'http://brd-customer-hl_4933e401-zone-serp_zoominfo:w7i2uuekyf5a@zproxy.lum-superproxy.io:22225'}))
if sys.version_info[0]==3:
    import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': 'http://brd-customer-hl_4933e401-zone-serp_zoominfo:w7i2uuekyf5a@zproxy.lum-superproxy.io:22225',
            'https': 'http://brd-customer-hl_4933e401-zone-serp_zoominfo:w7i2uuekyf5a@zproxy.lum-superproxy.io:22225'}))


def getSerpResults(domain):
    global opener
    try:
        return opener.open(f'https://www.google.com/search?client=firefox-b-d&q=Buy+Samsung+phone+online+&lum_json=1').read()
    except:
        print(domain)
        return None

def dump_json(keyword):
    try:
        j_data = json.loads(getSerpResults(keyword))
        with open('result.json','w') as f:
            json.dump(j_data,f,indent=4)
        # return [x['link'] for x in j_data['organic']]
    except:
        return []


def dump_links(file_path, start , end):
    search_keywords = pd.read_excel(file_path)
    data_entries = {
        'company_name':[],
        'domain_name': [],
        'url1':[],
        'url2':[],
        'url3':[],
    }

    for i in range(start,end + 1):
#put the coloumn heading here
        keyword = search_keywords["Domain"][i]

        if not keyword in domain_data.keys():
            links = []
            if keyword != "NullEntry":
                count = 0
                for x in get_top_links(keyword):
                    count += 1
                    if 'zoominfo' in x:
                        links.append(x)
                    if len(links) >= 3 :
                        break
                    if count >= 5:
                        break
                while len(links) < 3:
                    links.append("NotAvailable")
            else:
                links = ['NullEntry','NullEntry','NullEntry']
            domain_data[keyword] = links
        else:
            links = domain_data.get(keyword)
        print(links)

        data_entries['company_name'].append(search_keywords["Company Name"][i])
        data_entries['domain_name'].append(keyword)
        data_entries['url1'].append(links[0])
        data_entries['url2'].append(links[1])
        data_entries['url3'].append(links[2])

        if not os.path.exists(f"serp_progress_files/serp{start}_{end}"):
            os.makedirs(f"serp_progress_files/serp{start}_{end}/")

        if i%save_progress_at == 0:
            pd.DataFrame(data_entries).to_excel(f"serp_progress_files/serp{start}_{end}/save_SerpProgress_{i}.xlsx")

        if os.path.isfile(f"serp_progress_files/serp{start}_{end}/save_SerpProgress_{i-save_progress_at}.xlsx"):
            os.remove(f"serp_progress_files/serp{start}_{end}/save_SerpProgress_{i-save_progress_at}.xlsx")

    if not os.path.exists("serp_dump_files/"):
        os.makedirs("serp_dump_files/")
    pd.DataFrame(data_entries).to_excel(f"serp_dump_files/serp_dump_{start}_{end}.xlsx")

# def testing():
#     keyword = "https://www.zoominfo.com/c/fabfashionmallcom/369394810" 
#     links = []
#     if keyword != "NullEntry":
#         count = 0
#         for x in get_top_links(keyword):
#             count += 1
#             if 'zoominfo' in x:
#                 links.append(x)
#             if len(links) >= 3 :
#                 break
#             if count >= 5:
#                 break
#         while len(links) < 3:
#             links.append("NotAvailable")
#     else:
#         links = ['NullEntry','NullEntry','NullEntry']
#     domain_data[keyword] = links
#     else:
#         links = domain_data.get(keyword)
#     print(links)
