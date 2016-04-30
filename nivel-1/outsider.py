# coding: utf-8
import pilasengine
from settings import IMG_DIR

pilas = pilasengine.iniciar(alto=900,ancho=1600)


# Algunas transformaciones:
# (Pulsá el botón derecho del
#  mouse sobre alguna de las
#  sentencias)

imagen = pilas.imagenes.cargar(IMG_DIR + '/nivel-1/N1E1.png')
imagen_r = pilas.imagenes.cargar(IMG_DIR + '/nivel-1/ruedolph_small.png')

class Ruedolph(pilasengine.actores.Actor):
    def iniciar(self):
            self.imagen = imagen_r
            self.radio_de_colision = 50
            
    def actualizar(self):
        aux = 4
        if self.pilas.control.izquierda:
            self.x -= aux
            self.rotacion +=aux
        elif self.pilas.control.derecha:
            self.x += aux
            self.rotacion -=aux

pilas.actores.vincular(Ruedolph)
ruedolph = Ruedolph(pilas)
c = pilas.fisica.Circulo(radio=50, amortiguacion=0,restitucion=0)
ruedolph.imitar(c)
fondo = pilas.fondos.Fondo()
fondo.imagen = imagen
fondo.escala = .46
pilas.ejecutar()
