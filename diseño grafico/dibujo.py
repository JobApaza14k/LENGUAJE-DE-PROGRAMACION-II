from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np

def inicializar():
    glClearColor(0, 0, 0, 1)
    glColor3f(1, 1, 0)
    glPointSize(3)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho2D(-1.5, 1.5, -0.5, 1.5)

def dibujar_funcion():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor(1.0, 1.0, 1.0)
    
    glBegin(GL_LINE)
    glVertex2f(-1.5, 0.0)
    glVertex2f(1.5, 0.0)
    glVertex2f(0.0, -0.5)
    glVertex2f(0.0, 1.5)
    glEnd()

    glColor(0.2, 0.0, 1.0)
    glBenig(GL_LINES_STRIP)
    for x in np.linspace(-1.2, 1.2, 200):
        y=x**2
        glVertex2f(x,y)
    glEnd()
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"ecuacion: y=x^2")
    inicializar()
    glutDisplayFunc(dibujar_curva)
    glutMainLoop()

if __name__ == "__main__":
    main()
