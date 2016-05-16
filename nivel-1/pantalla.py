# coding: utf-8

import pilasengine
from settings import IMG_DIR

pilas = pilasengine.iniciar()

grilla = pilas.imagenes.cargar_grilla(IMG_DIR+"/grillaPEQUE.png", 23)
grilla_animacion = pilas.actores.Animacion(grilla, True)

pilas.ejecutar()