# coding: utf-8
import pilasengine
from settings  import IMG_DIR
from movimientos import *

# original (small) = 2000, 1080
# debug = 1000, 500
pilas = pilasengine.iniciar(2000, 1080)

SMALL_IMG_DIR = IMG_DIR + '/mapa-chico-separado/'

mapa = pilas.fondos.Fondo(imagen=
                SMALL_IMG_DIR+"fondo_small.jpg")

        
#############################

####### Elementos del Escenario ######

#############################

# Elementos de la cinta: tubo, horno, plancha, pantalla, scanner
class Elementos(pilasengine.actores.Actor):
    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y

pilas.actores.vincular(Elementos)

tubo = Elementos(pilas, -800, 415)
tubo.imagen = SMALL_IMG_DIR+'tubo.png'

horno = Elementos(pilas, -520, 170)
horno.imagen = SMALL_IMG_DIR+'horno.png'

plancha = Elementos(pilas, -200, 450)
plancha.imagen = SMALL_IMG_DIR+'plancha.png'

scanner = Elementos(pilas, 295, 450)
scanner.imagen = SMALL_IMG_DIR+'scanner.png'

laser = Elementos(pilas, 50, 145)
laser.imagen = SMALL_IMG_DIR+'laser2.png'
laser.transparencia = 100

pantalla = Elementos(pilas, 450, 350)
pantalla.imagen = SMALL_IMG_DIR+'pantalla.png'

grilla = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR+"grilla_small.png", 23)
grilla_animacion = pilas.actores.Animacion(grilla, True)
grilla_animacion.x = pantalla.x - 5
grilla_animacion.y = pantalla.y - 33
grilla_animacion.transparencia = 55

grilla_cinta = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR+'animacion_cinta.png',3)
grilla_animacion_cinta = pilas.actores.Animacion(grilla_cinta, True)
grilla_animacion_cinta.y = 200
grilla_animacion_cinta.x = -360
grilla_animacion_cinta.z = 2

brazo1 = Elementos(pilas,183,323)
brazo1.imagen = SMALL_IMG_DIR + 'brazo1.png'
brazo2 = Elementos(pilas,163,413)
brazo2.rotacion = 50
brazo2.imagen = SMALL_IMG_DIR + 'brazo2.png'
brazo3 = Elementos(pilas, 150, 496)
brazo3.imagen = SMALL_IMG_DIR + 'brazo3.png'
#############################

########### Actores #############

#############################


class RuedaGenerica(pilasengine.actores.Actor):
    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.imagen = IMG_DIR + '/metal_block.png'

pilas.actores.vincular(RuedaGenerica)

def generar_rueda():
    rueda = RuedaGenerica(pilas,-800,430)
    rueda.escala = 0.7
    rueda.z = 1
    return rueda


def generar_texto(text, x, y):
    t = pilas.actores.Texto(text, magnitud=27,x=x,y=y)
    t.color = 'rojo'
    t.transparencia = 100
    return t
 
def subir_diagonal(g):
    pilas.utils.interpolar(g, 'x', 210, 3.5)
    pilas.utils.interpolar(g, 'y', 270, 3.5)

#############################
########### Movimientos ##########
#############################

pilas.comportamientos.vincular(Desaparecer)
pilas.comportamientos.vincular(Mueve_x)
pilas.comportamientos.vincular(Mueve_y)
pilas.comportamientos.vincular(Mueve_y_arriba)
pilas.comportamientos.vincular(Eliminar)
pilas.comportamientos.vincular(Escanear)
pilas.comportamientos.vincular(ApareceTexto)
    


def general():
    m = generar_rueda()
    texto_0 = generar_texto('COMELA', 443, 355)
    texto_1 = generar_texto('JONATHAN', 443, 311)
    texto_2 = generar_texto('BLOW', 443, 265)
    # Tubo a la cinta
    pilas.tareas.agregar(1, mueve_y, m, 285)
    # cinta al horno
    pilas.tareas.agregar(3, mueve_x, m, 275, )
    # horno a plancha
    pilas.tareas.agregar(8, mueve_x, m, 310,IMG_DIR+'/liquid_metal.png' )
    # plancha a subida
    pilas.tareas.agregar(11, mueve_y, plancha,175 )
    pilas.tareas.agregar(14, mueve_y_arriba, plancha,-175, m )
    pilas.tareas.agregar(15, mueve_x, m, 170,)
    # subida a pantalla
    pilas.tareas.agregar(16.3, subir_diagonal, m,)
    # scanner
    pilas.tareas.agregar(20, escanear, laser)
    pilas.tareas.agregar(22, desaparecer, m)
    # pilas.tareas.agregar(1, generar_texto, 'COMELA', 443, 355)
    # pilas.tareas.agregar(23.5, generar_texto, 'JONATHAN', 443, 311)
    # pilas.tareas.agregar(23.5, generar_texto, 'BLOW', 443, 265)
    pilas.tareas.agregar(23.5, aparece_texto, texto_0)
    pilas.tareas.agregar(23.5, aparece_texto, texto_1)
    pilas.tareas.agregar(23.5, aparece_texto, texto_2)
    pilas.tareas.agregar(27, eliminar, [m, texto_0,texto_1,texto_2])
    
emisor = pilas.actores.Emisor(horno.x, horno.y+100)
emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
emisor.constante = True
emisor.frecuencia_creacion = 0.4
emisor.x_max =  100
emisor.x_min = - 100
emisor.dy_max = 30
emisor.composicion = "blanco"
emisor.duracion = 4

def bar():
    pilas.tareas.agregar(1, general)
    pilas.tareas.agregar(28, general)
    pilas.tareas.agregar(52, general)

pilas.tareas.agregar(1, general)
pilas.tareas.agregar(28, general)
# ruedolph
pilas.tareas.agregar(52, general)
pilas.tareas.siempre(79, bar)
pilas.ejecutar()