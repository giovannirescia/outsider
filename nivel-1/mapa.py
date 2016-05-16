# coding: utf-8
import pilasengine
from settings import IMG_DIR

pilas = pilasengine.iniciar(4000, 2160)

mapa = pilas.fondos.Fondo(imagen=IMG_DIR+"/mapa.jpg")
pilas.camara.escala = 1.1
pilas.camara.definir_y(60)
pilas.camara.definir_x(-150)
pilas.ejecutar()