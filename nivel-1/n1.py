#!/usr/bin/env python
# coding: utf-8

import pilasengine
#from protagonista import *
from settings import IMG_DIR

pilas = pilasengine.iniciar(ancho=1600, alto=900)
class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = IMG_DIR + "/ruedolph_small.png"

        self.figura = pilas.fisica.Circulo(self.x, self.y, 50,
            friccion=0, restitucion=0,dinamica=1)

        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3

        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5, sensor=True, dinamica=False,restitucion=0,amortiguacion=0)

    def actualizar(self):
        velocidad = 10
        salto = 125
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
            self.decir('putooooo')

        if self.esta_pisando_el_suelo():
            if self.pilas.control.arriba and not int(self.figura.velocidad_y):
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 53

    def esta_pisando_el_suelo(self):
        return len(self.sensor_pies.figuras_en_contacto) > 0

cinta1 = pilas.fisica.Rectangulo(plataforma=1,x=-345,y=-85,alto=35,ancho=870,amortiguacion=0,restitucion=0)
fondo = pilas.fondos.Fondo(imagen=IMG_DIR+'/N1E1.png')
fondo.escala = 0.46

pilas.actores.vincular(Ruedolph)
ruedolph = Ruedolph(pilas)

pilas.ejecutar()
