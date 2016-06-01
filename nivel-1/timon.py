# coding: utf-8

import pilasengine
from settings import *
pilas = pilasengine.iniciar()
SMALL_IMG_DIR = IMG_DIR + 'mapa-chico-separado/'

timon_grilla = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'timon-grilla.png', 46)

timon = pilas.actores.Animacion(timon_grilla, 1)

pilas.ejecutar()