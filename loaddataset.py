# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 04:30:24 2020

@author: joshu
"""


import googlemaps
import pandas as pd
#import dataprocessing
from datetime import datetime
import testingprocesses

gmaps = googlemaps.Client(key='AIzaSyAElWTfe3ngljDcScZo52GYqo3CbT_KN6g')

# Geocoding an address

geocode_result = gmaps.geocode('348 Douglass St, Brooklyn, NY 11217')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
print("Geocode")
print()
print("checking for borough")
print(geocode_result)
print("Reverse Geocode")
print()
print(reverse_geocode_result)
print()
geocode_result = gmaps.geocode('Northeast Bronx')
print(geocode_result)


data = pd.read_csv("/home/joshua/Downloads/Air_Quality.csv")
print(data)
dataiwant = data[data.geo_type_name=="UHF42"]
print(dataiwant)
geo_entities = []
for index,row in dataiwant.iterrows():
    
    geo_entities.append(row.geo_entity_name)
    
whatineed =  set(geo_entities)


    
    
    

