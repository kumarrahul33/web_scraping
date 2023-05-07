import pandas as pd
from googletrans import Translator


def thai_to_english(text):
    translator = Translator()
    translation = translator.translate(text, src='th', dest='en')
    return translation.text

 
df = pd.read_excel('samsung_thai.xlsx')
# go over the rows of df
for index, row in df.iterrows():
    # get the text from the row
    th_address = row['address']
    th_city = row['cityName']
    # translate the text
    en_address = thai_to_english(th_address)
    en_city = thai_to_english(th_city)
    # add the translation to the row
    df.loc[index, 'address'] = en_address 
    df.loc[index, 'cityName'] = en_city
    print(index)

df.to_excel('samsung_thai_english.xlsx', index=False)