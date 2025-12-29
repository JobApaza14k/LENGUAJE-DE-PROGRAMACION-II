from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def inicializar():
    """Configura el entorno OpenGL"""
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Fondo gris oscuro
    glPointSize(2)                    # Tamaño de los puntos
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() #matrix identidad
    glOrtho(-10.0, 10.0, -10.0, 10.0, -10.0, 10.0)  # Vista ortográfica 2D

def dibujar_UNA():
    glBegin(GL_LINE_STRIP)
    glVertex2f(-9, 5)     # superior izquierdo
    glVertex2f(-9, -5)    # inferior izquierdo
    glVertex2f(-6, -5)    # inferior derecho
    glVertex2f(-6, 5)     # superior derecho
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(-3, -5)    # línea izquierda (abajo)
    glVertex2f(-3, 5)     # línea izquierda (arriba)
    glVertex2f(-3, 5)     # diagonal arriba izquierda
    glVertex2f(0, -5)     # diagonal abajo derecha
    glVertex2f(0, -5)     # línea derecha (abajo)
    glVertex2f(0, 5)      # línea derecha (arriba)
    glEnd()

 
    glBegin(GL_LINES)
    glVertex2f(3, -5)     # izquierda abajo
    glVertex2f(4.5, 5)    # izquierda arriba
    glVertex2f(6, -5)     # derecha abajo
    glVertex2f(4.5, 5)    # derecha arriba
    glVertex2f(3.5, 0)    # barra del medio
    glVertex2f(5.5, 0)    # barra del medio
    glEnd()

    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Triangulo de puntos en OpenGL")  # b = evita error de ctypes
    inicializar()
    glutDisplayFunc(dibujar_UNA)
    glutMainLoop()

if __name__ == "__main__":
    main()
