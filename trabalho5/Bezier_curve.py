#! /usr/bin/env python
# coding=utf-8
from Point import Point

class Bezier_curve:

    def __init__(self, points, bezier):
        self.points = points
        self.bezier = bezier
        self.steps = 300


    def curve(self):
        i = 1
        self.bezier.append(self.points[0]) 

        while i < self.steps+1: 
            self.bezier.append(self.next_point(i))
            i = i+1

        self.bezier.append(self.points[-1]) 

        return self.bezier

    def next_point(self, step):
        t = (1.0/self.steps) * step 
        
        x = ( (1-t)**3 * self.points[0].x ) + ( 3*t *(1-t)**2 * self.points[1].x ) + ( (3*t)**2 *(1-t) * self.points[2].x ) + ( t**3 * self.points[3].x )
        y = ( (1-t)**3 * self.points[0].y ) + ( 3*t *(1-t)**2 * self.points[1].y ) + ( (3*t)**2 *(1-t) * self.points[2].y ) + ( t**3 * self.points[3].y )
        z = ( (1-t)**3 * self.points[0].z ) + ( 3*t *(1-t)**2 * self.points[1].z ) + ( (3*t)**2 *(1-t) * self.points[2].z ) + ( t**3 * self.points[3].z )

        np = Point(x, y, z)
        return np