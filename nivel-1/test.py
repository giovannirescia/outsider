# coding: utf-8
import pilasengine

pilas = pilasengine.iniciar()

mono = pilas.actores.Mono()

# Algunas transformaciones:
# (Pulsá el botón derecho del
#  mouse sobre alguna de las
#  sentencias)

mono.x = 0
mono.y = 0
mono.escala = 1.0
mono.rotacion = 0

pilas.ejecutar()
fondo = pilas.fondos.Fondo()
fondo.imagen = pilas.imagenes.cargar("/home/giovanni/proyectos/outsider/nivel-1/imagenes/escenario.jpg")
mono.aprender('moverseconelteclado',con_rotacion=1)