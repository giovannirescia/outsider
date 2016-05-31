# coding: utf-8

from __future__ import division
import pilasengine
from settings import IMG_DIR
from movimientos import *
from circulo_personalizado import Mi_Circulo
import math
from coordenadas import coor_esc_1, coor_esc_2
# original (small) = 2000, 1080
# debug = 1000, 500
# GLOBAL
en_colision = False
chequear = True
# GLOBAL
r = None
pilas = pilasengine.iniciar(2000, 1080, pantalla_completa=False, con_aceleracion='OpenGL')

SMALL_IMG_DIR = IMG_DIR + 'mapa-chico-separado/'

#mapa = pilas.fondos.Fondo(imagen=
           #     SMALL_IMG_DIR+"fondo_small.jpg")



###################################################

##################### Actores ######################

####################################################


class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = SMALL_IMG_DIR + 'ruedolph.png'
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(-780, -389, 50,
                                           friccion=0, restitucion=0, dinamica=1)
        self.figura_encaje = pilas.fisica.Circulo(self.x, self.y, 20,
                                                  friccion=0, restitucion=0, dinamica=0, sensor=1)
        self.imantado = False
        self.se_puede_mover = False
        self.garra = None
        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5,
                                                   sensor=True, dinamica=False, restitucion=0, amortiguacion=0)
        self.salto = 120
        self.fase = 0
    def actualizar(self):
        velocidad = 10
        salto = self.salto
#        pilas.eventos.pulsa_tecla.conectar(verificar)
        pilas.fisica.gravedad_y = -10
        # La camara sigue a Ruedolph
        cam = pilas.escena_actual().camara

        if self.garra is not None:
            self.figura.x, self.figura.y = self.garra.extremo
        if self.x >= 0:
            if self.x + 1000.0 / (cam.escala) <= 1000:
                cam.x = self.x
            else:
                cam.x = 1000 - 1000.0 / (cam.escala)
        else:
            if self.x - 1000.0 / (cam.escala) > -1000:
                cam.x = self.x
            else:
                cam.x = -1000 + 1000.0 / (cam.escala)
        if self.y >= 0:
            if self.y + 540.0 / (cam.escala) <= 540:
                cam.y = self.y
            else:
                cam.y = 540 - 540.0 / (cam.escala)
        else:
            if self.y - 540.0 / (cam.escala) > -540:
                cam.y = self.y
            else:
                cam.y = -540 + 540.0 / (cam.escala)

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
            if self.pilas.control.arriba and not int(self.figura.velocidad_y) and not pilas.control.boton and self.se_puede_mover:
                self.figura.impulsar(0, salto)

        self.sensor_pies.x = self.x
        self.sensor_pies.y = self.y - 53

    def esta_pisando_el_suelo(self):
        return any(isinstance(x, pilasengine.fisica.rectangulo.Rectangulo) for x in self.sensor_pies.figuras_en_contacto)

    def movete(self):
        self.se_puede_mover = True
        return False

    def imantate(self):
        self.imantado = True

    def poner_garra(self, g):
        self.garra = g

class Elementos(pilasengine.actores.Actor):
    def iniciar(self, x=0, y=0, es=''):
        self.x = x
        self.y = y
        self.es = es


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
    def iniciar(self, x, y, parte):
        self.x = x
        self.y = y
        self.imagen = parte


class Brazo(pilasengine.actores.Actor):
    def iniciar(self, parte, base_param):
        self.imagen = parte
        self.base_param = base_param
        self.rotacion = -60
        self.rotar = 0

    def actualizar(self):
        self.x = self.base_param.x + 12
        self.y = self.base_param.y + 3
        if self.rotar > 0:
            self.rotacion -= 5
            self.rotar -= 5
        if self.rotar < 0:
            self.rotacion += 5
            self.rotar += 5

    def ponete_a_rotar(self, val):
        self.rotar = val


class Garra(pilasengine.actores.Actor):
    def iniciar(self, parte, brazo):
        self.imagen = parte
        self.brazo = brazo
        self.rotacion = 90
        self.rotar = 0
        self.extremo = (self.x, self.y)

    def actualizar(self):
        self.x, self.y = get_coord(self.brazo)
        self.extremo = get_coord2(self)
        if self.rotar > 0:
            self.rotacion -= 5
            self.rotar -= 5
        if self.rotar < 0:
            self.rotacion += 5
            self.rotar += 5

    def ponete_a_rotar(self, val):
        self.rotar = val


