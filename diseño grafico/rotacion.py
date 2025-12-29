from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angulo = 0.0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    global angulo
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Aplicar rotación
    glRotatef(angulo, 0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 0.5)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-0.5, -0.5)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.5, -0.5)
    glEnd()

    glFlush()

def special_keys(key, x, y):
    global angulo
    if key == GLUT_KEY_LEFT:
        angulo += 5
    elif key == GLUT_KEY_RIGHT:
        angulo -= 5
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Rotacion con teclado - PyOpenGL")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if _name_ == "_main_":
    main()
