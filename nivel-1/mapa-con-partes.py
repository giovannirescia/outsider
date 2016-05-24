# coding: utf-8
import pilasengine
from settings  import IMG_DIR
from movimientos import *
from circulo_personalizado import Mi_Circulo
import math
import pickle
# original (small) = 2000, 1080
# debug = 1000, 500
# GLOBAL
en_colision = False
# GLOBAL
R = None
pilas = pilasengine.iniciar(2000, 1080, pantalla_completa=False)

SMALL_IMG_DIR = IMG_DIR + '/mapa-chico-separado/'

mapa = pilas.fondos.Fondo(imagen=
                SMALL_IMG_DIR+"fondo_small.jpg")


####################################################

##################### Actores ######################

####################################################


class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = SMALL_IMG_DIR + 'ruedolph.png'
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(-900,-389, 50,
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
        salto = 150
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
    def iniciar(self, x, y, param):
        self.x = x
        self.y = y
        self.garra = None
        self.imagen = param
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
            self.rotacion -=5
            self.rotar -=5
        if self.rotar < 0:
            self.rotacion +=5
            self.rotar +=5
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
            self.rotacion -=5
            self.rotar -=5
        if self.rotar < 0:
            self.rotacion +=5
            self.rotar +=5
    def ponete_a_rotar(self, val):
        self.rotar = val


pilas.actores.vincular(Ruedolph)
pilas.actores.vincular(Elementos)
pilas.actores.vincular(Brazo)
pilas.actores.vincular(Garra)
pilas.actores.vincular(Base)
pilas.actores.vincular(RuedaGenerica)



################################################################

################## Elementos del Escenario #####################

#################################################################

# Elementos de la cinta: tubo, horno, plancha, pantalla, scanner

tubo = Elementos(pilas, -800, 415)
tubo.imagen = SMALL_IMG_DIR+'tubo.png'

horno = Elementos(pilas, -520, 170)
horno.imagen = SMALL_IMG_DIR+'horno.png'

plancha = Elementos(pilas, -200, 450)
plancha.imagen = SMALL_IMG_DIR+'plancha.png'

scanner = Elementos(pilas, 315, 450)
scanner.imagen = SMALL_IMG_DIR+'scanner.png'

laser = Elementos(pilas, 70, 145)
laser.imagen = SMALL_IMG_DIR+'laser2.png'
laser.transparencia = 100

pantalla = Elementos(pilas, 450, 350)
pantalla.imagen = SMALL_IMG_DIR+'tele_prendido.png'

grilla = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR+"grilla_small.png", 23)
grilla_animacion = pilas.actores.Animacion(grilla, True)
grilla_animacion.x = pantalla.x - 5
grilla_animacion.y = pantalla.y - 33
grilla_animacion.transparencia = 55

grilla_cinta = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR+'animacion_cinta.png',3)
#grilla_animacion_cinta = pilas.actores.Animacion(grilla_cinta, True)
cinta = pilas.actores.Actor(x=-360, y=200)
cinta.z = 2
cinta.imagen = grilla_cinta
#grilla_animacion_cinta.y = 200
#grilla_animacion_cinta.x = -360
#grilla_animacion_cinta.z = 2


base = Base(pilas,95,426,SMALL_IMG_DIR + 'brazo3.png')   
brazo = Brazo(pilas,parte=SMALL_IMG_DIR + 'brazo2.png', base_param=base)
garra = Garra(pilas,parte=SMALL_IMG_DIR + 'brazo1.png', brazo=brazo)

garra.definir_centro((30,0))
brazo.definir_centro((22,0))

garra.rotacion = 12
base.definir_centro((25,base.alto-20))

base.aprender('arrastrable')

#######################################################

################## Funciones Auxiliares ###############

######################################################

# Generamos un rueda generica: dos al comienzo, despues
# viene ruedolph y despues generamos sin parar
def generar_rueda(test_p=IMG_DIR + '/mapa-chico-separado/bloque_generico.png'):
    rueda = RuedaGenerica(pilas=pilas,x=-800,y=430,param=test_p)
    rueda.z = 1
    return rueda

def generar_ruedolph():
    rueda = RuedaGenerica(pilas,-800,430, param=SMALL_IMG_DIR + 'bloque_perso_solido.png')
    rueda.z = 1
    return rueda

def genesis():
    global R
    R = Ruedolph(pilas)
    R.z = 1
    return R