class Pendorcho(pilasengine.actores.Actor):
    def iniciar(self, x, y, img, centro=(110, 80), cinta_rota = None):
        self.imagen = img
        self.y = y
        self.x = x
        self.bloque = None
        self.centro = centro
        self.cinta_rota = cinta_rota
        self.radio_de_colision = 10
        self.mc = Mi_Circulo(fisica=pilas.fisica, pilas=pilas, x=x, y=y,
                             radio=self.radio_de_colision, sensor=True, dinamica=False)
        self.piso = pilas.fisica.Rectangulo(x, y - 50, 30, 5, sensor=True, dinamica=False,
                                            restitucion=0, amortiguacion=0)
        self.estamina_cinta_rota = 0
    def actualizar(self):
        if self.cinta_rota is not None:
            if self.estamina_cinta_rota:
                self.cinta_rota.imagen.avanzar(5)
                self.estamina_cinta_rota -= 1
    
        self.mc.x, self.mc.y, self.piso.x, self.piso.y = self.x, self.y, self.x, self.y - 50


#Eslabon principal
class EslabonPrincipal(pilasengine.actores.Actor):
    def iniciar(self, x=-300, y=-400):
        self.imagen = SMALL_IMG_DIR + '/eslabon.png'
        self.escala = 0.4
        self.x = x
        self.z = 2
        self.y = y
        self.sigue = None

    def actualizar(self):
        if self.sigue is not None:
                self.x = self.sigue.x
                self.y = self.sigue.y


#Eslabones secundarios
class EslabonSecundario(pilasengine.actores.Actor):
    def iniciar(self, x, y, sigue):
        self.x = sigue.x + 10
        self.z = 2
        self.sigue = sigue
        self.escala = 0.4
        self.imagen = SMALL_IMG_DIR + '/eslabon.png'
        self.a_cola = True
    def actualizar(self):
        if self.sigue is not None:
            self.rotacion = self.sigue.rotacion / 2
            # la cadena sigue a derecha o izquierda
            if self.a_cola:
                self.x = min(self.sigue.x + 35, 779)
            else:
                self.x = min(self.sigue.x - 35, 779)
            if self.y > -400:
                if self.a_cola:
                    self.x = self.sigue.x + 10
                else:
                    self.x = self.sigue.x - 10
            self.y = max(self.sigue.y - 30, -400) - self.sigue.rotacion / 2
pilas.actores.vincular(EslabonPrincipal)
pilas.actores.vincular(EslabonSecundario)
pilas.actores.vincular(Pendorcho)
pilas.actores.vincular(Ruedolph)
pilas.actores.vincular(Elementos)
pilas.actores.vincular(Brazo)
pilas.actores.vincular(Garra)
pilas.actores.vincular(Base)
pilas.actores.vincular(RuedaGenerica)


#######################################################

################## Funciones Auxiliares ###############

######################################################

# Generamos un rueda generica: dos al comienzo, despues
# viene ruedolph y despues generamos sin parar
def generar_rueda(test_p=IMG_DIR + '/mapa-chico-separado/bloque_generico.png'):
    rueda = RuedaGenerica(pilas=pilas, x=-800, y=430, param=test_p)
    rueda.z = 1
    return rueda


def generar_ruedolph():
    rueda = RuedaGenerica(pilas, -800, 430, param=SMALL_IMG_DIR + 'bloque_perso_solido.png')
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
    t = pilas.actores.Texto(text, magnitud=27, x=x, y=y)
    t.color = 'rojo'
    t.transparencia = 100
    t.fijo = True
    return t


def subir_diagonal(g, cinta):
    pilas.utils.interpolar(g, 'x', 210, 3.5)
    pilas.utils.interpolar(g, 'y', 270, 3.5)
    cinta.imagen.avanzar(10)


def llevar(b, x, t):
    pilas.utils.interpolar(b, 'x', x, t)


def get_coord(pt):
    return (pt.x + math.sin(math.radians(pt.rotacion)) * pt.alto,
            pt.y - math.cos(math.radians(pt.rotacion)) * pt.alto)


