import requests


data = {
    "website" : [],    
    "company_name" : [],    
    "aws_competencies_count" : [],    
    "partner_programs_count" : [],    
    "description" : [],    
    "target_client_base" : [],    
    "aws_service_validation_count" : [],    
    "aws_certifications_count" : [],    
    "aws_certifications" : [],    
    "headquarters" : [],    
    "aws_competencies" : [],    
    "practices_count" : [],    
    "customer_references_count" : [],    
    "location_count" : [],    
    "countries_located_in" : [],    
    "partners_programs" : [],    
    "industry" : [],    
    "customer_type" : [],    
    "customer_launches_count" : [],    
    "segment" : [],    
    "tech_expertise" : [],    
    "professional_service_type" : [],    
    "current_program_status" : [],    
    "partner_validated" : [],    
    "aws_services" : [],    
    "aws_profile_link" : [],    
}

def get_values(key, json):
    if(key == "website"):
        return json["website"]
    elif(key == "company_name"):
        return json["literal_name"]
    elif(key == "aws_competencies_count"):
        return json["competencies_count"]
    elif(key == "partner_programs_count"):
        return json["programs_count"]
    elif(key == "description"):
        return json["description"]
    elif(key == "target_client_base"):
        # print(type(json["target_client_base"]))
        return ",".join(json["target_client_base"])
    elif(key == "aws_service_validation_count"):
        return json["services_count"]
    elif(key == "aws_certifications_count"):
        return json["aws_certifications_count"]
    elif(key == "headquarters"):
        for i in json["office_address"]:
            try:
                if(i["location_type"][0] == "Headquarters"):
                    return i
            except:
                continue
    elif(key == "aws_competencies"):
        return ",".join(json["competency_membership"])
    elif(key == "practices_count"):
        return json["solutions_practice_count"]
    elif(key == "customer_references_count"):
        return json["references_reference_count"]
    elif(key == "location_count"):
        return len(json["office_address"])
    elif(key == "countries_located_in"):
        countries = [i["country"] for i in json["office_address"]]
        return ",".join(countries) 
    elif(key == "partner_programs"):
        return ",".join(json["program_membership"])+","+json["current_program_status"]+"_tier_services"
    elif(key == "industry"):
        return ",".join(json["industry"])
    elif(key == "customer_type"):
        return json["customer_launches_count"]
    elif(key == "customer_launches_count"):
        return json["customer_launches_count"]
    elif(key == "segment"):
        return ",".join(json["segment"])
    elif(key == "tech_expertise"):
        return ",".join(json["technology_expertise"])
    elif(key == "professional_service_type"):
        return ",".join(json["professional_service_types"])
    elif(key == "current_program_status"):
        return json["current_program_status"]
    elif(key == "partner_validated"):
        return json["partner_validated"]
    elif(key == "aws_services"):
        return ",".join(json["service_membership"])


BASE_URL = "https://partners.amazonaws.com/partners/"
def get_data(id):
    url = "https://api.finder.partners.aws.a2z.com/search?id={}&locale=en&sourceFilter=detailPage".format(id)
    # url = "https://api.finder.partners.aws.a2z.com/search?id={}&locale=en&sourceFilter=detailPage".format("0010L00001rFYIPQA4")
    response = requests.get(url)
    data["aws_profile_link"].append(BASE_URL + id)

    for(key, value) in data.items():
        if(key == "aws_profile_link"):
            continue
        try:
            data[key].append(get_values(key, response.json()["message"]["_source"]))
            # print(key, get_values(key, response.json()["message"]))
        except:
            data[key].append("not-found")

    # for key in data.keys():
    #     print(key, len(data[key]))



import pandas as pd
ids = pd.read_csv("france.csv")
count = 0
for row_index, row in ids.iterrows():
    count += 1
    if(count >= 5):
        break
    get_data(row['id'])
    print(row['id'])
    
pd.DataFrame(data).to_excel("scraped_data.xlsx")
    

