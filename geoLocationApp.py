import pandas as pd
import numpy as np
import requests
import time
import re
import json
from tqdm.auto import tqdm

def getArabicAndEnglishDistrict(response):
    AllDistricts = []
    addresses = []
    iterations = json.dumps(response).count("formatted_address")
    Arabic_District = ''
    English_District = ''
    for n in range(iterations):
        addresses += re.split('، |, ',response['results'][n]['formatted_address'])
    
    for i in addresses:
        if("حي" in i):
            Arabic_District = i
    
    for i in addresses:
        if("District" in i):
            English_District = i
    
    AllDistricts.append(Arabic_District)
    AllDistricts.append(English_District)
    AllDistricts.append(response['results'][1]['formatted_address'])
    
    return AllDistricts

data = pd.read_csv("data.csv")

listx = data['x'].tolist()
listy = data['y'].tolist()

Arabic_Districts_data = []
English_Districts_data = []
All_Districts_data = []


for i in tqdm(range(len(listx))):
    coord = str(listx[i])+","+str(listy[i])
    key = "YOUR-KEY-HERE"
    URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+coord+"&key="+key
    r = requests.get(url = URL)
    response = r.json()
    
    Arabic_District = getArabicAndEnglishDistrict(response)[0]
    English_District = getArabicAndEnglishDistrict(response)[1]
    All_Districts = getArabicAndEnglishDistrict(response)[2]
    
    Arabic_Districts_data.append(Arabic_District)
    English_Districts_data.append(English_District)
    All_Districts_data.append(All_Districts)
    
    #print(coord,", ",Arabic_District," , ",English_District)

data['Arabic_Districts'] = Arabic_Districts_data
data['English_Districts'] = English_Districts_data
data['All_Districts'] = All_Districts_data

data.to_csv("CSV_result.csv")
data.to_excel("Excel_result.xlsx")