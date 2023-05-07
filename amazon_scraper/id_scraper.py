import requests
import pandas as pd
API_URL = "https://api.finder.partners.aws.a2z.com/search?locale=en&highlight=on&sourceFilter=searchPage&size=229&location=France"

# make a get request at this URL and show the response
response = requests.get(API_URL)
# print(response.json())
data = response.json()["message"]["results"]

final_ids = {
   "id" : [],
}
for d in data:
    final_ids["id"].append(d["_id"])
    

print(len(final_ids["id"]))
pd.DataFrame(final_ids).to_csv("france.csv")