# Vinculamos la garra a la rueda
def agarrar(r, g):
    r.poner_garra(g)

# Giramos el elemento g, 'y' grados
# si 'y' > 0, gira en sentido horario    
def gira(g, y):
    g.ponete_a_rotar(y)


def generar_texto(text='', x=0, y=0):
    t = pilas.actores.Texto(text, magnitud=27,x=x,y=y)
    t.color = 'rojo'
    t.transparencia = 100
    return t


def subir_diagonal(g, cinta):
    pilas.utils.interpolar(g, 'x', 210, 3.5)
    pilas.utils.interpolar(g, 'y', 270, 3.5)
    cinta.imagen.avanzar(10)

def llevar(b, x, t):
    pilas.utils.interpolar(b,'x',x,t)

def get_coord(pt):
    return pt.x + math.sin(math.radians(pt.rotacion))*pt.alto,\
        pt.y - math.cos(math.radians(pt.rotacion))*pt.alto

    
def get_coord2(pt):
    return pt.x + math.sin(math.radians(pt.rotacion))*pt.alto,\
        pt.y - math.cos(math.radians(pt.rotacion))*pt.alto


def laser_fade_in(l):
    laser.transparencia = [0],0.1

def laser_fade_out(l):
    laser.transparencia = [100],0.1


def girar_cinta():
    grilla_animacion_cinta= pilas.actores.Animacion(grilla_cinta, False, 1)
    grilla_animacion_cinta.y = 200
    grilla_animacion_cinta.x = -360
    grilla_animacion_cinta.z = 2


def aparece_emisor(e, b):
    if b:
        e.transparencia_min = 0
    else:
        e.transparencia_min = 100
        rm_emisor()

def mueve_cinta():
    cinta.imagen.avanzar()

def generar_emisor(const=True):
    emisor = pilas.actores.Emisor(horno.x, horno.y+100)
    emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
    emisor.constante = const
    emisor.transparencia_min = 100
    emisor.frecuencia_creacion = 0.3
    emisor.x_max =  100
    emisor.x_min = - 100
    emisor.dy_min = 7
    emisor.dy_max = -20
    emisor.composicion = "blanco"
    emisor.duracion = 4
    return emisor

def get_ruedolph():
    xs = pilas.actores.listar_actores()
    for x in xs:
        if isinstance(x, Ruedolph):
            return x

def rm_emisor():
    xs = pilas.actores.listar_actores()
    ys = [x for x in xs if isinstance(x, pilasengine.actores.Emisor)]
    for y in ys:
        y.eliminar()
###################################################

################## Movimientos ####################

###################################################
pilas.comportamientos.vincular(Mueve_x_y)
pilas.comportamientos.vincular(Desaparecer)
pilas.comportamientos.vincular(Mueve_x)
pilas.comportamientos.vincular(Mueve_y)
pilas.comportamientos.vincular(Mueve_y_arriba)
pilas.comportamientos.vincular(Eliminar)
pilas.comportamientos.vincular(Escanear)
pilas.comportamientos.vincular(ApareceTexto)
    
