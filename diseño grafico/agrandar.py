from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

escala = 1.0

def inicializar():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glPointSize(2)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

def dibujar_triangulo():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScalef(escala, escala, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.5)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
    glFlush()

def keyboard(key, x, y):
    global escala
    if key == b'+':
        escala += 0.1
    elif key == b'-':
        escala -= 0.1
        if escala < 0.1:
            escala = 0.1
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Transformacion Geometrica 2D - Escalado")
    inicializar()
    glutDisplayFunc(dibujar_triangulo)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()

