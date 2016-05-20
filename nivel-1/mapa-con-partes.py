# coding: utf-8
import pilasengine
from settings  import IMG_DIR
from movimientos import *
import math
import pickle
# original (small) = 2000, 1080
# debug = 1000, 500
pilas = pilasengine.iniciar(2000, 1080)

SMALL_IMG_DIR = IMG_DIR + '/mapa-chico-separado/'

mapa = pilas.fondos.Fondo(imagen=
                SMALL_IMG_DIR+"fondo_small.jpg")

#pilas.camara.y = 340
#pilas.camara.escala = 2



#############################

########### Actores #############

#############################


class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = IMG_DIR +  '/estaticas/ruedolph_concept_art_small2.png'
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(-800, 430, 50,
            friccion=0, restitucion=0, dinamica=1)
        self.figura_encaje = pilas.fisica.Circulo(self.x, self.y, 20,
            friccion=0, restitucion=0, dinamica=0, sensor=1)
        self.imantado = False
        self.se_puede_mover = True
        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5,
            sensor=True, dinamica=False, restitucion=0, amortiguacion=0)

    def actualizar(self):
        velocidad = 10
        salto = 120
        pilas.fisica.gravedad_y = -10
        self.x = self.figura.x
        self.y = self.figura.y
        self.figura_encaje.x = self.x
        self.figura_encaje.y = self.y

        if self.pilas.control.derecha and self.se_puede_mover:
            self.figura.velocidad_x = velocidad
            self.rotacion -= velocidad

        elif self.pilas.control.izquierda and self.se_puede_mover:
            self.figura.velocidad_x = -velocidad
            self.rotacion += velocidad

        else:
            self.figura.velocidad_x = 0

        if self.pilas.control.boton and self.se_puede_mover:
            if any(isinstance(x, Mi_Circulo) for x in self.figura_encaje.figuras_en_contacto):
                global en_colision
                en_colision = True
                pilas.fisica.gravedad_y = 0
                self.figura.velocidad_x = 0
                self.figura.velocidad_y = 0

        if self.esta_pisando_el_suelo():
            if self.pilas.control.arriba and  not int(self.figura.velocidad_y) and not pilas.control.boton:
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 53

    def esta_pisando_el_suelo(self):
        return any(isinstance(x, pilasengine.fisica.rectangulo.Rectangulo) for x in self.sensor_pies.figuras_en_contacto)


class Elementos(pilasengine.actores.Actor):
    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y

class RuedaGenerica(pilasengine.actores.Actor):
    def iniciar(self, x, y):
        self.x = x
        self.y = y
        self.garra = None
        self.imagen = IMG_DIR + '/metal_block.png'
    def actualizar(self):
        if self.garra is not None:
            self.x, self.y = self.garra.extremo
    def poner_garra(self, g):
        self.garra = g

class Base(pilasengine.actores.Actor):
    def iniciar(self,x,y, parte):
        self.x = x
        self.y = y
        self.imagen = parte

class Brazo(pilasengine.actores.Actor):
    def iniciar(self,parte, base_param):
        self.imagen = parte
        self.base_param = base_param
        self.rotacion = -60
        self.rotar = 0
    def actualizar(self):
        self.x = self.base_param.x + 12
        self.y = self.base_param.y + 3
        if self.rotar > 0:
            self.rotacion -=1
            self.rotar -=1
        if self.rotar < 0:
            self.rotacion +=1
            self.rotar +=1
    def ponete_a_rotar(self, val):
        self.rotar = val

    
class Garra(pilasengine.actores.Actor):
    def iniciar(self,parte, brazo):
        self.imagen = parte
        self.brazo = brazo
        self.rotacion = 90
        self.rotar = 0
        self.extremo = (self.x, self.y) 
    def actualizar(self):
        self.x, self.y = get_coord(self.brazo)
        self.extremo = get_coord2(self)
        if self.rotar > 0:
            self.rotacion -=1
            self.rotar -=1
        if self.rotar < 0:
            self.rotacion +=1
            self.rotar +=1
    def ponete_a_rotar(self, val):
        self.rotar = val


pilas.actores.vincular(Ruedolph)
pilas.actores.vincular(Elementos)
pilas.actores.vincular(Brazo)
pilas.actores.vincular(Garra)
pilas.actores.vincular(Base)
pilas.actores.vincular(RuedaGenerica)
        
#############################

####### Elementos del Escenario ######

#############################

# Elementos de la cinta: tubo, horno, plancha, pantalla, scanner

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


base = Base(pilas,95,426,SMALL_IMG_DIR + 'brazo3.png')   
brazo = Brazo(pilas,parte=SMALL_IMG_DIR + 'brazo2.png', base_param=base)
garra = Garra(pilas,parte=SMALL_IMG_DIR + 'brazo1.png', brazo=brazo)

garra.definir_centro((30,0))
brazo.definir_centro((22,0))

garra.rotacion = 12
base.definir_centro((25,base.alto-20))

base.aprender('arrastrable')

#############################

####### Funciones Auxiliares #########

#############################
# Generamos un rueda generica: dos al comienzo, despues
# viene ruedolph y despues generamos sin parar
def generar_rueda():
    rueda = RuedaGenerica(pilas,-800,430)
    rueda.z = 1
    rueda.escala = 0.7
    return rueda

def generar_ruedolph():
    rueda = RuedaGenerica(pilas,-800,430)
    rueda.z = 1
    return rueda

