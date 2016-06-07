# coding: utf-8

from __future__ import division
import pilasengine
from random import randint
from settings import IMG_DIR
from movimientos import *
from circulo_personalizado import Mi_Circulo
import math
from coordenadas import coor_esc_1, coor_esc_2, coor_cad, coor_rod_cinta, coor_rod_cinta_rota
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
class Ruedolf(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = SMALL_IMG_DIR + 'ruedolf.png'
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
        self.tiene_cadena = False
        self.camara = False
        self.seguido_por_camara = False
        c = pilas.escena_actual().camara
        c.escala = [1], 1
        c.x = 0
        c.y = 0

    def actualizar(self):
        velocidad = 10
        salto = self.salto
        pilas.fisica.gravedad_y = -10
        # La camara sigue a Ruedolf
        cam = pilas.escena_actual().camara
        if self.garra is not None:
            self.figura.x, self.figura.y = self.garra.extremo
        if self.seguido_por_camara:
            if self.se_puede_mover:
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
            if self.seguido_por_camara:

                self.activar_camara()
            self.figura.velocidad_x = velocidad
            self.rotacion -= velocidad

        elif self.pilas.control.izquierda and self.se_puede_mover:
            if self.seguido_por_camara:
                self.activar_camara()

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

    def activar_camara(self, val=2, seguir=True):
        c = pilas.escena_actual().camara
        self.seguido_por_camara = seguir
        if val == 1:
            c.x = [0], 0.5
            c.y = [0], 0.5
        c.escala = [val], 0.5

    def esta_pisando_el_suelo(self):
        return any(isinstance(x, pilasengine.fisica.rectangulo.Rectangulo) for x in self.sensor_pies.figuras_en_contacto)

    def movete(self):
        self.se_puede_mover = True
        return False

    def imantate(self):
        self.imantado = True

    def poner_garra(self, g):
        self.garra = g

    def restore_zoom(self):
        c = pilas.escena_actual().camara
        c.escala = [1], 1
        c.x = [0], 1
        c.y = [0], 1


class Elementos(pilasengine.actores.Actor):
    def iniciar(self, x=0, y=0, es=''):
        self.x = x
        self.y = y
        self.es = es
        self.rodillos = None


class RuedaGenerica(pilasengine.actores.Actor):
    def iniciar(self, x, y, param, cam_lo_sigue):
        self.x = x
        self.y = y
        self.garra = None
        self.imagen = param
        self.cam_lo_sigue = cam_lo_sigue

    def actualizar(self):
        if self.garra is not None:
            self.x, self.y = self.garra.extremo
        if self.cam_lo_sigue:
            cam = pilas.escena_actual().camara
            cam.escala = [2], 2

            if self.x >= 0:
                if self.x + 1000.0 / (cam.escala) <= 1000:
                    cam.x = [self.x], 0.5
                else:
                    cam.x = [1000 - 1000.0 / (cam.escala)], 0.5
            else:
                if self.x - 1000.0 / (cam.escala) > -1000:
                    cam.x = [self.x], 0.5
                else:
                    cam.x = [-1000 + 1000.0 / (cam.escala)], 0.5
            if self.y >= 0:
                if self.y + 540.0 / (cam.escala) <= 540:
                    cam.y = [self.y], 0.5
                else:
                    cam.y = [540 - 540.0 / (cam.escala)], 0.5
            else:
                if self.y - 540.0 / (cam.escala) > -540:
                    cam.y = [self.y], 0.5
                else:
                    cam.y = [-540 + 540.0 / (cam.escala)], 0.5

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
        self.rodillos = None
        self.timon = None
    def actualizar(self):
        if self.cinta_rota is not None:
            if self.estamina_cinta_rota:
                self.cinta_rota.imagen.avanzar(5)
                if self.timon is not None:
                    self.timon.imagen.avanzar(25)
                self.estamina_cinta_rota -= 1
                r_xs = self.rodillos
                for rodillo in r_xs:
                    rodillo.rotacion -= 3
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
    def iniciar(self, x, y, sigue=None):
        if sigue is not None:
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
pilas.actores.vincular(Ruedolf)
pilas.actores.vincular(Elementos)
pilas.actores.vincular(Brazo)
pilas.actores.vincular(Garra)
pilas.actores.vincular(Base)
pilas.actores.vincular(RuedaGenerica)

#######################################################

################## Funciones Auxiliares ###############

######################################################

# Generamos un rueda generica: dos al comienzo, despues
# viene ruedolf y despues generamos sin parar


def generar_rueda(test_p=IMG_DIR + '/mapa-chico-separado/bloque_generico.png', cam_lo_sigue=False):
    rueda = RuedaGenerica(pilas=pilas, x=-800, y=430, param=test_p, cam_lo_sigue=cam_lo_sigue)
    rueda.z = 1
    return rueda


def restore_zoom():
    pass


def generar_ruedolf(cam_lo_sigue=False):
    rueda = RuedaGenerica(pilas, -800, 430, param=SMALL_IMG_DIR + 'bloque_perso_solido.png', cam_lo_sigue=cam_lo_sigue)
    rueda.z = 1
    return rueda


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
    emisor.z = -7
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
        pilas.utils.interpolar(rueda, 'rotacion', -720, 2.5, 'lineal')
        pilas.utils.interpolar(rodillo, 'rotacion', -720, 2.5, 'lineal')
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
        rueda = get_ruedolf()
        pilas.control.boton = True
        rueda.figura.x = rodillo.x
        rueda.figura.y = rodillo.y
        t = get_elem('timon')[0]
        pilas.utils.interpolar(rueda, 'rotacion', -500, 2, 'lineal')
        pilas.utils.interpolar(rodillo, 'rotacion', -500, 2, 'lineal')
        rodillo.timon = t
        # tambien funciona para el timon
        rodillo.estamina_cinta_rota = 124

        for rod in rodillo.rodillos:
            pilas.utils.interpolar(rod, 'rotacion', -500, 2, 'lineal')

        pilas.tareas.condicional(0.5, mifun)
        rueda.seguido_por_camara = False
        pilas.tareas.una_vez(0, rueda.activar_camara, 1, False)
        pilas.tareas.una_vez(5, rueda.activar_camara, 2, True)

        puerta = get_elem('puerta')[0]
        pilas.tareas.condicional(1, cambiar_puerta, puerta, 1)
        pilas.tareas.condicional(1.5, cambiar_puerta, puerta, 2)


def fijar_cadena_rodillo():
    r = get_ruedolf()
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
    pilas.utils.interpolar(b, 'x', x, t, 'lineal')


def aux_mueve_x_y(b, x, y, t=0.5):
    pilas.utils.interpolar(b, 'x', x, t, 'lineal')
    pilas.utils.interpolar(b, 'y', y, t, 'lineal')


def cambiar_img(b):
    b.imagen = SMALL_IMG_DIR + 'bronce-roto.png'
    b.x = -266


def opa(e, c):
    e.transparencia_min = c


def puerta_nivel():
    e2 = pilas.escenas.Escenario_2(False, viene_de_ventana=False)
    e2.cambiar_a_escenario_2()
    ruedolf = get_ruedolf()
    pilas.eventos.pulsa_tecla.conectar(verificar)


def cambiar_puerta(p, n):
    # la puerta empieza cerrada (fase 0)
    # entreabierta: fase 1
    # abierta: fase 2
    r = get_ruedolf()
    if n == 1:
        p.imagen = SMALL_IMG_DIR + 'puerta-entreabierta.png'
    if n == 2:
        p.imagen = SMALL_IMG_DIR + 'puerta-abierta.png'
        puerta = pilas.actores.ActorInvisible(850, p.y)
        puerta.transparencia = 100
        puerta.figura_de_colision = pilas.fisica.Rectangulo(x=puerta.x, y=p.y, alto=200, ancho=50, sensor=True, dinamica=False)
        pilas.colisiones.agregar(r, puerta, puerta_nivel)
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


def get_ruedolf():
    xs = pilas.actores.listar_actores()
    for x in xs:
        if isinstance(x, Ruedolf):
            return x


# piezas empiezan con rotacion random
def randrot(xs):
    for x in xs:
        x.rotacion = randint(0, 359)


def rm_emisor():
    xs = pilas.actores.listar_actores()
    ys = [x for x in xs if isinstance(x, pilasengine.actores.Emisor)]
    for y in ys:
        y.eliminar()


def verificar(evento):
    global en_colision
    ruedolf = get_ruedolf()
    if en_colision and pilas.control.boton:
        en_colision = False
        aux = None
        xs = ruedolf.figura.figuras_en_contacto
        for elem in xs:
            if isinstance(elem, Mi_Circulo):
                if ruedolf.figura != elem:
                    aux = elem
        if aux is not None:
            ruedolf.figura.x = aux.x
            ruedolf.figura.y = aux.y
            ruedolf.figura.velocidad_y = 0
            pilas.fisica.gravedad_y = 0


def encajar(Ruedolf, pendorchos):
    global en_colision
    en_colision = True


def seguir_rueda(rueda, eslabon):
    if rueda.imantado:
        eslabon.sigue = rueda
        rueda.tiene_cadena = True


def imantacion(x, y):
    x.imantate()
    if x.fase > 2:
        piedritas = pilas.actores.Actor(x.x, x.y, SMALL_IMG_DIR + 'piedritas-iman.png')
        aux_mueve_x_y(piedritas, piedritas.x + 72, piedritas.y + 56, t=0.2)
        x.imagen = SMALL_IMG_DIR + 'ruedolf.png'


def agarra_metal_rojo(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolf-fase-1.png'
        rueda.fase = 1


def agarra_metal_azul(rueda, metal):
    if rueda.imantado:
        rueda.imagen = SMALL_IMG_DIR + 'ruedolf-fase-2.png'
        rueda.fase = 2


def agarra_metal_amarillo(rueda, metal):
    if rueda.imantado:
        if rueda.fase == 2:
            rueda.imagen = SMALL_IMG_DIR + 'ruedolf-fase-3.png'
            rueda.fase = 3
        elif rueda.fase == 1:
            rueda.imagen = SMALL_IMG_DIR + 'ruedolf-fase-4.png'


def vuelta_final():
    e1 = pilas.escenas.Escenario_1(False, 1)
    e1.cambiar_a_escenario_1()
    ruedolf = get_ruedolf()
    pilas.eventos.pulsa_tecla.conectar(verificar)


def crear_stats(fase):
    stats = pilas.actores.Actor(450, 310)
    stats_dict = {
        1: SMALL_IMG_DIR + 'stats-ok.png',
        2: SMALL_IMG_DIR + 'stats-ruedolf.png',
        3: SMALL_IMG_DIR + 'stats-ruedolf-sobra.png',
        200: SMALL_IMG_DIR + 'stats-tick.png',
        404: SMALL_IMG_DIR + 'stats-cruz.png',
    }
    stats.imagen = stats_dict[fase]
    if fase > 3:
        stats.y = 250
    stats.transparencia = 100
    return stats


def act_check_flag():
    global chequear
    chequear = True


def check():
    global chequear
    ruedolf = get_ruedolf()
    n = ruedolf.fase
    act_xs = pilas.actores.listar_actores()
    elementos_xs = filter(lambda x: isinstance(x, Elementos), act_xs)
    elem_es_xs = map(lambda x: x.es, elementos_xs)
    laser = elementos_xs[elem_es_xs.index('laser')]
    base = filter(lambda x: isinstance(x, Base), act_xs)[0]
    brazo = filter(lambda x: isinstance(x, Brazo), act_xs)[0]
    garra = filter(lambda x: isinstance(x, Garra), act_xs)[0]
    stats = crear_stats(n)
    ruedolf.se_puede_mover = True
#    pilas.tareas.eliminar_todas()
    if chequear:
        t1 = pilas.tareas.agregar(1, laser_fade_in, laser)
        pilas.tareas.agregar(1.1, eliminar_t, t1)
        t2 = pilas.tareas.agregar(4, laser_fade_out, laser)
        pilas.tareas.agregar(4.1, eliminar_t, t2)

        if ruedolf.fase == 3:
            substats = crear_stats(404)
            # garra agarra ruedolf y lo desecha
            t3 = pilas.tareas.agregar(5, aparece_texto, stats)
            t33 = pilas.tareas.agregar(6, aparece_texto, substats)
            pilas.tareas.agregar(5.1, eliminar_t, t3)
            pilas.tareas.agregar(6.1, eliminar_t, t33)

            # El brazo se mueve hacia la rueda
            t4 = pilas.tareas.agregar(8, gira, brazo, -70)
            pilas.tareas.agregar(8.1, eliminar_t, t4)

            # Giro de la garra hacia la rueda
            t5 = pilas.tareas.agregar(8.2, gira, garra, -55)
            pilas.tareas.agregar(8.3, eliminar_t, t5)

            # La garra agarra la rueda agarrable
            t6 = pilas.tareas.agregar(8.3, agarrar, ruedolf, garra)
         #   pilas.tareas.agregar(8.4, eliminar_t, t6)

            t7 = pilas.tareas.agregar(8.4, llevar, base, -970, 2)
        #    pilas.tareas.agregar(8.5, eliminar_t, t7)

            t8 = pilas.tareas.agregar(10.4, gira, garra, 55)
       #     pilas.tareas.agregar(10.5, eliminar_t, t8)

            t9 = pilas.tareas.agregar(10.7, agarrar, ruedolf, None)
      #      pilas.tareas.agregar(10.8, eliminar_t, t9)

            t10 = pilas.tareas.agregar(11, mueve_y, ruedolf, 380)
     #       pilas.tareas.agregar(11.1, eliminar_t, t10)

            t11 = pilas.tareas.agregar(11.4, gira, garra, -55 + 55)
    #        pilas.tareas.agregar(11.5, eliminar_t, t11)

            t12 = pilas.tareas.agregar(11.4, gira, brazo, 70)
   #         pilas.tareas.agregar(11.5, eliminar_t, t12)

            t13 = pilas.tareas.agregar(11.5, llevar, base, 95, 2)
  #          pilas.tareas.agregar(11.6, eliminar_t, t13)

            t14 = pilas.tareas.agregar(12.1, borrate, stats)
            t1414 = pilas.tareas.agregar(12.1, borrate, substats)

 #           pilas.tareas.agregar(12.2, eliminar_t, t14)

            t15 = pilas.tareas.condicional(13, ruedolf.movete)
#            pilas.tareas.agregar(13.1, eliminar_t, t15)

            pilas.tareas.agregar(14, ruedolf.movete)
            chequear = False
        # Aceptamos a Ruedolf
        elif ruedolf.fase == 1:
            substats = crear_stats(200)
            # garra agarra ruedolf y lo desecha
            t3 = pilas.tareas.agregar(5, aparece_texto, stats)
            t33 = pilas.tareas.agregar(6, aparece_texto, substats)
            pilas.tareas.agregar(5.1, eliminar_t, t3)
            pilas.tareas.agregar(6.1, eliminar_t, t33)

            # El brazo se mueve hacia la rueda
            t4 = pilas.tareas.agregar(8, gira, brazo, -70)
            pilas.tareas.agregar(8.1, eliminar_t, t4)

            # Giro de la garra hacia la rueda
            t5 = pilas.tareas.agregar(8.2, gira, garra, -55)
            pilas.tareas.agregar(8.3, eliminar_t, t5)

            # La garra agarra la rueda agarrable
            t6 = pilas.tareas.agregar(8.3, agarrar, ruedolf, garra)
         #   pilas.tareas.agregar(8.4, eliminar_t, t6)

            # El brazo se mueve hacia arriba
            pilas.tareas.agregar(8.4, gira, brazo, 150)
            # La garra se mueve hacia arriba
            pilas.tareas.agregar(8.4, gira, garra, 200)
            # Eliminamos la rueda y el texto
            pilas.tareas.agregar(9, eliminar, [ruedolf])
            pilas.tareas.agregar(10.8, eliminar, [stats, substats])
            # La garra vuelve a su posicion original
            pilas.tareas.agregar(12.4, gira, garra, -200 + 55)
            # El brazo vuelve a su posicion original
            pilas.tareas.agregar(12.7, gira, brazo, -150 + 70)
            pilas.tareas.una_vez(14, restore_zoom)


def borrate(elem):
    elem.eliminar()
    return False


def restore_zoom():
    c = pilas.escena_actual().camara
    c.escala = [1]
    c.x = [0], 1
    c.y = [0], 1


def pasar_a_escenario_2():
    ruedolf = get_ruedolf()
    e2 = pilas.escenas.Escenario_2(True, ruedolf.fase)
    e2.cambiar_a_escenario_2()
    pilas.eventos.pulsa_tecla.conectar(verificar)


def pasar_a_escenario_1():
    ruedolf = get_ruedolf()
    e1 = pilas.escenas.Escenario_1(False, ruedolf.fase, ruedolf.tiene_cadena)
    e1.cambiar_a_escenario_1()
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
def general(generico, horno, cinta, plancha, laser, base, brazo, garra, cam_seguir_rueda):
    # Generamos la rueda generica
    if generico:
        rg = generar_rueda(cam_lo_sigue=cam_seguir_rueda)
    else:
        rg = generar_ruedolf(cam_lo_sigue=cam_seguir_rueda)
    # El texto (por ahora) de la pantalla que
    # se va a inicializar totalmente transparente
    if generico:
        texto = crear_stats(1)
        subtexto = crear_stats(200)
    else:
        texto = crear_stats(2)
        subtexto = crear_stats(404)
    # La emision tambien esta presente todo el tiempo
    # solo la opacamos cuando necesitamos que aparezca
    e = generar_emisor(True, horno)
    # Cae el bloque del tubo a la cinta
    pilas.tareas.agregar(1, mueve_y, rg, 280, )
    # El bloque se mueve desde donde cayo hacia el horno
    pilas.tareas.agregar(3, mueve_x, rg, 275, cinta)
    # El horno se enciende
    pilas.tareas.agregar(5.5, cambiar_imagen, horno, SMALL_IMG_DIR + 'horno-quemando.png')
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
        bloque_img = SMALL_IMG_DIR + 'bloque-ruedolf-derretido.png'
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
        rueda_img = SMALL_IMG_DIR + 'ruedolf.png'
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
    pilas.tareas.agregar(23.5, aparece_texto, texto)
    pilas.tareas.agregar(24.3, aparece_texto, subtexto)

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
        pilas.tareas.agregar(29, eliminar, [rg, texto, subtexto])
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
        pilas.tareas.agregar(30.1, eliminar, [rg, texto, subtexto])


def bar():
    r = get_ruedolf()
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
    pilas.tareas.agregar(1, general, generico, horno, cinta, plancha, laser, base, brazo, garra, False)
    pilas.tareas.agregar(32, general, generico, horno, cinta, plancha, laser, base, brazo, garra, False)
    pilas.tareas.agregar(63, general, generico, horno, cinta, plancha, laser, base, brazo, garra, False)


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

# poner el elemento en background (pensado para la cadena)
def bg(elem):
    elem.z = 5


class Escenario_1(pilasengine.escenas.Escena):
    def iniciar(self, pe, f=2, tc=False):
        self.fondo = pilas.fondos.Fondo(imagen=SMALL_IMG_DIR + 'fondo_small.jpg')
        # primera ejecucion (cambia si aparece el bloque de ruedolf)
        self.pe = pe
        self.f = f
        self.tc = tc

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

        laser = Elementos(pilas, 128, 257, es='laser')
        laser.imagen = SMALL_IMG_DIR + 'laser.png'
        laser.transparencia = 100
        laser.z = -6
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

        rod_xs = list(map(lambda attr: pilas.actores.Actor(x=attr[0], y=attr[1], imagen=attr[2]), coor_rod_cinta))
        for rod_x in rod_xs:
            rod_x.rotacion = randint(0, 359)
        rod_g = pilas.actores.Grupo()
#        map(randrot, rod_xs)
        map(rod_g.agregar, rod_xs)

        cinta.rodillos = rod_g

        grilla_timon = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'timon-grilla-SMALL.png', 46)
        timon = pilas.actores.Elementos(x=812, y=-320, es='timon')
        timon.imagen = grilla_timon
        timon.centro = (100, 100)
        timon.x, timon.y = 812, -320
        timon.z = 3

        puerta = Elementos(pilas, 773, -334, es='puerta')
        puerta.imagen = SMALL_IMG_DIR + 'puerta-cerrada.png'
        puerta.z = 4

        puerta.aprender('arrastrable')
        ruedolf = Ruedolf(pilas)
        ruedolf.seguido_por_camara = True
        ruedolf.z = -1

        if self.pe:
            pilas.tareas.una_vez(97, ruedolf.restore_zoom)
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

        check_flag = pilas.actores.ActorInvisible(-800, -380)

        grilla_cinta_rota = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'cinta-rota-grilla.png', 3)
        cinta_rota = pilas.actores.Elementos(x=-474, y=-224.7, es='cinta-rota')
        cinta_rota.z = 5

        cinta_rota.imagen = grilla_cinta_rota
        # rodillo de la cinta rota
        rodillo = Pendorcho(pilas, -454, -290.8, SMALL_IMG_DIR + 'rodillo-3.png', (0, 0), cinta_rota)
        rodillo.z = 1
        rodillo.bloque = bloque_bronce
        rodillo.centro = (20, 20)
        #rodillo.aprender('arrastrable')
        rodillos_cinta_rota = map(lambda attr: pilas.actores.Actor(x=attr[0], y=attr[1], imagen=attr[2]), coor_rod_cinta_rota)
        for rod_x in rodillos_cinta_rota:
            rod_x.rotacion = randint(0, 359)

        rodillo.rodillos = rodillos_cinta_rota

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
        ventana.transparencia = 100
        ventana.figura_de_colision = pilas.fisica.Rectangulo(830, -40, 55, 55, sensor=True, dinamica=False)
        plataforma_piso = pilas.fisica.Rectangulo(x=200, y=210, alto=20,
                                                  ancho=150, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        pantalla_caja = pilas.fisica.Rectangulo(x=450, y=300, ancho=275,
                                                alto=230, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        # no es la primera vez que esta en este escenario
        if not self.pe:
            ruedolf.figura.x = 650
            if self.tc or self.f > 1:
                #ruedolf = get_ruedolf()
                ruedolf.figura.y = -36
            else:
                ruedolf.figura.y = -389
            ruedolf.imantate()
            ruedolf.z = -1
            # lugar donde ruedolf se va a posicionar para ser escaneado
            lugar = pilas.actores.ActorInvisible(189, 284)
            lugar.radio_de_colision = 10
            lugar.transparencia = 100

            if self.f == 2:
                ruedolf.imagen = SMALL_IMG_DIR + 'ruedolf-fase-2.png'
                ruedolf.fase = 2
            elif self.f == 3:
                ruedolf.imagen = SMALL_IMG_DIR + 'ruedolf-fase-3.png'
                ruedolf.fase = 3
                ruedolf.imantate()
                if self.tc:
                    eslabon = EslabonPrincipal(pilas, x=650, y=-36)
                    eslabon.aprender('arrastrable')
                    cadena = pilas.actores.Grupo()
                    cadena.agregar(eslabon)
                    xs = [eslabon]
                    for j in range(0, 39):
                        e = EslabonSecundario(pilas, 0, 0, xs[j])
                        e.aprender('arrastrable')
                        cadena.agregar(e)
                        xs.append(e)

                    pilas.colisiones.agregar(ruedolf, eslabon, seguir_rueda)
                    pilas.colisiones.agregar(ruedolf, rodillo, girar_para_abrir)
                    pilas.colisiones.agregar(eslabon, rodillo, fijar_cadena_rodillo)
                    pilas.colisiones.agregar(eslabon, timon, fijar_cadena_timon)

            elif self.f == 1:
                ruedolf.imagen = SMALL_IMG_DIR + 'ruedolf-fase-1.png'
                ruedolf.fase = 1
                puerta.imagen = SMALL_IMG_DIR + 'puerta-abierta.png'
                xs = map(lambda attr: EslabonSecundario(pilas, x=attr[0], y=attr[1]), coor_cad)
                map(bg, xs)
                timon.z = 5

            pilas.colisiones.agregar(ruedolf, lugar, check)

        ys = map(lambda attr: Pendorcho(pilas, x=attr[0], y=attr[1], centro=attr[2], img=attr[3]), coor_esc_1)

        pendorchos = pilas.actores.Grupo()
        map(lambda x: pendorchos.agregar(x), ys)
        map(lambda x: x.aprender('arrastrable'), ys)
        if self.pe:
            aux_flag_cam = True
        else:
            aux_flag_cam = False
        pilas.tareas.agregar(1, general, True, horno, cinta, plancha, laser, base, brazo, garra, aux_flag_cam)
        pilas.tareas.agregar(32, general, True, horno, cinta, plancha, laser, base, brazo, garra, aux_flag_cam)

        # Ruedolf
        if self.pe:
            generico_flag = False
        else:
            generico_flag = True
        pilas.tareas.agregar(63, general, generico_flag, horno, cinta, plancha, laser, base, brazo, garra, aux_flag_cam)

        pilas.tareas.siempre(94, bar)
        if self.pe:
            pilas.tareas.condicional(100, ruedolf.movete)
        else:
            pilas.tareas.condicional(1, ruedolf.movete)
        if self.pe:
            pilas.colisiones.agregar(ruedolf, rodillo, girar)
        pilas.colisiones.agregar(ruedolf, bloque_bronce, agarra_metal_amarillo)
        pilas.colisiones.agregar(ruedolf, ventana, pasar_a_escenario_2)
        pilas.colisiones.agregar(ruedolf, pendorchos, encajar)
        pilas.colisiones.agregar(ruedolf, check_flag, act_check_flag)
        monticulo = pilas.actores.Actor(-640, -271, SMALL_IMG_DIR + 'monticulo-small.png')
        monticulo.z = -2
        return ruedolf


class Escenario_2(pilasengine.escenas.Escena):
    def iniciar(self, pe=True, fase=0, viene_de_ventana=True):
        self.fondo = pilas.fondos.Fondo(imagen=SMALL_IMG_DIR + "fondo_escenario_2_small.jpg")
        self.pe = pe
        self.fase = fase
        self.vdv = viene_de_ventana

    def cambiar_a_escenario_2(self):
        ruedolf = Ruedolf(pilas)
        ruedolf.fase = self.fase
        ruedolf.z = -2
        # viene desde la puerta
        if not self.pe:
            ruedolf.imagen = SMALL_IMG_DIR + 'ruedolf-fase-3.png'
            ruedolf.fase = 3
            ruedolf.figura.x = -700
            # puerta de vuelta
            puerta_de_vuelta = pilas.actores.Actor(-850, -330)
            puerta_de_vuelta.transparencia = 100
            puerta_de_vuelta.figura_de_colision = pilas.fisica.Rectangulo(x=-950, y=-330, alto=200, ancho=60, sensor=True, dinamica=False)
            pilas.colisiones.agregar(ruedolf, puerta_de_vuelta, vuelta_final)
        ruedolf.movete()
        ruedolf.seguido_por_camara = True
        if self.vdv:
            pc = pilas.actores.Actor(-821, -336, SMALL_IMG_DIR + 'puerta-cerrada-e2.png')
            pc.z = 3
            ruedolf.figura.y = -36
            ruedolf.figura.x = -650
        # generamos los pendorchos, coor_esc_2 es una lista
        # donde cada elementos es (x, y, (centro_x, centro_y), ruta_de_la_imagen)
        colgables = map(lambda attr: Pendorcho(pilas, x=attr[0], y=attr[1], centro=attr[2], img=attr[3]), coor_esc_2)
        iman = pilas.actores.Actor(x=550, y=-280)
        iman.transparencia = 100
        iman.radio_de_colision = 100
        piso_escenario_2 = pilas.fisica.Rectangulo(x=-200, y=-450, ancho=1300,
                                                   restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pared_escenario_2 = pilas.fisica.Rectangulo(x=-870, y=0, ancho=20,
                                                    alto=1080, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        # piso bajada antes del iman y pared del iman
        pb1 = pilas.fisica.Rectangulo(x=450, y=-465, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pb2 = pilas.fisica.Rectangulo(x=485, y=-470, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pb3 = pilas.fisica.Rectangulo(x=540, y=-460, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        pb4 = pilas.fisica.Rectangulo(x=560, y=-450, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)
        # pared
        pb5 = pilas.fisica.Rectangulo(x=621, y=-430, alto=400, restitucion=0, friccion=0, amortiguacion=0, plataforma=1)

        metal_rojo = pilas.actores.Actor(x=240, y=421)
        metal_rojo.radio_de_colision = 30
        metal_rojo.imagen = SMALL_IMG_DIR + 'rojas.png'
        metal_azul = pilas.actores.Actor(x=-629, y=197)
        metal_azul.radio_de_colision = 30
        metal_azul.imagen = SMALL_IMG_DIR + 'azules.png'
        ventana = pilas.actores.Actor(-826, -36)
        ventana.transparencia = 100
        ventana.figura_de_colision = pilas.fisica.Rectangulo(ventana.x, ventana.y,
                                                             55, 55, sensor=True, dinamica=False)
       # generamos la cadena si es la primera vez que entra al escenario (o si es la segunda por la ventana)
        if self.pe:
            if self.fase == 3:
                ruedolf.imagen = SMALL_IMG_DIR + 'ruedolf-fase-3.png'
                ruedolf.imantate()
            eslabon = EslabonPrincipal(pilas)
            eslabon.aprender('arrastrable')
            xs = [eslabon]
            for j in range(0, 19):
                xs.append(EslabonSecundario(pilas, 0, 0, xs[j]))
            map(bg, xs)
            pilas.colisiones.agregar(ruedolf, eslabon, seguir_rueda)

        pilas.colisiones.agregar(ruedolf, iman, imantacion)
        pilas.colisiones.agregar(ruedolf, metal_rojo, agarra_metal_rojo)
        pilas.colisiones.agregar(ruedolf, metal_azul, agarra_metal_azul)
        pilas.colisiones.agregar(ruedolf, colgables, encajar)
        pilas.colisiones.agregar(ruedolf, ventana, pasar_a_escenario_1)
        return ruedolf

pilas.escenas.vincular(Escenario_1)
pilas.escenas.vincular(Escenario_2)
#e1 = pilas.escenas.Escenario_1(True)
# desde el escenario 2, con los materiales (fase 2) y sin la cadena
#e1 = pilas.escenas.Escenario_1(False, 2, False)
# desde el escenario 2, con los materiales (fase 3) y la cadena
e1 = pilas.escenas.Escenario_1(False, 3, tc=True)
# desd el escenario 2, con el material rojo, sin la cadena
#e1 = pilas.escenas.Escenario_1(False, 1, tc=False)
ruedolf = e1.cambiar_a_escenario_1()
pilas.eventos.pulsa_tecla.conectar(verificar)


# esta funcion 'estira' la cadena desde el rodillo hacia el timon
def mifun():
    ys = filter(lambda x: isinstance(x, EslabonSecundario), pilas.actores.listar_actores())
    for elem in ys:
        elem.sigue = None
    xs = map(lambda elem: (elem.x, elem), ys)
    xs.sort(key=lambda x: -x[0])
    for i in range(len(xs)):
        x = xs[i][1]
        aux = i * 0.73
        x.y = [-320 + aux], 1.6
    return False

pilas.ejecutar()
