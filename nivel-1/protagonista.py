# coding: utf-8
import pilasengine
import Box2D as box2d
from pilasengine.fisica.figura import Figura
from pilasengine import utils
from pilasengine import fisica
from settings import IMG_DIR
#pilas = pilasengine.iniciar(ancho=1600, alto=900)
#f = pilas.fisica.Rectangulo(plataforma=1,x=-345,y=-85,alto=35,ancho=870,amortiguacion=0,restitucion=0)

# Variable global
en_colision = False

pilas = pilasengine.iniciar()

class MC(object):
    def __init__(self):
        self.es_eje = True
        self.eje = pilas.fisica.Circulo(y=-200,sensor=1, dinamica=0)
# Ruedolph_Circle
class RC(pilasengine.fisica.circulo.Circulo):
    def __init__(self, fisica=fisica, pilas=pilas, x=0, y=0, radio=20, dinamica=True, densidad=1.0, restitucion=0.56, friccion=10.5, amortiguacion=0.1, sin_rotacion=False, sensor=False):
        super(RC, self).__init__(fisica, pilas, x, y, radio, dinamica, densidad, restitucion, friccion, amortiguacion, sin_rotacion,sensor)

class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = IMG_DIR + "/ruedolph_small.png"
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(self.x, self.y, 50,
            friccion=0, restitucion=0,dinamica=1)
        self.imantado = False
        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3

        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5, sensor=True, dinamica=False,restitucion=0,amortiguacion=0)

    def actualizar(self):
        velocidad = 10
        salto = 125
        pilas.fisica.gravedad_y = -10
        self.x = self.figura.x
        self.y = self.figura.y
        
        if self.pilas.control.derecha:
            self.figura.velocidad_x = velocidad
            self.rotacion -= velocidad

        elif self.pilas.control.izquierda:
            self.figura.velocidad_x = -velocidad
            self.rotacion += velocidad

        else:
            self.figura.velocidad_x = 0

        if self.pilas.control.boton:
            pilas.fisica.gravedad_y = 0
            self.figura.velocidad_x = 0
            self.figura.velocidad_y = 0


        if self.esta_pisando_el_suelo():
            if self.pilas.control.arriba and not int(self.figura.velocidad_y) and not pilas.control.boton:
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 53

    def esta_pisando_el_suelo(self):
        return len(self.sensor_pies.figuras_en_contacto) > 0


class Pendorcho(pilasengine.actores.Actor):
    def iniciar(self, x, y):
        self.imagen = IMG_DIR + '/tornillo.png'
        self.y = y
        self.x = x
        self.escala = 0.1
        self.radio_de_colision = 20
        self.piso = pilas.fisica.Rectangulo(x, y - 50, 30, 5, sensor=True, dinamica=False,restitucion=0,amortiguacion=0)

pilas.actores.vincular(Pendorcho)
pilas.actores.vincular(Ruedolph)
r = Ruedolph(pilas)
t1 = Pendorcho(pilas, 0, -128)
t2 = Pendorcho(pilas, 150, -90)
#f = pilas.fondos.Fondo(imagen=IMG_DIR+'/nivel-1/N1E1.png')
#f.escala = 0.46

pendorchos = pilas.actores.Grupo()
pendorchos.agregar(t1)
pendorchos.agregar(t2)

def verificar(evento):
    global en_colision
    if en_colision and pilas.control.boton:
        en_colision = False
        r.figura.x = Pendorcho.get_x()
        r.figura.y = Pendorcho.get_y()
        pilas.fisica.gravedad_y = 0
        r.figura.velocidad_y = 0
        
def encajar(r, pendorchos):
    global en_colision
    en_colision = True


pilas.eventos.pulsa_tecla.conectar(verificar)
pilas.colisiones.agregar(r, pendorchos, encajar)




pilas.ejecutar()