# Vinculamos la garra a la rueda
def agarrar(r, g):
    r.poner_garra(g)

# Giramos el elemento g, y grados
# si y es positivo, gira en sentido horario    
def gira(g, y):
    g.ponete_a_rotar(y)


def generar_texto(text, x, y):
    t = pilas.actores.Texto(text, magnitud=27,x=x,y=y)
    t.color = 'rojo'
    t.transparencia = 100
    return t


def subir_diagonal(g):
    pilas.utils.interpolar(g, 'x', 210, 3.5)
    pilas.utils.interpolar(g, 'y', 270, 3.5)

def llevar(b, x, t):
    pilas.utils.interpolar(b,'x',x,t)

def get_coord(pt):
    return pt.x + math.sin(math.radians(pt.rotacion))*pt.alto,\
        pt.y - math.cos(math.radians(pt.rotacion))*pt.alto

    
def get_coord2(pt):
    return pt.x + math.sin(math.radians(pt.rotacion))*pt.alto,\
        pt.y - math.cos(math.radians(pt.rotacion))*pt.alto
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
    

# generamos a ruedolph
def genesis():
    m = generar_rueda()
    texto_0 = generar_texto('PUTO\nEL QUE\nLEE', 443, 315)
    # Tubo a la cinta
    pilas.tareas.agregar(1, mueve_y, m, 285)
    # cinta al horno
    pilas.tareas.agregar(3, mueve_x, m, 275, )
    # horno a plancha
    pilas.tareas.agregar(8, mueve_x, m, 310)
    pilas.tareas.agregar(8, cambiar_imagen, m, IMG_DIR + '/liquid_metal.png')

   # plancha a subida
    pilas.tareas.agregar(11, mueve_y, plancha,175 )
    pilas.tareas.agregar(14, mueve_y_arriba, plancha,-175, m )
    pilas.tareas.agregar(14, cambiar_imagen, m,\
         IMG_DIR + '/estaticas/ruedolph_concept_art_small2.png')
    pilas.tareas.agregar(15, mueve_x, m, 170,)
    # subida a pantalla
    

    pilas.tareas.agregar(16.3, subir_diagonal, m,)
    # scanner
    pilas.tareas.agregar(20, escanear, laser)
    pilas.tareas.agregar(23.5, aparece_texto, texto_0)
    pilas.tareas.agregar(25.5, gira, brazo, -65)
    pilas.tareas.agregar(25.5, gira, garra, -45)
    pilas.tareas.agregar(28, agarrar, m, garra)
    pilas.tareas.agregar(28.3, llevar, base,-970,4)
    pilas.tareas.agregar(32, gira, garra,57 )
    pilas.tareas.agregar(33.9, agarrar,m , None)
    pilas.tareas.agregar(34, mueve_y, m, 340)
    pilas.tareas.agregar(35.5, gira, garra, -57+45)
    pilas.tareas.agregar(35.5, gira, brazo, 65)
    pilas.tareas.agregar(36, llevar, base, 95, 4)
    pilas.tareas.agregar(36, eliminar, [m, texto_0])


# Accion general que va a crear bloques de metal, derrertirlos
# y crear una rueda dentada a partir de un molde
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
    pilas.tareas.agregar(8, mueve_x, m, 310)
    pilas.tareas.agregar(8, cambiar_imagen, m, IMG_DIR + '/liquid_metal.png')

   # plancha a subida
    pilas.tareas.agregar(11, mueve_y, plancha,175 )
    pilas.tareas.agregar(14, mueve_y_arriba, plancha,-175, m )
    pilas.tareas.agregar(14.5, cambiar_imagen, m, IMG_DIR + '/ruedolph_small.png')
    pilas.tareas.agregar(15, mueve_x, m, 170,)
    # subida a pantalla
    

    pilas.tareas.agregar(16.3, subir_diagonal, m,)
    # scanner
    pilas.tareas.agregar(20, escanear, laser)
   # pilas.tareas.agregar(22, desaparecer, m)
    # pilas.tareas.agregar(1, generar_texto, 'COMELA', 443, 355)
    # pilas.tareas.agregar(23.5, generar_texto, 'JONATHAN', 443, 311)
    # pilas.tareas.agregar(23.5, generar_texto, 'BLOW', 443, 265)
    pilas.tareas.agregar(23.5, aparece_texto, texto_0)
    pilas.tareas.agregar(23.5, aparece_texto, texto_1)
    pilas.tareas.agregar(23.5, aparece_texto, texto_2)
    pilas.tareas.agregar(25.5, gira, brazo, -65)
    pilas.tareas.agregar(25.5, gira, garra, -45)
    pilas.tareas.agregar(28, agarrar, m, garra)
    pilas.tareas.agregar(28, gira, brazo, 130)
    pilas.tareas.agregar(29.5, gira, garra, 200)
    pilas.tareas.agregar(34, eliminar, [m, texto_0, texto_1, texto_2])
    pilas.tareas.agregar(34.5, gira, garra, -200 + 45)
    pilas.tareas.agregar(37.5, gira, brazo, -130 + 65)
    
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
    pilas.tareas.agregar(38, general)
    pilas.tareas.agregar(52, general)

pilas.tareas.agregar(1, general)
pilas.tareas.agregar(38, general)
pilas.tareas.agregar(75, genesis)
# ruedolph
#pilas.tareas.agregar(52, general)
#pilas.tareas.siempre(79, bar)
pilas.ejecutar()