#!/usr/bin/python
# Curvas y Triedro de Frenet

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
from OpenGL.GLUT import *
import sys, time
# from math import sin,cos,sqrt,pi
from sympy.core.sympify import sympify
from sympy import *
from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB
vec4 = GLfloat_4

tStart = t0 = time.time()
frames = 0
rotationRate = 1.01
vertices = []
tangentes = []
normales = []
binormales = []
evoluta = []
camara_angulo_x = 0.0
camara_angulo_y = 0.0

ventana_pos_x  = 50
ventana_pos_y  = 50
ventana_tam_x  = 1024
ventana_tam_y  = 800

frustum_factor_escala = 1.0
frustum_dis_del = 0.1
frustum_dis_tra = 10.0
frustum_ancho = 0.5 * frustum_dis_del

frustum_factor_escala = 1.0

vertice_actual = 0
direccion = 1
velocidad = 0
vertice_animado = 0

show_frames = False
dibujoEvoluta = False


def fijarProyeccion():
    ratioYX = float(ventana_tam_y) / float(ventana_tam_x)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(-frustum_ancho, +frustum_ancho, -frustum_ancho*ratioYX, +frustum_ancho*ratioYX, +frustum_dis_del, +frustum_dis_tra)

    glTranslatef( 0.0,0.0,-0.5*(frustum_dis_del+frustum_dis_tra))

    glScalef( frustum_factor_escala, frustum_factor_escala,  frustum_factor_escala )


def fijarViewportProyeccion():
    glViewport( 0, 0, ventana_tam_x, ventana_tam_y )
    fijarProyeccion()

def fijarCamara():

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(camara_angulo_x,1,0,0)
    glRotatef(camara_angulo_y,0,1,0)


def framerate():
    global t0, frames
    t = time.time()
    frames += 1
    if t - t0 >= 5.0:
        seconds = t - t0
        fps = frames/seconds
        print ("%.0f frames in %3.1f seconds = %6.3f FPS" % (frames,seconds,fps))
        t0 = t
        frames = 0

def dibujarEjes():

    long_ejes = 10.0

    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

    # Ancho de línea
    glLineWidth( 1.5 );
    # dibujar tres segmentos
    glBegin(GL_LINES)

    # eje X, color rojo
    glColor3f( 1.0, 0.0, 0.0 )
    glVertex3f( -long_ejes, 0.0, 0.0 )
    glVertex3f( +long_ejes, 0.0, 0.0 )
    # eje Y, color verde
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.0, -long_ejes, 0.0 )
    glVertex3f( 0.0, +long_ejes, 0.0 )
    # eje Z, color azul
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, -long_ejes )
    glVertex3f( 0.0, 0.0, +long_ejes )

    glEnd()

