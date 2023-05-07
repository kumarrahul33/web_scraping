import sys
import ssl
import json
import pandas as pd
import csv
import os
import urllib.parse

save_progress_at = 20 

domain_data = dict()

class Json_Parsing_Error(Exception):
    def __init(self,message="got the data from the api but could not parse"):
        self.message = message
        super().__init__(self.message)

class SERP_error(Exception):
    def __init(self,message="error while fetching data from the serp api"):
        self.message = message
        super().__init__(self.message)

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

NAME_DOMAIN_COL = 'ZoomInfo'

# NAME_COMPANY_COL = 'Company Name'

def getSerpResults(domain):
    global opener
    domain = urllib.parse.quote(domain.encode('utf8'))
    try:
        return opener.open(f'https://www.google.com/search?q={domain}+%22zoominfo%22&lum_json=1').read()
    except Exception as e:
        print(e)
        print(domain)
        raise SERP_error

def get_top_links(keyword):
    try:
        j_data = json.loads(getSerpResults(keyword))
        return [x['link'] for x in j_data['organic']]
    except SERP_error:
        return []
    except Exception as e:
        print(e)
        raise Json_Parsing_Error 


def dump_links(file_path, start , end):
    search_keywords = pd.read_excel(file_path)
    data_entries = {
        # 'company_name':[],
        'domain_name': [],
        'url1':[],
        'url2':[],
        'url3':[],
    }
    assert end > start
    start = start%len(search_keywords)
    # end = len(search_keywords)%end
    if end > len(search_keywords):
        end = len(search_keywords)

    for i in range(start,end):
#put the coloumn heading here
        keyword = search_keywords[NAME_DOMAIN_COL][i]

        if not keyword in domain_data.keys():
            links = []
            if keyword != "NullEntry":
                count = 0
                try:
                    top_links = get_top_links(keyword)
                except Json_Parsing_Error:
                    top_links = []
                except Exception as e:
                    print(e)
                    top_links = []
                
                for x in top_links:
                    print(x)
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

        # data_entries['company_name'].append(search_keywords[NAME_COMPANY_COL][i])
        data_entries['domain_name'].append(search_keywords[NAME_DOMAIN_COL][i])
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