# Accion general que va a crear bloques de metal, derrertirlos
# y crear una rueda dentada a partir de un molde
def general(generico=True):
    # Generamos la rueda generica
    if generico:
        rg = generar_rueda()
    else:
        rg = generar_ruedolph()
    # El texto (por ahora) de la pantalla que
    # se va a inicializar totalmente transparente
    if generico:
        texto = 'OK\nOK\nOK'
    else:
        texto = 'Fail\nFail\nFail'
    texto_0 = generar_texto(texto, x=443, y=311)
    # La emision tambien esta presente todo el tiempo
    # solo la opacamos cuando necesitamos que aparezca
    e = generar_emisor()
    # Cae el bloque del tubo a la cinta
    pilas.tareas.agregar(1, mueve_y, rg, 280, )
    # El bloque se mueve desde donde cayo hacia el horno
    pilas.tareas.agregar(3, mueve_x, rg, 275, cinta)
    # El horno se enciende
    pilas.tareas.agregar(5.5, cambiar_imagen, horno, SMALL_IMG_DIR + 'hornoquemando.png')
    # Vemos el humo
    pilas.tareas.agregar(5.5, aparece_emisor, e, True)
    # Dejamos de ver humo
    pilas.tareas.agregar(6.8, aparece_emisor, e, False)
    # El horno se apaga
    pilas.tareas.agregar(6.5, cambiar_imagen, horno, SMALL_IMG_DIR + 'horno.png')
    # El bloque se ablanda
    if generico:
        bloque_img = SMALL_IMG_DIR + 'derretido_generico.png'
    else:
        bloque_img = SMALL_IMG_DIR+'bloque-ruedolph-derretido.png'
    pilas.tareas.agregar(8, cambiar_imagen, rg, bloque_img)
    # El bloque se mueve hacia la plancha (molde)
    pilas.tareas.agregar(8, mueve_x, rg, 310, cinta)
    # La plancha baja para darle forma al bloque
    pilas.tareas.agregar(11, mueve_y, plancha, 175)
    # La plancha sube
    pilas.tareas.agregar(14, mueve_y_arriba, plancha, -175, rg)
    # Ahora el bloque es una rueda
    if generico:
        rueda_img = SMALL_IMG_DIR + 'rueda_generica.png'
    else:
        rueda_img = SMALL_IMG_DIR + 'ruedolph.png'
    pilas.tareas.agregar(14, cambiar_imagen, rg, rueda_img)
    # La rueda se mueve hacia la rampa
    pilas.tareas.agregar(15, mueve_x, rg, 170, cinta)
    # La rueda sube la rampa hacia el escaner
    pilas.tareas.agregar(16.3, mueve_x_y, rg, 250, 130, cinta)
    # El escaner se enciende
    pilas.tareas.agregar(20, laser_fade_in, laser)
    # El escaner se apaga
    pilas.tareas.agregar(23, laser_fade_out, laser)
    # Vemos el texto
    pilas.tareas.agregar(23.5, aparece_texto, texto_0)
    # El brazo se mueve hacia la rueda
    pilas.tareas.agregar(26, gira, brazo, -70)
    # Giro de la garra hacia la rueda
    pilas.tareas.agregar(26.2, gira, garra, -55)
    # La garra agarra la rueda agarrable
    pilas.tareas.agregar(26.3, agarrar, rg, garra)
    if generico:
        # El brazo se mueve hacia arriba
        pilas.tareas.agregar(26.4, gira, brazo, 150)
        # La garra se mueve hacia arriba
        pilas.tareas.agregar(27, gira, garra, 200)
        # Eliminamos la rueda y el texto
        pilas.tareas.agregar(29, eliminar, [rg, texto_0,])
        # La garra vuelve a su posicion original
        pilas.tareas.agregar(30, gira, garra, -200 + 55)
        # El brazo vuelve a su posicion original
        pilas.tareas.agregar(30.3, gira, brazo, -150 + 70)
    else:
        pilas.tareas.agregar(26.4, llevar, base,-970,2)
        pilas.tareas.agregar(28.4, gira, garra,55 )
        pilas.tareas.agregar(28.7, agarrar, rg, None)
        pilas.tareas.agregar(29, mueve_y, rg, 380)
        pilas.tareas.agregar(29.4, gira, garra, -55+55)
        pilas.tareas.agregar(29.4, gira, brazo, 70)
        pilas.tareas.agregar(29.5, llevar, base, 95, 2)
        pilas.tareas.agregar(30.1, eliminar, [rg, texto_0])

def bar():
    pilas.tareas.agregar(1, general)
    pilas.tareas.agregar(32, general)
    pilas.tareas.agregar(63, general)

def eliminar_t(test_t):
    pilas.tareas.eliminar_tarea(test_t)

pilas.tareas.agregar(1, general)
pilas.tareas.agregar(32, general)
# Ruedolph
pilas.tareas.agregar(63, general, False)
p=pilas.tareas.agregar(2, genesis)
pilas.tareas.agregar(3, eliminar_t, p)

pilas.tareas.siempre(94, bar)




piso = pilas.fisica.Rectangulo(y=-450,ancho=2000,\
        restitucion = 0, friccion =0, amortiguacion=0, plataforma=1)
pared = pilas.fisica.Rectangulo(x=840,y=0,ancho=20,\
        alto=1080, restitucion = 0, friccion =0, amortiguacion=0, plataforma=1)
ventana = pilas.fisica.Rectangulo(x=830, y=-40,alto=50,\
ancho=50,dinamica=False,plataforma=1,sensor=1)
pilas.ejecutar()