def get_coord2(pt):
    return (pt.x + math.sin(math.radians(pt.rotacion)) * pt.alto,
            pt.y - math.cos(math.radians(pt.rotacion)) * pt.alto)


def laser_fade_in(laser):
    laser.transparencia = [0], 0.1


def laser_fade_out(laser):
    laser.transparencia = [100], 0.1


def girar_cinta():
    grilla_animacion_cinta = pilas.actores.Animacion(grilla_cinta, False, 1)
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



def generar_emisor_caida(x, y):
    emisor = pilas.actores.Emisor(x, y)
    emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
    emisor.constante = True
    emisor.transparencia_min = 100
    emisor.frecuencia_creacion = 0.1
    emisor.x_max = 30
    emisor.x_min = -50
    emisor.dy_min = 4
    emisor.vida = 2
    emisor.dy_max = 6
    emisor.composicion = "blanco"
    emisor.duracion = 2
    return emisor


# cinta rota
def girar(rueda, rodillo):
    if pilas.control.boton:
        em = generar_emisor_caida(-291, -430)
        em2 = generar_emisor_caida(-240, -462)
#        f = pilas.actores.Animacion(grilla= grilla_cinta_rota, ciclica=1)
  #      f.z = 2
        pilas.control.boton = True
        rueda.figura.x = rodillo.x
        rueda.figura.y = rodillo.y 
        pilas.utils.interpolar(rueda, 'rotacion', -720, 2.5,'lineal')
        pilas.utils.interpolar(rodillo, 'rotacion', -720, 2.5,'lineal')
        rodillo.estamina_cinta_rota = 155
#        pilas.tareas.agregar(0, mueve_x, bloque, 3, 0.5)
        pilas.tareas.agregar(0.0, aux_mueve_x_y, rodillo.bloque, -456.5, -167, 1)
        pilas.tareas.agregar(1.0, aux_mueve_x, rodillo.bloque, -415.3, 0.5)
        pilas.tareas.agregar(1.5, aux_mueve_x_y, rodillo.bloque, -305, -374, 1)
        pilas.tareas.agregar(2.5, opa, em, 0)
        pilas.tareas.agregar(2.5, opa, em2, 0)
        pilas.tareas.agregar(3.5, cambiar_img, rodillo.bloque)
        pilas.tareas.agregar(4.5, rm_emisor)
#        cinta.imagen(avanzar)


# encajar cadena en rodillo y girar rodillo para abrir la puerta
def girar_para_abrir(rueda, rodillo):
    if pilas.control.boton:
        pilas.control.boton = True
        rueda.figura.x = rodillo.x
        rueda.figura.y = rodillo.y 
        pilas.utils.interpolar(rueda, 'rotacion', -520, 2.5,'lineal')
        pilas.utils.interpolar(rodillo, 'rotacion', -520, 2.5,'lineal')

        pilas.tareas.condicional(0.5, mifun)

        puerta = get_elem('puerta')[0]
        pilas.tareas.condicional(1, cambiar_puerta, puerta, 1)
        pilas.tareas.condicional(1.5, cambiar_puerta, puerta, 2)

def fijar_cadena_rodillo():
    r = get_ruedolph()
    r.imantado = 0
    eslabon = filter(lambda x: isinstance(x, EslabonPrincipal), pilas.actores.listar_actores())[0]
    eslabon.sigue = None

def fijar_cadena_timon():
    timon = get_elem('timon')[0]
    eslabon = EslabonPrincipal(pilas, x=timon.x, y=timon.y)
    eslabon.aprender('arrastrable')
    xs = [eslabon]
    for j in range(0, 2):
        e = EslabonSecundario(pilas, 0, 0, xs[j])
        e.a_cola = False
        xs.append(e)

def aux_mueve_x(b, x, t):
    pilas.utils.interpolar(b, 'x', x,t,'lineal')

def aux_mueve_x_y(b, x, y, t=0.5):
    pilas.utils.interpolar(b,'x', x, t,'lineal')
    pilas.utils.interpolar(b,'y', y, t,'lineal')

def cambiar_img(b):
    b.imagen = SMALL_IMG_DIR + 'bronce-roto.png'
    b.x = -266

def opa(e, c):
    e.transparencia_min = c

