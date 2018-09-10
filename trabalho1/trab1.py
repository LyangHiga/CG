#! /usr/bin/env python
# coding=utf-8

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


# setting globals
#x and y size screen
DIMX = 640 
DIMY = 480 

#cliked points and the new points after curve smoothing
points = [] 
smooth_points = []


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
    for point in points:
        glVertex2f(point[0], point[1]) 
    glEnd()

    #Draw the line between two points
    glBegin(GL_LINE_STRIP)
    for point in points:
        glVertex2f(point[0], point[1])
    glEnd()


    glFlush()

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        #we should count y from top-down
        points.append([x, DIMY - y])
        glutPostRedisplay()

def keyboard(key, x, y):
    global points

    key = key.decode("utf-8")
    #smooth 
    if str(key) == 's': 
        smooth()

    #clear the points
    if str(key) == 'c':
        points = []

    glutPostRedisplay()



#split the line in 4 and add each new point to smooth_points
def split_four(point):

    if (point+1) != len(points):

        #midpoint
        mx = (points[point][0] + points[point+1][0])/2
        my = (points[point][1] + points[point+1][1])/2

        #halve between the first point and the midpoint
        x1 = (mx + points[point][0])/2
        y1 = (my + points[point][1])/2

        #halve between the second point and the midpoint
        x2 = (mx + points[point+1][0])/2
        y2 = (my + points[point+1][1])/2

        smooth_points.append([x1, y1]) 
        smooth_points.append([mx, my]) 
        smooth_points.append([x2, y2]) 


def smooth():
    global points, smooth_points

    smooth_points = []
    smooth_points.append(points[0])

    for index, point in enumerate(points):
        split_four(index)

    smooth_points.append(points[-1])

    points = smooth_points


if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(DIMX,DIMY)
    glutCreateWindow("Smooth Curve")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  # Determinando o tipo da janela com um buffer duplo
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()