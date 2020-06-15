#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:40:15 2020

@author: joshua
"""
import computedistance
from pyspark.sql import Row




def handle_building(building,mental_health):
    address = building.house_no + " " + building.street_name
    latlong = computedistance.getLatLong(address)
    latlong2 = [mental_health.longitude, mental_health.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False
    