def cambiar_puerta(p, n):
    # la puerta empieza cerrada (fase 0)
    # entreabierta: fase 1
    # abierta: fase 2
    if n == 1:
        p.imagen = SMALL_IMG_DIR + 'puerta-entreabierta.png'
    if n == 2:
        p.imagen = SMALL_IMG_DIR + 'puerta-abierta.png'
    p.z = -1
    return False

def generar_emisor(const, horno):
    emisor = pilas.actores.Emisor(horno.x, horno.y + 100)
    emisor.imagen_particula = pilas.imagenes.cargar_grilla("humo2.png")
    emisor.constante = const
    emisor.transparencia_min = 100
    emisor.frecuencia_creacion = 0.3
    emisor.x_max = 100
    emisor.x_min = -100
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


def verificar(evento):
    global en_colision
    ruedolph = get_ruedolph()
    if en_colision and pilas.control.boton:
        en_colision = False
        aux = None
        xs = ruedolph.figura.figuras_en_contacto
        for elem in xs:
            if isinstance(elem, Mi_Circulo):
                if ruedolph.figura != elem:
                    aux = elem
        if aux is not None:
            ruedolph.figura.x = aux.x
            ruedolph.figura.y = aux.y
            ruedolph.figura.velocidad_y = 0
            pilas.fisica.gravedad_y = 0


def encajar(Ruedolph, pendorchos):
    global en_colision
    en_colision = True


def seguir_rueda(rueda, eslabon):
    if rueda.imantado:
        eslabon.sigue = rueda


def imantacion(x, y):
    x.imantate()


