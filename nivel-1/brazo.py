import pilasengine
from settings import *
import math
pilas = pilasengine.iniciar()


class Base(pilasengine.actores.Actor):
    def iniciar(self,x,y, parte):
        self.x = x
        self.y = y
        self.imagen = parte

class Brazo(pilasengine.actores.Actor):
    def iniciar(self,parte, base_param):
        self.imagen = parte
        self.x = base_param.x + 12
        self.y = base_param.y + 11

class Garra(pilasengine.actores.Actor):
    def iniciar(self,parte, brazo):
        self.imagen = parte
        self.brazo = brazo
    def actualizar(self):
        self.x, self.y = get_coord(self.brazo)


def get_coord(pt):
    return pt.x -11+ math.sin(math.radians(pt.rotacion))*pt.alto, pt.y +20- math.cos(math.radians(pt.rotacion))*pt.alto

pilas.actores.vincular(Brazo)
pilas.actores.vincular(Garra)
pilas.actores.vincular(Base)


base = Base(pilas,151,122,SMALL_IMG_DIR + 'brazo3.png')   
brazo = Brazo(pilas,parte=SMALL_IMG_DIR + 'brazo2.png', base_param=base)
garra = Garra(pilas,parte=SMALL_IMG_DIR + 'brazo1.png', brazo=brazo)

brazo.aprender('arrastrable')

garra.definir_centro((30,0))
brazo.definir_centro((22,0))
base.definir_centro((25,base.alto-20))

pilas.ejecutar()