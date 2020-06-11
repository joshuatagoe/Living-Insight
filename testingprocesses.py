# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:15:53 2020

@author: joshu
"""

from fastkml import kml
import dataprocessing
from dataprocessing import Point

k = kml.KML()


with open("Police Precincts.kml", 'rb') as myfile:
    doc=myfile.read()
    
k.from_string(doc)

features = list(k.features())
print(len(features))
print(features)
f2 = list(features[0].features())
print(f2)
f3 = list(f2[0].features())
#print(f3)
placemark1 = f3[0]
print(placemark1)
p1 = placemark1.__dict__.keys()
print(p1)
p1shape = placemark1.geometry
#print(p1shape)
#print(len(p1shape.geoms))
#print(list(p1shape.geoms))
def findprecinct(p):
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = dataprocessing.getPolygon(finallist)
        if dataprocessing.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
            

p = Point(-43.9999157921724, 40.72693471293184)
print(findprecinct(p))
#print(k.to_string(prettyprint=False))