def dibujarObjetos():
    # Dibujar la curva
    glColor3f(0.0,0.0,0.0)
    glLineWidth( 2.5 );
    glBegin(GL_LINE_STRIP)
    for v in vertices:
        glVertex3f(v[0],v[1],v[2])
    glEnd()

    # Dibujar el triedo del vértice actual
    glLineWidth( 3.5 )
    glBegin(GL_LINES)

    # Tangente
    glColor3f(0.0,0.0,1.0)
    glVertex3f(vertices[vertice_actual][0],vertices[vertice_actual][1],vertices[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + tangentes[vertice_actual][0],vertices[vertice_actual][1]+tangentes[vertice_actual][1],vertices[vertice_actual][2]+tangentes[vertice_actual][2])
    # Normal
    glColor3f(0.0,1.0,0.0)
    glVertex3f(vertices[vertice_actual][0],vertices[vertice_actual][1],vertices[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + normales[vertice_actual][0],vertices[vertice_actual][1]+normales[vertice_actual][1],vertices[vertice_actual][2]+normales[vertice_actual][2])
    # Binormal
    glColor3f(1.0,0.0,0.0)
    glVertex3f(vertices[vertice_actual][0],vertices[vertice_actual][1],vertices[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + binormales[vertice_actual][0],vertices[vertice_actual][1]+binormales[vertice_actual][1],vertices[vertice_actual][2]+binormales[vertice_actual][2])

    glEnd()

    # Plano osculador
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_TRIANGLES)
    glColor4f(0.0,1.0,1.0,0.1)

    glVertex3f(vertices[vertice_actual][0], vertices[vertice_actual][1],    vertices[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + tangentes[vertice_actual][0],  vertices[vertice_actual][1] +   tangentes[vertice_actual][1],   vertices[vertice_actual][2] +   tangentes[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + normales[vertice_actual][0],   vertices[vertice_actual][1] +   normales[vertice_actual][1],    vertices[vertice_actual][2] +   normales[vertice_actual][2])

    glVertex3f(vertices[vertice_actual][0] + tangentes[vertice_actual][0],  vertices[vertice_actual][1] +   tangentes[vertice_actual][1],   vertices[vertice_actual][2] +   tangentes[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + normales[vertice_actual][0],   vertices[vertice_actual][1] +   normales[vertice_actual][1],    vertices[vertice_actual][2] +   normales[vertice_actual][2])
    glVertex3f(vertices[vertice_actual][0] + normales[vertice_actual][0] +  tangentes[vertice_actual][0],   vertices[vertice_actual][1] +   normales[vertice_actual][1] +   tangentes[vertice_actual][1], vertices[vertice_actual][2] + normales[vertice_actual][2] + tangentes[vertice_actual][2])

    glEnd()

    if dibujoEvoluta:
        # Evoluta
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0,0.0,1.0)
        for v in evoluta:
            glVertex3f(v[0],v[1],v[2])
        glEnd()

        # Línea que une evoluta y gráfica
        glBegin(GL_LINES)
        glColor3f(0.0,1.0,0.0)

        glVertex3f(vertices[vertice_actual][0],vertices[vertice_actual][1],vertices[vertice_actual][2])
        glVertex3f(evoluta[vertice_actual][0],evoluta[vertice_actual][1],evoluta[vertice_actual][2])

        glEnd()

def ayuda():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, ventana_tam_x, 0.0, ventana_tam_y)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 0.0, 0.0)

    strings_ayuda = ["N y M controlan la animación","E dibuja la evoluta"]

    num_lineas = 0
    print(ventana_tam_x,ventana_tam_y)
    for s in strings_ayuda:
        glWindowPos2i(ventana_tam_x / 2, ventana_tam_y / 2)
        for c in s:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c));
            print(c,end="")
        print()
        num_lineas += 1

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()



# Función de dibujado
def dibujar():
    rotationRate = (time.time() - tStart) * 1.05
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    fijarViewportProyeccion()
    fijarCamara()

    dibujarEjes()

    dibujarObjetos()

    ayuda()

    glutSwapBuffers()

    if show_frames:
        framerate()

# Función de animación del triedro de Frenet
def animar():
    global velocidad, direccion, vertice_animado, vertice_actual

    vertice_animado += velocidad*direccion

    if vertice_animado < 0 or vertice_animado > len(vertices):
        direccion *= -1


    vertice_actual = int(vertice_animado)
    if vertice_actual < 0:
        vertice_actual = 0
    elif vertice_actual >= len(vertices):
        vertice_actual = len(vertices) - 1

    glutPostRedisplay()


# Teclas normales: para cambiar escala y velocidad
def teclaNormal(k, x, y):
    global frustum_factor_escala, vertice_actual, velocidad, camara_angulo_x, camara_angulo_y, dibujoEvoluta

    if k == '+':
        frustum_factor_escala *= 1.05
    elif k == '-':
        frustum_factor_escala /= 1.05
    elif k == b'e':
        dibujoEvoluta = not dibujoEvoluta
    elif k == b'n':
        velocidad -= 0.1
        if velocidad < 0:
            velocidad = 0
    elif k == b'm':
        velocidad += 0.1
        if velocidad > 1.5:
            velocidad = 1.5
    elif k == b'r':
        camara_angulo_x = camara_angulo_y = 0.0
    elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return
    glutPostRedisplay()


# Teclas especiales: para cambiar la cámara
def teclaEspecial(k, x, y):
    global camara_angulo_x, camara_angulo_y

    if k == GLUT_KEY_UP:
        camara_angulo_x += 5.0
    elif k == GLUT_KEY_DOWN:
        camara_angulo_x -= 5.0
    elif k == GLUT_KEY_LEFT:
        camara_angulo_y += 5.0
    elif k == GLUT_KEY_RIGHT:
        camara_angulo_y -= 5.0
    else:
        return
    glutPostRedisplay()


# Nuevo tamaño de ventana
def cambioTamanio(width, height):
    global ventana_tam_x,ventana_tam_y

    ventana_tam_x = width
    ventana_tam_y = height

    fijarViewportProyeccion()
    glutPostRedisplay()

