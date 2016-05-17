# coding: utf-8
import pilasengine
from settings import IMG_DIR
from movimientos import *
pilas = pilasengine.iniciar(4000, 2160)

mapa = pilas.fondos.Fondo(imagen=IMG_DIR+"/mapa.jpg")
pilas.camara.escala = 1.1
pilas.camara.definir_y(60)
pilas.camara.definir_x(-150)


class RuedaGenerica(pilasengine.actores.Actor):
    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = IMG_DIR + '/metal_block.png'

pilas.actores.vincular(RuedaGenerica)
def generar_rueda():
    b = RuedaGenerica(pilas,-1550,530)
    b.escala = 1.5
    return b

pilas.comportamientos.vincular(Desaparecer)
pilas.comportamientos.vincular(Mueve_x)
pilas.comportamientos.vincular(Mueve_y)
pilas.comportamientos.vincular(Eliminar)

def mueve_x(g, stamina, img=''):
    g.hacer("Mueve_x", stamina, img)

def mueve_x2(g):
    g.hacer("Mueve_x2")

def mueve_y(g, stamina):
    g.hacer("Mueve_y",stamina)

def eliminar(g):
    g.hacer("Eliminar")

def desaparecer(g):
    g.hacer("Desaparecer")

def general():
    m = generar_rueda()
    pilas.tareas.agregar(1, mueve_y, m, 240)
    pilas.tareas.agregar(2, mueve_x, m, 450, )
    pilas.tareas.agregar(6, mueve_x, m, 700,IMG_DIR+'/liquid_metal.png' )
    pilas.tareas.agregar(12, mueve_x, m, 300,IMG_DIR+'/ruedolph_small.png')
    pilas.tareas.agregar(15, mueve_y, m, 220)
    pilas.tareas.agregar(15, mueve_x, m, 480)
    pilas.tareas.agregar(18, desaparecer, m)
    pilas.tareas.agregar(22, eliminar, m)

pilas.tareas.agregar(1,general)
pilas.tareas.agregar(17,general)
pilas.ejecutar()
