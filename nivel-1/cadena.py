# coding: utf-8
import pilasengine
from settings import IMG_DIR

pilas = pilasengine.iniciar()


class MM(pilasengine.actores.Actor):
    def iniciar(self):
        self.imagen = IMG_DIR+'/eslabon_small.png'
        self.figura = pilas.fisica.Rectangulo(
        alto=self.imagen.alto(),ancho=self.imagen.ancho(),
        friccion=0,restitucion=0,dinamica=1)
    def actualizar(self):
        pilas.fisica.gravedad_y = -10
        if self.y > -100:
            self.figura.rotacion = 35
        self.x = self.figura.x
        self.y = self.figura.y
        self.figura.escala_de_gravedad=3
        self.rotacion = self.figura.rotacion
        if self.pilas.control.izquierda:
            self.figura.velocidad_x = -2
        if self.pilas.control.derecha:
            self.figura.velocida_x = 2
class MM2(pilasengine.actores.Actor):
    def iniciar(self, x, y, sigue):
        self.x = x
        self.sigue = sigue
        self.y = y
        self.imagen = IMG_DIR+'/eslabon_small.png'
    def actualizar(self):
        self.rotacion = self.sigue.rotacion / 2
        self.x = self.sigue.x - 85
        self.y = max(self.sigue.y - 20, -209)
t = pilas.fisica.Rectangulo(x=0,y=-100,plataforma=1, ancho=450, alto = 20)
pilas.actores.vincular(MM)
pilas.actores.vincular(MM2)
m = MM(pilas)
m2 = MM2(pilas,0 , 0, m)
m3 = MM2(pilas,0,0,m2)
m4 = MM2(pilas, 0,0,m3)
m5 = MM2(pilas, 0,0,m4)

pilas.ejecutar()