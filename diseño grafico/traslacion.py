from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

posx, posy = 0.0, 0.0


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
   
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 0.0)
    glTranslatef(posx, posy, 0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    glFlush()

def special_keys(key, x, y):
    global posx, posy
    paso = 0.05
    if key == GLUT_KEY_UP:
        posy += paso
    elif key == GLUT_KEY_DOWN:
        posy -= paso
    elif key == GLUT_KEY_LEFT:
        posx -= paso
    elif key == GLUT_KEY_RIGHT:
        posx += paso
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Transformacion geometrica 2D - Traslacion y Rotacion")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutMainLoop()

if __name__ == "__main__":
    main()
