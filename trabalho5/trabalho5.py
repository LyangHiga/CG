#! /usr/bin/env python
# coding=utf-8
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy

from Bezier_curve import Bezier_curve
from Point import Point


#5th home work from Graphics Computer at UFRJ by Lyang Higa Cano

'''Instruction
    press b to creat the Bezier Curve
    press c to start again
    press l to left rotation
    press r to right rotation
    press u to up rotation
    press d to down rotation
'''

# setting globals

#x and y size screen
DIMX = 640 
DIMY = 480 

points = [] 
bezier = []

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(4.0)
    

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Draw a new point randomly
    glBegin(GL_POINTS)
    for p in points:
        glVertex3f(p.x,p.y,p.z) 
    glEnd()

    #Draw the line between each point
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for p in points:
        glVertex3f(p.x,p.y,p.z) 
    glEnd()

    #to draw the bezier curve
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for bp in bezier:
        glVertex3f(bp.x, bp.y, bp.z)
    glEnd()

    glFlush()
    glutSwapBuffers()


def keyboard(key, x, y):
    global points,bezier

    key = key.decode("utf-8")
    
    #clear the points
    if str(key) == 'c':
        points = []
        bezier = []
        poligonal()

    #build the bezier curve
    if str(key) == 'b':
        curve = Bezier_curve(points, bezier)
        bezier = curve.curve()

    #left rotaion
    if str(key) == 'l': 
        glRotatef(-2.0, 0.0, 2.0, 0.0)

    #right rotation
    if str(key) == 'r': 
        glRotatef(2.0, 0.0, 2.0, 0.0)

    #up rotation
    if str(key) == 'u': 
        glRotatef(-2.0, 2.0, 0.0, 0.0)

    #down rotation
    if str(key) == 'd': 
        glRotatef(2.0, 2.0, 0.0, 0.0)

    glutPostRedisplay()

def poligonal():
    global points

    for i in range(4):
        p = Point(random.uniform(-0.8, 0.8),random.uniform(-0.8, 0.8),random.uniform(-0.8, 0.8))
        points.append(p) 


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(DIMX,DIMY)
    glutCreateWindow("Bezier Curve")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  
    poligonal()
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()