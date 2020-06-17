# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:15:53 2020

@author: joshu
"""

from fastkml import kml
import dataprocessing




    
def findprecinct(p, dat):
    k = kml.KML()
    precincts = k.from_string(dat)
    features = list(precincts.features())
    print(features)
    f2 = list(features[0].features())
    print(f2)
    f3 = list(f2[0].features())
    print(f3)
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = dataprocessing.getPolygon(finallist)
        if dataprocessing.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
        
        
def finddistrict(p, dat):
    k = kml.KML()
    districts = k.from_string(dat)
    features = list(districts.features())
    print(features)
    f2 = list(features[0].features())
    print(f2)
    f3 = list(f2[0].features())
    print(f3)
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = dataprocessing.getPolygon(finallist)
        if dataprocessing.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
            