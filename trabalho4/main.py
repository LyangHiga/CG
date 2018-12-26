# coding=utf-8

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy

from Delaunay import Delaunay
from Convex_hull import FechoConvexo

# setting globals

#x and y size screen
DIMX = 640 
DIMY = 480 

points = [] 
#triangulos = []
#poligono = []

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
'''
def main():
    # Inicializa glut e cria janela
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  # Determinando o tipo da janela com um buffer duplo
    # e o modelo de representação de cores

    glutInitWindowSize(DIMX, DIMY)  # Tamanho da tela é 600x600
    #glutCreateWindow('Trabalho 4 - Larissa Galeno - Delaunay')
    glutMouseFunc(mouse)
    #glutKeyboardFunc(keyboard)

    glutDisplayFunc(display)
    glutMainLoop()

    return
'''

'''
def display():
    global triangulos
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Mudando a cor do fundo para branco
    glClear(GL_COLOR_BUFFER_BIT)  # Carregando a cor do fundo no Buffer

    glPointSize(4.0)
    glColor3f(0.4, 0.4, 0.4)

    #Draw a new point when it's cliked
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p.x,p.y) 
    glEnd()

    glPointSize(4.0)
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINE_STRIP)

    for ponto in poligono:
        glVertex2f(ponto[0], ponto[1])  # Desenhando as linhas entre os pontos do Fecho Convexo

    glEnd()

    glPointSize(4.0)
    glColor3f(0.4, 0.4, 0.4)

    for triangulo in triangulos:
        glBegin(GL_LINE_STRIP)

        glVertex2f(conj_pontos[triangulo[0]][0], conj_pontos[triangulo[0]][1])
        glVertex2f(conj_pontos[triangulo[1]][0], conj_pontos[triangulo[1]][1])
        glVertex2f(conj_pontos[triangulo[2]][0], conj_pontos[triangulo[2]][1])
        glEnd()

    glFlush()
    glutSwapBuffers()
'''

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Draw a new point when it's cliked
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p.x,p.y) 
    glEnd()


    glFlush()

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        p = Point(x,DIMY - y)
        points.append(p) 
        #conj_pontos.append([p.x, p.y])  # Adicionando a minha lista de entrada os pontos com as coordenadas certas
        glutPostRedisplay()

def keyboard(key, x, y):
    global points

    key = key.decode("utf-8")
    
    #clear the points
    if str(key) == 'c':
        points = []


    if str(key) == 'b':
        fechoConvexo = FechoConvexo(points)
        poligono = fechoConvexo.jarvis()

        triangulacao = Delaunay()
        for ponto in points:
            triangulacao.adicionaPonto(ponto)

        triangulos = triangulacao.pegaTriangulos()
        print(triangulos)



    glutPostRedisplay()



'''
def keyboard(key, x, y):
    global conj_pontos, triangulos, poligono

    key = key.decode("utf-8")
    if str(
            key) == 'r':  # Apertar a tecla r para dizer ao algoritmo que o usuário acabou de entrar com o conjunto de pontos
        
          #  Nesse caso se o usuário apertar 'r' o programa irá entende que o usuário já entrou com o conjunto de pontos
    
        # Se o usuário apertar r devo começar o algorimo da Traingulação
        fechoConvexo = FechoConvexo(conj_pontos)
        poligono = fechoConvexo.jarvis()

        triangulacao = Delaunay()
        for ponto in conj_pontos:
            triangulacao.adicionaPonto(ponto)

        triangulos = triangulacao.pegaTriangulos()
        print(triangulos)
        # print ("Triangulos: " + (str)(triangulacao.triangulos))
        # print ("ArestaParaTriangulos: " + (str)(triangulacao.arestaParaTriangulo))
        # print ("ArestasBorda: " + (str)(triangulacao.arestasBorda))

    if str(key) == 'b':  # Limpar o canvas
        conj_pontos = []
        poligono = []
        triangulos = []

    glutPostRedisplay()

'''

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(4.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,DIMX,0.0,DIMY)

if __name__ == '__main__':
    glutInit()
    glutInitWindowSize(DIMX,DIMY)
    glutCreateWindow("Convex Hull - Jarvis")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()