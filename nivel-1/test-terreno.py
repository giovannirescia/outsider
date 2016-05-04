# coding: utf-8
import pilasengine
from ruedolph import Ruedolph
pilas = pilasengine.iniciar(alto=900,ancho=1600)

pilas.actores.vincular(Ruedolph)
ruedolph = Ruedolph(pilas)
c = pilas.fisica.Circulo(y=-300, x=-748, radio=50, amortiguacion=0,restitucion=0,)
ruedolph.imitar(c)
xs = []
#for i in range(0,30):
  #  xs.append(pilas.fisica.Rectangulo(ancho=200,alto=2, y=-190-20*i, x=500-150*i,
    #    plataforma=1, dinamica=False,amortiguacion=1))
for i in range(-30,9):
    xs.append(pilas.fisica.Rectangulo(ancho=40,dinamica=0,plataforma=1,amortiguacion=1,
    x=i*25-150,y=i*5-290))
for j in range(1,40):
    xs.append(pilas.fisica.Rectangulo(ancho=40,dinamica=0,plataforma=1,amortiguacion=1,
    x=j*25,y=j*-5-245))
pilas.fisica.definir_gravedad_y(-100)

pilas.ejecutar()
