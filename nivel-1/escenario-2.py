#coding: utf-8

from __future__ import division
import pilasengine
from settings  import IMG_DIR
from movimientos import *
from circulo_personalizado import Mi_Circulo
import math
import pickle
from coordenadas import *

# GLOBAL
en_colision = False

pilas = pilasengine.iniciar(2000, 1080, pantalla_completa=False)

SMALL_IMG_DIR = IMG_DIR + 'mapa-chico-separado/'
cam = pilas.camara
class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = SMALL_IMG_DIR + 'ruedolph.png'
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(-780,-389, 50,
            friccion=0, restitucion=0, dinamica=1)
        self.figura_encaje = pilas.fisica.Circulo(self.x, self.y, 20,
            friccion=0, restitucion=0, dinamica=0, sensor=1)
        self.imantado = False
        self.se_puede_mover = False
        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5,
            sensor=True, dinamica=False, restitucion=0, amortiguacion=0)
        self.salto = 120
    def actualizar(self):
        velocidad = 10
        salto = self.salto
        pilas.fisica.gravedad_y = -10
        # La camara sigue a Ruedolph
        if self.x >=0:
            if self.x + 1000.0/(cam.escala)<=1000:
                cam.x = self.x
            else:
                cam.x = 1000 - 1000.0/(cam.escala)
        else:
            if self.x - 1000.0/(cam.escala) > -1000:
                cam.x = self.x
            else:
                cam.x = -1000 + 1000.0/(cam.escala)
        if self.y >=0:
            if self.y + 540.0/(cam.escala) <= 540:
                cam.y = self.y
            else:
                cam.y = 540 - 540.0/(cam.escala)
        else:
            if self.y - 540.0/(cam.escala) > -540:
                cam.y = self.y
            else:
                cam.y = -540 + 540.0/(cam.escala)
        
        self.x = self.figura.x
        self.y = self.figura.y
        self.figura_encaje.x = self.x
        self.figura_encaje.y = self.y

        if self.pilas.control.derecha and self.se_puede_mover:
            self.figura.velocidad_x = velocidad
            self.rotacion -= velocidad

        elif self.pilas.control.izquierda and self.se_puede_mover:
            self.figura.velocidad_x = -velocidad
            self.rotacion += velocidad

        else:
            self.figura.velocidad_x = 0

        if self.pilas.control.boton and self.se_puede_mover:
            if any(isinstance(x, Mi_Circulo) for x in self.figura_encaje.figuras_en_contacto):
                global en_colision
                en_colision = True
                pilas.fisica.gravedad_y = 0
                self.figura.velocidad_x = 0
                self.figura.velocidad_y = 0

        if self.esta_pisando_el_suelo():
            if self.pilas.control.arriba and  not int(self.figura.velocidad_y) and not pilas.control.boton and self.se_puede_mover:
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 53

    def esta_pisando_el_suelo(self):
        return any(isinstance(x, pilasengine.fisica.rectangulo.Rectangulo) for x in self.sensor_pies.figuras_en_contacto)
    
    def movete(self):
        self.se_puede_mover = True
        return False

    def imantate(self):
        self.imantado = True


class Pendorcho(pilasengine.actores.Actor):
    def iniciar(self, x, y, img,centro=(110,80)):
        self.imagen = img
        self.y = y
        self.x = x
        self.centro = centro
        self.radio_de_colision = 10
        self.mc = Mi_Circulo(fisica=pilas.fisica, pilas=pilas, x=x, y=y,
            radio=self.radio_de_colision, sensor=True, dinamica=False)
        self.piso = pilas.fisica.Rectangulo(x, y - 50, 30, 5,
                sensor=True, dinamica=False, restitucion=0, amortiguacion=0)
    def actualizar(self):
        self.mc.x, self.mc.y, self.piso.x, self.piso.y = self.x, self.y, self.x, self.y-50

class Escenario2(pilasengine.escenas.Escena):
    def iniciar(self):
        self.fondo = pilas.fondos.Fondo(imagen=
                SMALL_IMG_DIR+"escenario_2_small.png")
    def ejecutar(self):
        pass
pilas.actores.vincular(Ruedolph)
pilas.actores.vincular(Pendorcho)
pilas.escenas.vincular(Escenario2)

