#! /usr/bin/env python
# coding=utf-8

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys


#Second home work from Graphics Computer at UFRJ by Lyang Higa Cano

# setting globals

#x and y size screen
DIMX = 640 
DIMY = 480 


points = [] 
test_points = []
#stop collecting points
stop = False
#Only true when we want to test if a point is insed of the polygon
test = False

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

    #Draw a new test point when it's cliked
    glBegin(GL_POINTS)
    for point in test_points:
        glVertex2f(point[0], point[1]) 
    glEnd()

    #Draw the line between two test points
    glBegin(GL_LINE_STRIP)
    for point in test_points:
        glVertex2f(point[0], point[1])
    glEnd()


    glFlush()

def mouse(button, state, x, y):
    global test, stop, points, test_points

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and stop == False:
        #we should count y from top-down
        points.append([x, DIMY - y]) 

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and test == True:
        if len(test_points) >= 2:
            print("You must use only two points!")
            test = False
        else:
            test_points.append([x, DIMY - y])

    glutPostRedisplay()


def keyboard(key, x, y):
    global points, test_points, stop,test

    key = key.decode("utf-8")
    
    #clear the points
    if str(key) == 'c':
        points = []
        test_points = []
        stop = False
        test = False

    #build the polygon
    if str(key) == 'b':
        polygon_bilder()

    #test if the point clicked is inside of the polygon
    if str(key) == 't':
        inside_point_test()


    glutPostRedisplay()

def polygon_bilder():
    global points, stop, test
    points.append(points[0])
    #collect the testing points
    stop = True
    test = True
    print("Click in a point outside of the polygon and in any point that you want to test")

def inside_point_test():
    global test_points, test
    n = 0
    if len(test_points) > 2:
        print("You must use only two points!,press C to start again.")
        test = False
        test_points = []
    else:
        for i in range(len(points)):
            if(interception(points[i-1],points[i],test_points[0],test_points[1]) == True):
                n+=1
        if(n%2 == 0):
            print("Outside!")
        else:
            print("inside!")

#cross product between ab x cd
def cross_prod_2d(a,b,c,d):
    x1 = b[0] - a[0]
    y1 = b[1] - a[1]
    x2 = d[0] - c[0]
    y2 = d[1] - c[1]
    cp = (x1*y2) - (x2*y1)
    return (cp)

#checks if there is an interception between ab cd
def interception(a,b,c,d):
    if( (cross_prod_2d(a,b,a,c) * cross_prod_2d(a,b,a,d)) < 0 and (cross_prod_2d(c,d,c,a) * cross_prod_2d(c,d,c,b)) < 0 ):
        return True

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(DIMX,DIMY)
    glutCreateWindow("Smooth Curve")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()