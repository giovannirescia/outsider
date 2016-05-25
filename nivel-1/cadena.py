# coding: utf-8
import pilasengine
from settings import *

pilas = pilasengine.iniciar(2900, 800)


class MM(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = SMALL_IMG_DIR+'/eslabon.png'
#        self.figura = pilas.fisica.Rectangulo(
#            alto=self.imagen.alto(),ancho=self.imagen.ancho(),
   #     friccion=0,restitucion=0,dinamica=1)

    def actualizar(self):
        pilas.fisica.gravedad_y = -10
   #     if self.y > -100:
           # self.figura.rotacion = 35
  #      self.x = self.figura.x
    #    self.y = self.figura.y

   #     self.rotacion = self.figura.rotacion
        if self.pilas.control.izquierda:
            self.figura.velocidad_x = -2
        if self.pilas.control.derecha:
            self.figura.velocida_x = 2
class MM2(pilasengine.actores.Actor):
    def iniciar(self, x, y, sigue):
        self.x = sigue.x + 10
        self.sigue = sigue
        self.figura = pilas.fisica.Circulo()
        self.y = y
        self.imagen = SMALL_IMG_DIR+'/eslabon.png'
    def actualizar(self):
        self.rotacion = self.sigue.rotacion / 2
        self.figura.x = self.sigue.x + 50
        self.figura.y = max(self.sigue.y - 60, -380) - self.sigue.rotacion/2
        self.x = self.figura.x
        self.y = self.figura.y
#t = pilas.fisica.Rectangulo(x=0,y=-100,plataforma=1, ancho=450, alto = 20)
pilas.actores.vincular(MM)
pilas.actores.vincular(MM2)
m = MM(pilas)
m.aprender('arrastrable')

xs = [m]

for j in range(0, 10):
        xs.append(MM2(pilas,0,0,xs[j]))



pilas.ejecutar()