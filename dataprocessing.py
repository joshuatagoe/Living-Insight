be# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:11:27 2020

@author: joshu
"""
import gmpy2

INF = 10000
    
class Point:
    def __init__(self,x, y):
        self.x = gmpy2.mpfr(str(x),200)
        self.y = gmpy2.mpfr(str(y),200)
    def get(self):
        return { "x" : self.x, "y" : self.y}
    def size(self):
        return 2;

def getPolygon(args):
    polygon = []
    for arg in args:
        polygon.append(Point(arg[0],arg[1]))
    return polygon
    

def isInside(polygon, n, p):
    #there must be at least 3 vertices in polygon
    if n<3:
        return False
    
    #create a point for line segment from p to infinite
    extreme = Point(INF, p.y)
    
    #count intersections of the above line with sides of polygon
    count = 0
    i = 0
    _next = (i+1)%n;
    
    #check if the line segment from 'p' to 'extreme' intersects
    #with the line segment from polygon[i] to polygon[next]
    if doIntersect(polygon[i], polygon[_next],p, extreme):
        #if the point 'p' is colinear with line segment 'i-next,
        #then check if it lies on segment. if it lies, return true,
        #otherwise false
        if orientation(polygon[i], p, polygon[_next]) == 0:
            return onSegment(polygon[i], p, polygon[_next])
        
        count+=1
    i=_next
    while i!=0:

        _next = (i+1)%n;
        #check if the line segment from 'p' to 'extreme' intersects
        #with the line segment from polygon[i] to polygon[next]
        if doIntersect(polygon[i], polygon[_next],p, extreme):
            #if the point 'p' is colinear with line segment 'i-next,
            #then check if it lies on segment. if it lies, return true,
            #otherwise false
            if orientation(polygon[i], p, polygon[_next]) == 0:
                return onSegment(polygon[i], p, polygon[_next])
            count+=1
            
        i=_next
        
        #return true if count is odd otherwise, return false
    return count%2==1 #same as count %2 ==1


def onSegment(p,q,r):
    if q.x <= max(p.x, r.x) and q.x  >= min(p.x, r.x) and q.y<=max(p.y, r.y) and q.y>=min(p.y, r.y):
        return True
    return False
def orientation(p, q, r):
    val = ((q.y-p.y) * (r.x - q.x)) - ((q.x-p.x)*(r.y-q.y))
    if val==0:
        return 0; #colinear
    if val>0: #clock or counterclock wise
        return 1
    else:
        return 2

def doIntersect(p1, q1, p2, q2):
    #Find the four orientations needed for general and 
    #special cases
    o1 = orientation(p1, q1,p2)
    o2 = orientation(p1,q1,q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    #general case
    if o1 != o2 and o3 !=o4:
        return True
    
    #special cases
    #p1, q1, and p2 aere colinear and p2 lie on segment p1q1
    if o1==0 and onSegment(p1,p2,q1):
        return True
    #p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if o2==0 and onSegment(p1,q2, q1):
        return True
    
    #p2,q2 and p1 are colinear and p1 lies on segment p2q2
    if o3==0 and onSegment(p2,p1,q2):
        return True
    
    #p2,q2 and q1 are colinear and q1 lies on segment p2q2
    if o4==0 and onSegment(p2,q1,q2):
        return True
    
    return False #doesn't fall in any of the above cases
 
    
if __name__ == "__main__":
    polygon1 = [Point(0,0), Point(10, 0), Point(10, 10), Point(0,10) ]
    n = len(polygon1)
    p = Point(20,20)
    if isInside(polygon1, n, p):
        print("Yes") 
    else:
        print("No")
        
  
    p = Point(5,5)
    if isInside(polygon1, n, p):
        print("Yes") 
    else:
        print("No")
        

    polygon2 = [ Point(0,0), Point(5,5), Point(5,0)]
    p = Point(3,3)
    n = len(polygon2) 
    if isInside(polygon2, n, p):
        print("Yes") 
    else:
        print("No")
        
  
    p = Point(5,1) 
    if isInside(polygon2, n, p):
        print("Yes") 
    else:
        print("No")
  
    p = Point(8,1)
    if isInside(polygon2, n, p):
        print("Yes") 
    else:
        print("No")
  
    polygon3 =  [Point(0,0), Point(10, 0), Point(10, 10), Point(0, 10)] 
    p = Point(-1,10)
    n = len(polygon3)
    if isInside(polygon3, n, p):
        print("Yes") 
    else:
        print("No")
  
    