def agarra_metal_rojo(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolph_fase_1.png'
        rueda.fase = 1


def agarra_metal_azul(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolph_fase_2.png'
        rueda.fase = 2


def agarra_metal_amarillo(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolph_fase_3.png'
        rueda.fase = 3


def crear_stats(fase):
    stats = pilas.actores.Actor(452, 304)
    if fase == 3:
        stats.imagen = SMALL_IMG_DIR + 'stats-ruedolph-sobra.png'
    elif fase == 4:
        stats.imagen = SMALL_IMG_DIR + 'stats-ok.png'
    stats.transparencia = 100
    return stats


def act_check_flag():
    global chequear
    chequear = True

def check():
    global chequear
    ruedolph = get_ruedolph()
    n = ruedolph.fase
    act_xs = pilas.actores.listar_actores()
    elementos_xs = filter(lambda x: isinstance(x, Elementos), act_xs)
    elem_es_xs = map(lambda x: x.es, elementos_xs)
    laser = elementos_xs[elem_es_xs.index('laser')]
    base = filter(lambda x: isinstance(x, Base), act_xs)[0]
    brazo = filter(lambda x: isinstance(x, Brazo), act_xs)[0]
    garra = filter(lambda x: isinstance(x, Garra), act_xs)[0]
    stats = crear_stats(n)
    ruedolph.se_puede_mover = False
    if chequear:
        t1 = pilas.tareas.agregar(1, laser_fade_in, laser)
        pilas.tareas.agregar(1.1, eliminar_t, t1)
        t2 = pilas.tareas.agregar(4, laser_fade_out, laser)
        pilas.tareas.agregar(4.1, eliminar_t, t2)


        if ruedolph.fase == 3:
            # garra agarra ruedolph y lo desecha
            t3 = pilas.tareas.agregar(5, aparece_texto, stats)
            pilas.tareas.agregar(5.1, eliminar_t, t3)
            # El brazo se mueve hacia la rueda
            t4 = pilas.tareas.agregar(8, gira, brazo, -70)
            pilas.tareas.agregar(8.1, eliminar_t, t4)
            
            # Giro de la garra hacia la rueda
            t5 = pilas.tareas.agregar(8.2, gira, garra, -55)
            pilas.tareas.agregar(8.3, eliminar_t, t5)
            
            # La garra agarra la rueda agarrable
            t6 = pilas.tareas.agregar(8.3, agarrar, ruedolph, garra)
            pilas.tareas.agregar(8.4, eliminar_t, t6)
            
            t7 = pilas.tareas.agregar(8.4, llevar, base, -970, 2)
            pilas.tareas.agregar(8.5, eliminar_t, t7)
            
            t8 = pilas.tareas.agregar(10.4, gira, garra, 55)
            pilas.tareas.agregar(10.5, eliminar_t, t8)
            
            t9 = pilas.tareas.agregar(10.7, agarrar, ruedolph, None)
            pilas.tareas.agregar(10.8, eliminar_t, t9)
            
            t10 = pilas.tareas.agregar(11, mueve_y, ruedolph, 380)
            pilas.tareas.agregar(11.1, eliminar_t, t10)
            
            t11 = pilas.tareas.agregar(11.4, gira, garra, -55 + 55)
            pilas.tareas.agregar(11.5, eliminar_t, t11)
            
            t12 = pilas.tareas.agregar(11.4, gira, brazo, 70)
            pilas.tareas.agregar(11.5, eliminar_t, t12)
            
            t13 = pilas.tareas.agregar(11.5, llevar, base, 95, 2)
            pilas.tareas.agregar(11.6, eliminar_t, t13)

            t14 = pilas.tareas.agregar(12.1, borrate, stats)
            pilas.tareas.agregar(12.2, eliminar_t, t14)
            
            t15 = pilas.tareas.condicional(13, ruedolph.movete)
            pilas.tareas.agregar(13.1, eliminar_t, t15)
            
            pilas.tareas.agregar(14, ruedolph.movete)
            chequear = False
    elif ruedolph.fase == 4:
        # garra agarra ruedolph y lo acepta
#        pilas.tareas.agregar(5, crear_stats, 4)
        pass
def borrate(elem):
    elem.eliminar()
    return False

def pasar_a_escenario_2():
    e2 = pilas.escenas.Escenario_2(True)
    e2.cambiar_a_escenario_2()
    ruedolph = get_ruedolph()
    pilas.eventos.pulsa_tecla.conectar(verificar)


def pasar_a_escenario_1():
    e1 = pilas.escenas.Escenario_1(False)
    e1.cambiar_a_escenario_1()
    ruedolph = get_ruedolph()
    pilas.eventos.pulsa_tecla.conectar(verificar)

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
def general(generico, horno, cinta, plancha, laser, base, brazo, garra):
    # Generamos la rueda generica
    if generico:
        rg = generar_rueda()
    else:
        rg = generar_ruedolph()
    # El texto (por ahora) de la pantalla que
    # se va a inicializar totalmente transparente
    if generico:
        texto = 'Cu: OK\nPo:OK\nUut:OK'
    else:
        texto = 'Cu: Fail\nPo: Ok\nUut: Fail'
    texto_0 = generar_texto(texto, x=443, y=311)
    # La emision tambien esta presente todo el tiempo
    # solo la opacamos cuando necesitamos que aparezca
    e = generar_emisor(True, horno)
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
        bloque_img = SMALL_IMG_DIR + 'bloque-ruedolph-derretido.png'
    pilas.tareas.agregar(8, cambiar_imagen, rg, bloque_img)
    # El bloque se mueve hacia la plancha (molde)
    pilas.tareas.agregar(8, mueve_x, rg, 310, cinta)
    # La plancha baja para darle forma al bloque
    pilas.tareas.agregar(11, mueve_y, plancha, 160)
    # La plancha sube
    pilas.tareas.agregar(14, mueve_y_arriba, plancha, -160, rg)
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
        pilas.tareas.agregar(26.6, gira, garra, 200)
        # Eliminamos la rueda y el texto
        pilas.tareas.agregar(29, eliminar, [rg, texto_0])
        # La garra vuelve a su posicion original
        pilas.tareas.agregar(30, gira, garra, -200 + 55)
        # El brazo vuelve a su posicion original
        pilas.tareas.agregar(30.3, gira, brazo, -150 + 70)
    else:
        pilas.tareas.agregar(26.4, llevar, base, -970, 2)
        pilas.tareas.agregar(28.4, gira, garra, 55)
        pilas.tareas.agregar(28.7, agarrar, rg, None)
        pilas.tareas.agregar(29, mueve_y, rg, 380)
        pilas.tareas.agregar(29.4, gira, garra, -55 + 55)
        pilas.tareas.agregar(29.4, gira, brazo, 70)
        pilas.tareas.agregar(29.5, llevar, base, 95, 2)
        pilas.tareas.agregar(30.1, eliminar, [rg, texto_0])


def bar():
    generico = True
    act_xs = pilas.actores.listar_actores()
    elementos_xs = filter(lambda x: isinstance(x, Elementos), act_xs)
    elem_es_xs = map(lambda x: x.es, elementos_xs)
    horno = elementos_xs[elem_es_xs.index('horno')]
    cinta = elementos_xs[elem_es_xs.index('cinta')]
    plancha = elementos_xs[elem_es_xs.index('plancha')]
    laser = elementos_xs[elem_es_xs.index('laser')]
    base = filter(lambda x: isinstance(x, Base), act_xs)[0]
    brazo = filter(lambda x: isinstance(x, Brazo), act_xs)[0]
    garra = filter(lambda x: isinstance(x, Garra), act_xs)[0]
    pilas.tareas.agregar(1, general, generico, horno, cinta, plancha, laser, base, brazo, garra)
    pilas.tareas.agregar(32, general, generico, horno, cinta, plancha, laser, base, brazo, garra)
    pilas.tareas.agregar(63, general, generico, horno, cinta, plancha, laser, base, brazo, garra)


def eliminar_t(test_t):
    try:
        test_t.terminar()
    except:
        pass
    return False

def escenario2():
    global r
    pilas.escenas.Escenario2(r)
    pilas.escena_actual().ejecutar()

def get_elem(tipo):
    xs = pilas.actores.listar_actores()
    ys = filter(lambda x: isinstance(x, Elementos), xs)
    return list(filter(lambda x: x.es == tipo, ys))
######################################


######                       ESCENARIOS                     ########


#######################################

# poner personaje en background
def bg(elem):
    elem.z = 0


class Escenario_1(pilasengine.escenas.Escena):
    def iniciar(self, pe):
        self.fondo = pilas.fondos.Fondo(imagen=SMALL_IMG_DIR + 'fondo_small.jpg')
        # primera ejecucion (cambia si aparece el bloque de ruedolph)
        self.pe = pe

    def cambiar_a_escenario_1(self):
        ################################################################

        ################## Elementos del Escenario #####################

        #################################################################

        # Elementos de la cinta: tubo, horno, plancha, pantalla, scanner

        tubo = Elementos(pilas, -800, 415, es='tubo')
        tubo.imagen = SMALL_IMG_DIR + 'tubo.png'

        horno = Elementos(pilas, -520, 170, es='horno')
        horno.imagen = SMALL_IMG_DIR + 'horno.png'

        plancha = Elementos(pilas, -200, 450, es='plancha')
        plancha.imagen = SMALL_IMG_DIR + 'plancha.png'

        scanner = Elementos(pilas, 315, 450, es='escaner')
        scanner.imagen = SMALL_IMG_DIR + 'scanner.png'

        laser = Elementos(pilas, 70, 145, es='laser')
        laser.imagen = SMALL_IMG_DIR + 'laser2.png'
        laser.transparencia = 100

        pantalla = Elementos(pilas, 450, 350, es='pantalla')
        pantalla.imagen = SMALL_IMG_DIR + 'tele_prendido.png'

        grilla = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + "grilla_small.png", 23)
        grilla_animacion = pilas.actores.Animacion(grilla, True)
        grilla_animacion.x = pantalla.x - 5
        grilla_animacion.y = pantalla.y - 33
        grilla_animacion.transparencia = 55

        grilla_cinta = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'animacion_cinta.png', 3)
        cinta = pilas.actores.Elementos(x=-360, y=200, es='cinta')
        cinta.z = 2
        cinta.imagen = grilla_cinta

        grilla_timon = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'timon-grilla-SMALL.png', 46)
        timon = pilas.actores.Elementos(x=812, y=-320, es='timon')
        timon.imagen = grilla_timon
        timon.centro = (100, 100)
        timon.x, timon.y = 812, -320
