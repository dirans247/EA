#!/usr/bin/env python
# coding: utf-8

# In[2]

import pandas

from pandas.core import api
#EA DOC 
# This is an autoscript that uses data dump from Elemos and checks licenses against EAs REST API
# Written by Diran Edwards 01/11/2022
# Last edited by Diran Edwards 04/11/2022

import requests
import json
import pandas as pd
import numpy as np

from datetime import date
now = date.today()
nowString = str(now);


#from google.colab import files
#files.upload()
data = pd.read_excel("../data.xlsx") #this is the output from Elemos
#display(data.head())
df = pd.DataFrame(data)
wcls = df.loc[:,'Waste Carrier License No']
wcl = pd.unique(wcls)
#display(df.head())
display(wcl)
#curl -X GET "http://environment.data.gov.uk/public-register/waste-carriers-brokers/registration/"

#REST API endpoint
api_url = "http://environment.data.gov.uk/public-register/waste-carriers-brokers/registration/"

#testkey='CBDL258464'

from urllib.request import urlopen
from urllib.parse import quote


def search(reg):

    #check if not string
    if not type(reg) == str:
      print(f"\033[1;91mNOT found for: {reg}")
      return

    url = api_url + reg
    response = requests.get(url)
    if(response.status_code == 200):
    
      url = api_url + reg + '.json'
      response = urlopen(url).read().decode('utf8')
    
      display(url)
    
      print(f"\033[1;92mSucessfully found: {reg} license ")
      ea_info = json.loads(response)
      #print(ea_info)
      
      items=ea_info["items"]
      items_list_object = items[0]
      
      if "organization_name" in items_list_object["site"]["siteAddress"]:
        print(items_list_object["site"]["siteAddress"]["organization_name"])
      
      if "postcode" in items_list_object["site"]["siteAddress"]:
        print(items_list_object["site"]["siteAddress"]["postcode"])
      
      if "expiryDate" in items_list_object:
        print("Expiry Date" ,items_list_object["expiryDate"])
        if items_list_object["expiryDate"] >= nowString:
            print("Date ok")
        else:
            print("\033[1;91m Date expired")
            

      if items_list_object["tier"]["label"] == "Upper":
        print("\033[1;92mTier ", items_list_object["tier"]["label"])   
      else:
        print(f"\033[1;91mTier ", items_list_object["tier"]["label"])
    
      
      
        
      return ea_info
    
    else:
      print(f"\033[1;91m NOT found for: {reg}")
      return ""
    
#def info()):
   
i = 0
for string in wcl:    
    ea_info = search(string)
    print("-----------------")
    # print(ea_info)
    i += 1
    #break
print("\033[1;39mSearch finished")

##todo #tidy code


# In[ ]:




