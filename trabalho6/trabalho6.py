#! /usr/bin/env python
# coding=utf-8

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from operator import attrgetter
from math import acos
import sys

from Delaunay import Delaunay

#6th home work from Graphics Computer at UFRJ by Lyang Higa Cano

'''Instruction
    Just click to collect points
    press b to bild the triangulation
    press s to smooth the triangulation
    press c to start again
'''

# setting globals

#x and y size screen
DIMX = 640 
DIMY = 480 
INF = 999999
LAMBDA = 0.3

#stop collecting points
stop = False
points = [] 
ch_points = []
triangles = []


class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "point(%s,%s)"%(str(self.x),str(self.y))

    def __add__(self,v):
        return Point(self.x+v.x, self.y+v.y)
    
    def __sub__(self,v):
        return Point(self.x-v.x, self.y-v.y)


class Vector:
    
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return "vector(%s,%s)"%(str(self.p1),str(self.p2))

    def __mul__(self, v):
        return ( ((self.p2.x - self.p1.x ) * (v.p2.x - v.p1.x))+ ((self.p2.y - self.p1.y ) * (v.p2.y - v.p1.y)) )

    def euclian_norm(self):
        return float( (self.p1.x - self.p2.x)**(2) + (self.p1.y - self.p2.y)**(2) )**(0.5)

    def angle(self,v):
        a = self.euclian_norm()
        b = v.euclian_norm()
        if( ( (self.p2.x == self.p1.x) and (self.p2.y == self.p1.y) ) or ( (v.p2.x == v.p1.x) and (v.p2.y == v.p1.y)) ):
            return INF
        c = (self * v)/ ( a * b )
        c = float('%.3f'%(c))
        return acos(c)
        

class Convex_hull:

    pl = []

    def __init__(self,p_list):
        self.p_list = p_list

    def jarvis(self):
        p1 = min(self.p_list,key=attrgetter('y'))
        self.pl.append(p1)
        p0 = Point(0,0)
        p = Point(1,0)  
        v0 = Vector(p0,p)
        p2 = self.next(v0)
        self.pl.append(p2)
        i = 0
        px = p0
        while(px!=p1):
            vx = Vector(self.pl[-2],self.pl[-1])
            px = self.next(vx)
            self.pl.append(px)
        return self.pl 

    def next(self,v0):
        last_p = self.pl[-1]
        min_ang = INF
        p0 = Point(0,0)
        for p in self.p_list:
            v = Vector(last_p,p)
            a = v0.angle(v)
            if(a < min_ang and a!= 0 ):
                min_ang = a
                p0 = p
        return p0


def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,DIMX,0.0,DIMY)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Draw a new point when it's cliked
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p.x,p.y) 
    glEnd()

    #Draw the line between ch two points
    glBegin(GL_LINE_STRIP)
    for p in ch_points:
        glVertex2f(p.x,p.y)
    glEnd()

    #Draw the triangles
    glBegin(GL_LINE_STRIP)
    for t in triangles:
        glVertex2f(points[t[0]].x, points[t[0]].y)
        glVertex2f(points[t[1]].x, points[t[1]].y)
        glVertex2f(points[t[2]].x, points[t[2]].y)    
    glEnd()


    glFlush()

def mouse(button, state, x, y):
    global points, stop

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and stop==False:
        #we should count y from top-down
        p = Point(x,DIMY - y)
        points.append(p) 

    glutPostRedisplay()


def keyboard(key, x, y):
    global points,ch_points, stop, triangles

    key = key.decode("utf-8")
    
    #clear the points
    if str(key) == 'c':
        points = []
        ch_points = []
        stop =False

    #build the triangulation
    if str(key) == 'b':
        stop = True
        convex_hull_bilder()
        #triangulation
        tri = Delaunay()
        for ponto in points:
            tri.addPoint(ponto)

        triangles = tri.tri()

    if str(key) == 's':
        smooth()
        tri = Delaunay()
        for ponto in points:
            tri.addPoint(ponto)

        triangles = tri.tri()

    glutPostRedisplay()

def convex_hull_bilder():
    global points,ch_points
    ch = Convex_hull(points)
    ch.pl = []
    ch.jarvis()
    ch_points = ch.pl

def smooth():
    global points, triangles
    v_old = points[-1]
    x=0
    y=0
    for i in range(len(points)):
        x+= points[i].x - v_old.x
        y+= points[i].y - v_old.y
    x /= len(points)
    y /= len(points)
    x = v_old.x + (LAMBDA * x)
    y = v_old.y + (LAMBDA * y)
    v_new = Point(x,y)
    points[-1] = v_new
 
    
if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(DIMX,DIMY)
    glutCreateWindow("Triangulation - Smoothing")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()