origen = [-1,-1]
def pulsarRaton(boton,estado,x,y):
    da = 5.0
    redisp = False
    global frustum_factor_escala,origen,camara_angulo_x,camara_angulo_y

    if boton == GLUT_LEFT_BUTTON:
        if estado == GLUT_UP:
            origen = [-1,-1]
        else:
            origen = [x,y]
    elif boton == 3: # Rueda arriba aumenta el zoom
        frustum_factor_escala *= 1.05;
        redisp = True
    elif boton == 4: # Rueda abajo disminuye el zoom
        frustum_factor_escala /= 1.05;
        redisp = True
    elif boton == 5: # Llevar la rueda a la izquierda gira la cámara a la izquierda
        camara_angulo_y -= da
        redisp = True
    elif boton == 6: # Llevar la rueda a la derecha gira la cámara a la derecha
        camara_angulo_y += da
        redisp = True

    if redisp:
        glutPostRedisplay();

def moverRaton(x,y):
    global camara_angulo_x,camara_angulo_y, origen

    if origen[0] >= 0 and origen[1] >= 0:
        camara_angulo_x += (y - origen[1])*0.25;
        camara_angulo_y += (x - origen[0])*0.25;

        origen[0] = x;
        origen[1] = y;

        # Redibujar
        glutPostRedisplay();


def inicializar():
    if len(sys.argv) < 7:
        print("No has metido 6 argumentos: tienes",len(sys.argv))
        exit(-1)

    global vertices,evoluta, x_t, y_t, z_t
    t = symbols('t')

    x_t         = sympify(sys.argv[1])
    y_t         = sympify(sys.argv[2])
    z_t         = sympify(sys.argv[3])
    num_puntos  = int(sys.argv[4])
    inicio      = int(sys.argv[5])
    final       = int(sys.argv[6])

    longitud = final - inicio
    incremento = longitud / (num_puntos - 1)

    curva = Matrix([x_t,y_t,z_t])

    # derivada_curva = Matrix([curva[0].diff(t),curva[1].diff(t),curva[2].diff(t)])
    derivada_curva = curva.diff(t)
    derivada2_curva = derivada_curva.diff(t)
    # derivada2_curva = Matrix([derivada_curva[0].diff(t),derivada_curva[1].diff(t),derivada_curva[2].diff(t)])

    T = simplify(derivada_curva.normalized())
    B = simplify(derivada_curva.cross(derivada2_curva).normalized())
    N = simplify(B.cross(T))

    curvatura = simplify((derivada_curva.cross(derivada2_curva).norm()) / (derivada_curva.norm() ** 3))
    print("Tangente: ",T)
    print("\nNormal: ",N)
    print("\nBinormal: ",B)
    print("\nCurvatura: ", curvatura)

    for indice_punto in range(num_puntos):
        t_var = inicio + indice_punto*incremento
        vertices.append([curva[0].subs(t,t_var),curva[1].subs(t,t_var),curva[2].subs(t,t_var)])
        tangentes.append([T[0].subs(t,t_var),T[1].subs(t,t_var),T[2].subs(t,t_var)])
        normales.append([N[0].subs(t,t_var),N[1].subs(t,t_var),N[2].subs(t,t_var)])
        binormales.append([B[0].subs(t,t_var),B[1].subs(t,t_var),B[2].subs(t,t_var)])

        vertice_evoluta = curva.subs(t,t_var) + N.subs(t,t_var)/curvatura.subs(t,t_var)
        # print("curva: ",curva.subs(t,t_var),"+",N.subs(t,t_var),"/",curvatura.subs(t,t_var))
        evoluta.append([vertice_evoluta[0],vertice_evoluta[1],vertice_evoluta[2]])

    # for e in evoluta:
    #     print(e)


    glEnable(GL_NORMALIZE)
    glEnable(GL_MULTISAMPLE_ARB);
    glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
    glColor3f(0.0,0.0,0.0)

def visible(vis):
    if vis == GLUT_VISIBLE:
        glutIdleFunc(animar)
    else:
        glutIdleFunc(None)


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(ventana_tam_x, ventana_tam_y)
    glutCreateWindow("Curvas, triedro de Frenet y evoluta")
    inicializar()

    glutDisplayFunc(dibujar)
    glutReshapeFunc(cambioTamanio)
    glutKeyboardFunc(teclaNormal)
    glutSpecialFunc(teclaEspecial)
    glutMouseFunc(pulsarRaton)
    glutMotionFunc(moverRaton)
    glutVisibilityFunc(visible)

    if "-info" in sys.argv:
        print("GL_RENDERER   = ", glGetString(GL_RENDERER))
        print("GL_VERSION    = ", glGetString(GL_VERSION))
        print("GL_VENDOR     = ", glGetString(GL_VENDOR))
        print("GL_EXTENSIONS = ", glGetString(GL_EXTENSIONS))

    if "-framerate" in sys.argv:
        show_frames = True

    glutMainLoop()
