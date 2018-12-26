#! /usr/bin/env python
# coding=utf-8
class Point:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "point(%s,%s,%s)"%(str(self.x),str(self.y),str(self.z))

    def __add__(self,v):
        return Point(self.x+v.x, self.y+v.y, self.z+v.z)
    
    def __sub__(self,v):
        return Point(self.x-v.x, self.y-v.y, self.z-v.z)