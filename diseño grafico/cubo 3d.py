from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import sys

textures = []

def loadTexture(image):
    img = Image.open(image)
    img_data = img.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
    width, height = img.size
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    textures.append(tex)

def drawCube():
    glBegin(GL_QUADS)
    # cara frontal
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexCoord2f(0,0); glVertex3f(-1,-1, 1)
    glTexCoord2f(1,0); glVertex3f( 1,-1, 1)
    glTexCoord2f(1,1); glVertex3f( 1, 1, 1)
    glTexCoord2f(0,1); glVertex3f(-1, 1, 1)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1, 1, 1, 0)
    drawCube()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(600,600)
    glutCreateWindow("Cubo 3D con Imágenes")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    for i in range(1, 7):
        loadTexture(f"img{i}.jpg")
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

main()