#Eslabon principal
class EslabonPrincipal(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = SMALL_IMG_DIR+'/eslabon.png'
        self.escala = 0.4
        self.x = -300
        self.z = 2
        self.y = -400
        self.sigue = None
    def actualizar(self):
        if self.sigue is not None:
                self.x = self.sigue.x
                self.y = self.sigue.y

#Eslabones secundarios
class EslabonSecundario(pilasengine.actores.Actor):
    def iniciar(self, x, y, sigue):
        self.x = sigue.x + 10
        self.z = 2
        self.sigue = sigue
        self.escala = 0.4
        self.imagen = SMALL_IMG_DIR+'/eslabon.png'
    def actualizar(self):
        self.rotacion = self.sigue.rotacion / 2
        self.x = self.sigue.x + 25
        if self.y > -400:
            self.x = self.sigue.x
        self.y = max(self.sigue.y - 30, -400) - self.sigue.rotacion/2
#t = pilas.fisica.Rectangulo(x=0,y=-100,plataforma=1, ancho=450, alto = 20)
pilas.actores.vincular(EslabonPrincipal)
pilas.actores.vincular(EslabonSecundario)


################
# Colisiones
##################

def seguir_rueda(rueda, eslabon):
    if rueda.imantado:
        eslabon.sigue = rueda

def imantacion(x, y):
    x.imantate()


def agarra_metal_rojo(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolph_fase_1.png'

def agarra_metal_azul(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolph_fase_2.png'

def verificar(evento):
    global en_colision
    if en_colision and pilas.control.boton:
        en_colision = False
        aux = None
        xs = ruedolph.figura.figuras_en_contacto
        for elem in xs:
            if isinstance(elem, Mi_Circulo):
                if ruedolph.figura != elem:
                    aux = elem
        if aux is not None:
            ruedolph.figura.x = aux.x
            ruedolph.figura.y = aux.y
            ruedolph.figura.velocidad_y = 0
            pilas.fisica.gravedad_y = 0


def encajar(Ruedolph, pendorchos):
    global en_colision
    en_colision = True


# El parametro indica si es la primera vez que se ingresa al escenario
def cambiar_a_escenario_2(param=False):
    e2 = pilas.escenas.Escenario2()
    rueda = Ruedolph(pilas)
    rueda.movete()
    colgables = map(lambda attr: Pendorcho(pilas,x=attr[0],y=attr[1],centro=attr[2],img=attr[3]), coor_esc_2)
    iman = pilas.actores.Actor(x=550, y=-280)
    iman.transparencia = 100
    iman.radio_de_colision = 100
    piso_e2 = pilas.fisica.Rectangulo(y=-450,ancho=2000,\
            restitucion = 0, friccion =0, amortiguacion=0, plataforma=1)
    pared_e2 = pilas.fisica.Rectangulo(x=-870,y=0,ancho=20,\
            alto=1080, restitucion = 0, friccion =0, amortiguacion=0, plataforma=1)
    metal_rojo = pilas.actores.Actor(x=236, y=426)
    metal_rojo.radio_de_colision = 30
    metal_rojo.imagen = SMALL_IMG_DIR + 'metal_rojo_1.png'
    metal_azul = pilas.actores.Actor(x=-623, y=200)
    metal_azul.radio_de_colision = 30
    metal_azul.imagen = SMALL_IMG_DIR + 'metal_azul_3.png'

    # generamos la cadena
    eslabon = EslabonPrincipal(pilas)
    eslabon.aprender('arrastrable')
    xs = [eslabon]
    for j in range(0, 19):
        xs.append(EslabonSecundario(pilas,0,0,xs[j]))
    pilas.colisiones.agregar(rueda, iman, imantacion)
    pilas.colisiones.agregar(rueda, metal_rojo, agarra_metal_rojo)
    pilas.colisiones.agregar(rueda, metal_azul, agarra_metal_azul)
    pilas.colisiones.agregar(rueda, eslabon, seguir_rueda)
 
    return rueda

ruedolph=cambiar_a_escenario_2()
pilas.eventos.pulsa_tecla.conectar(verificar)
pilas.ejecutar()