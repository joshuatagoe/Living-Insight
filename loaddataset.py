# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 04:30:24 2020

@author: joshu
"""


import googlemaps
import pandas as pd
import dataprocessing
from datetime import datetime
import testingprocesses

gmaps = googlemaps.Client(key='')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
print("Geocode")
print()
print(geocode_result)
print("Reverse Geocode")
print()
print(reverse_geocode_result)
print()
geocode_result = gmaps.geocode('Northeast Bronx')
print(geocode_result)


data = pd.read_csv("Air_Quality.csv")
print(data)
dataiwant = data[data.geo_type_name=="UHF42"]
print(dataiwant)
geo_entities = []
for index,row in dataiwant.iterrows():
    
    geo_entities.append(row.geo_entity_name)
    
whatineed =  set(geo_entities)

for x in whatineed:
    print(x)
    geocode = gmaps.geocode(x)
    lat = geocode[0]['geometry']['location']['lat']
    lng = geocode[0]['geometry']['location']['lng']
    location = dataprocessing.Point(lng,lat)
    print(testingprocesses.findprecinct(location))
    
    
    