#        timon.aprender('arrastrable')
        timon.z = 3
        
        puerta = Elementos(pilas, 773, -334, es='puerta')
        puerta.imagen = SMALL_IMG_DIR + 'puerta-cerrada.png'
        puerta.z = 4
        
        
        
        if self.pe:
            bloque_bronce = Elementos(pilas, x=-519, y=-40, es='bloque-bronce-sano')
            bloque_bronce.imagen = SMALL_IMG_DIR + 'bronce.png'
            bloque_bronce.z = 3
        else:
            bloque_bronce = Elementos(pilas, x=-266, y=-374, es='bloque-bronce-roto')
            bloque_bronce.imagen = SMALL_IMG_DIR + 'bronce-roto.png'
            bloque_bronce.z = 3
        bloque_bronce.escala = 0.7
        bloque_bronce.radio_de_colision = 60
        bloque_bronce.rotacion = 10
        bloque_bronce.aprender('arrastrable')


        check_flag = pilas.actores.ActorInvisible(-800, -380)



        grilla_cinta_rota = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'cinta-rota-grilla.png', 3)
        cinta_rota = pilas.actores.Elementos(x=-474, y=-224.7, es='cinta-rota')
        cinta_rota.z = 5
        cinta_rota.aprender('arrastrable')
        cinta_rota.imagen = grilla_cinta_rota
        # rodillo de la cinta rota
        rodillo = Pendorcho(pilas, -454, -290.8, SMALL_IMG_DIR + 'rodillo-3.png', (0,0),cinta_rota)
        rodillo.z = 1
        rodillo.bloque = bloque_bronce
        rodillo.centro = (20,20)
        rodillo.aprender('arrastrable')


        base = Base(pilas, 95, 426, SMALL_IMG_DIR + 'brazo3.png')
        brazo = Brazo(pilas, parte=SMALL_IMG_DIR + 'brazo2.png', base_param=base)
        garra = Garra(pilas, parte=SMALL_IMG_DIR + 'brazo1.png', brazo=brazo)
        garra.definir_centro((30, 0))
        brazo.definir_centro((22, 0))

        garra.rotacion = 12
        base.definir_centro((25, base.alto - 20))
        base.aprender('arrastrable')

        piso = pilas.fisica.Rectangulo(y=-450, ancho=2000,
                                       restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pared = pilas.fisica.Rectangulo(x=870, y=0, ancho=20,
                                        alto=1080, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        # ventana
        ventana = pilas.actores.ActorInvisible(x=830, y=-40)
        ventana.transparencia = 50
        ventana.figura_de_colision = pilas.fisica.Rectangulo(830, -40, 55, 55, sensor=True, dinamica=False)
        plataforma_piso = pilas.fisica.Rectangulo(x=200, y=210, alto=20,
                                                  ancho=150, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        pantalla_caja = pilas.fisica.Rectangulo(x=450, y=300, ancho=275,
                                                alto=230, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        ruedolph = Ruedolph(pilas)
        ruedolph.z = -1
        # no es la primera vez que esta en este escenario
        if not self.pe:
            c = pilas.escena_actual().camara
            c.escala = 1
            ruedolph.figura.x = 600
            ruedolph.figura.y = -389
            ruedolph.imagen = SMALL_IMG_DIR + 'ruedolph_fase_2.png'
            ruedolph.imantate()
            ruedolph.fase = 3
            ruedolph.z = -1
            # lugar donde ruedolph se va a posicionar para ser escaneado
            lugar = pilas.actores.ActorInvisible(189, 284)
            lugar.radio_de_colision = 10
            lugar.transparencia = 50
            
            eslabon = EslabonPrincipal(pilas, x=600)
            eslabon.aprender('arrastrable')
            cadena = pilas.actores.Grupo()
            cadena.agregar(eslabon)
            xs = [eslabon]
            for j in range(0, 39):
                e = EslabonSecundario(pilas, 0, 0, xs[j])
                e.aprender('arrastrable')
                cadena.agregar(e)
                xs.append(e)
      #      map(bg, xs)
            pilas.colisiones.agregar(ruedolph, eslabon, seguir_rueda)
            
            pilas.colisiones.agregar(ruedolph, lugar, check)
            pilas.colisiones.agregar(ruedolph, rodillo, girar_para_abrir)
            pilas.colisiones.agregar(eslabon, rodillo, fijar_cadena_rodillo)
            pilas.colisiones.agregar(eslabon, timon, fijar_cadena_timon)

        ys = map(lambda attr: Pendorcho(pilas, x=attr[0], y=attr[1], centro=attr[2], img=attr[3]), coor_esc_1)

        pendorchos = pilas.actores.Grupo()
        map(lambda x: pendorchos.agregar(x), ys)
        map(lambda x: x.aprender('arrastrable'), ys)

       # pilas.tareas.agregar(1, general, True, horno, cinta, plancha, laser, base, brazo, garra)
       # pilas.tareas.agregar(32, general, True, horno, cinta, plancha, laser, base, brazo, garra)
        # Ruedolph
        if self.pe:
            generico_flag = False
        else:
            generico_flag = True
       # pilas.tareas.agregar(63, general, generico_flag, horno, cinta, plancha, laser, base, brazo, garra)

      #  pilas.tareas.siempre(94, bar)
        pilas.tareas.condicional(1, ruedolph.movete)
        if self.pe:
            pilas.colisiones.agregar(ruedolph, rodillo, girar)
        pilas.colisiones.agregar(ruedolph, bloque_bronce, agarra_metal_amarillo)
        pilas.colisiones.agregar(ruedolph, ventana, pasar_a_escenario_2)
        pilas.colisiones.agregar(ruedolph, pendorchos, encajar)
        pilas.colisiones.agregar(ruedolph, check_flag, act_check_flag)
        monticulo = pilas.actores.Actor(-640, -271, SMALL_IMG_DIR + 'monticulo-small.png')
        monticulo.z = -2
        return ruedolph


class Escenario_2(pilasengine.escenas.Escena):
    def iniciar(self, pe=True):
        self.fondo = pilas.fondos.Fondo(imagen=SMALL_IMG_DIR + "fondo_escenario_2_small.jpg")
        self.pe = pe

    def cambiar_a_escenario_2(self):
        ruedolph = Ruedolph(pilas)
        ruedolph.movete()
        ruedolph.z = 0
        # generamos los pendorchos, coor_esc_2 es una lista
        # donde cada elementos es (x, y, (centro_x, centro_y), ruta_de_la_imagen)
        colgables = map(lambda attr: Pendorcho(pilas, x=attr[0], y=attr[1], centro=attr[2], img=attr[3]), coor_esc_2)
        iman = pilas.actores.Actor(x=550, y=-280)
        iman.transparencia = 100
        iman.radio_de_colision = 100
        piso_escenario_2 = pilas.fisica.Rectangulo(y=-450, ancho=2000,
                                                   restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pared_escenario_2 = pilas.fisica.Rectangulo(x=-870, y=0, ancho=20,
                                                    alto=1080, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        metal_rojo = pilas.actores.Actor(x=236, y=426)
        metal_rojo.radio_de_colision = 30
        metal_rojo.imagen = SMALL_IMG_DIR + 'metal_rojo_1.png'
        metal_azul = pilas.actores.Actor(x=-623, y=200)
        metal_azul.radio_de_colision = 30
        metal_azul.imagen = SMALL_IMG_DIR + 'metal_azul_3.png'
        ventana = pilas.actores.Actor(-826, -36)
        ventana.transparencia = 77
        ventana.figura_de_colision = pilas.fisica.Rectangulo(ventana.x, ventana.y,
                                                             500, 500, sensor=True, dinamica=False)
        # generamos la cadena si es la primera vez que entra al escenario
        if self.pe:
            eslabon = EslabonPrincipal(pilas)
            eslabon.aprender('arrastrable')
            xs = [eslabon]
            for j in range(0, 19):
                xs.append(EslabonSecundario(pilas, 0, 0, xs[j]))
        map(bg, xs)
        pilas.colisiones.agregar(ruedolph, iman, imantacion)
        pilas.colisiones.agregar(ruedolph, metal_rojo, agarra_metal_rojo)
        pilas.colisiones.agregar(ruedolph, metal_azul, agarra_metal_azul)
        pilas.colisiones.agregar(ruedolph, eslabon, seguir_rueda)
        pilas.colisiones.agregar(ruedolph, colgables, encajar)
        pilas.colisiones.agregar(ruedolph, ventana, pasar_a_escenario_1)
        return ruedolph

pilas.escenas.vincular(Escenario_1)
pilas.escenas.vincular(Escenario_2)

e1 = pilas.escenas.Escenario_1(True)
ruedolph = e1.cambiar_a_escenario_1()
pilas.eventos.pulsa_tecla.conectar(verificar)

def mifun():
    ys = filter(lambda x: isinstance(x, EslabonSecundario), pilas.actores.listar_actores())
    for elem in ys:
        elem.sigue = None
    xs = map(lambda elem: (elem.x, elem), ys)
    xs.sort(key=lambda x:-x[0])    
    for i in range(len(xs)):
        x = xs[i][1]
        aux = i*0.73
        x.y = [-320 + aux],1.6
    return False
pilas.ejecutar()
