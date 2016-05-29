# coding: utf-8

import pilasengine
from settings import *
pilas = pilasengine.iniciar()
# GLOBAL
en_colision = False

SMALL_IMG_DIR = IMG_DIR + 'mapa-chico-separado/'

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

def mueve_x(b, x, t):
    pilas.utils.interpolar(b, 'x', x,t,'lineal')

def mueve_x_y(b, x, y, t=0.5):
    pilas.utils.interpolar(b,'x', x, t,'lineal')
    pilas.utils.interpolar(b,'y', y, t,'lineal')

def cambiar_img(b):
    b.imagen = SMALL_IMG_DIR + 'bronce-roto.png'
    b.x = 195


def opa(e, c):
    e.transparencia_min = c

def rm_emisor():
    xs = pilas.actores.listar_actores()
    ys = [x for x in xs if isinstance(x, pilasengine.actores.Emisor)]
    for y in ys:
        y.eliminar()

def girar(rueda, rodillo):
    if pilas.control.boton:
        em = generar_emisor_caida(170, -190)
        em2 = generar_emisor_caida(222, -222)
#        f = pilas.actores.Animacion(grilla= grilla_cinta_rota, ciclica=1)
  #      f.z = 2
        pilas.control.boton = True
        rueda.figura.x = rodillo.x
        rueda.figura.y = rodillo.y 
        pilas.utils.interpolar(rueda, 'rotacion', -520, 2,'lineal')
        pilas.utils.interpolar(rodillo, 'rotacion', -520, 2,'lineal')
        rodillo.estamina = 155
#        pilas.tareas.agregar(0, mueve_x, bloque, 3, 0.5)
        pilas.tareas.agregar(0.0, mueve_x_y, bloque, 4.5, 93, 1)
        pilas.tareas.agregar(1.0, mueve_x, bloque, 46.7, 0.5)
        pilas.tareas.agregar(1.5, mueve_x_y, bloque, 157, -134, 1)
        pilas.tareas.agregar(2.5, opa, em, 0)
        pilas.tareas.agregar(2.5, opa, em2, 0)
        pilas.tareas.agregar(3.5, cambiar_img, bloque)
        pilas.tareas.agregar(4.5, rm_emisor)
#        cinta.imagen(avanzar)



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

#em = generar_emisor()
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
        self.figura.sin_rotacion = True
        self.figura.escala_de_gravedad = 3
        self.sensor_pies = pilas.fisica.Rectangulo(self.x, self.y, 30, 5,
                                                   sensor=True, dinamica=False, restitucion=0, amortiguacion=0)
        self.salto = 150
        self.estamina_rotacion = 0
        self.z = 0
    def actualizar(self):
        velocidad = 10
        salto = self.salto
        pilas.fisica.gravedad_y = -10
        # La camara sigue a Ruedolph
        cam = pilas.escena_actual().camara
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
        if self.estamina_rotacion:
            self.rotacion += 3
            self.estamina_rotacion =-3
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

class Elementos(pilasengine.actores.Actor):
    def iniciar(self, x=0, y=0, es=''):
        self.x = x
        self.y = y
        self.es = es

class Pendorcho(pilasengine.actores.Actor):
    def iniciar(self, x, y, img, cinta):
        self.imagen = img
        self.y = y
        self.cinta = cinta
        self.x = x
        self.radio_de_colision = 10
        self.mc = Mi_Circulo(fisica=pilas.fisica, pilas=pilas, x=x, y=y,
                             radio=self.radio_de_colision, sensor=True, dinamica=False)
        self.piso = pilas.fisica.Rectangulo(x, y - 50, 30, 5, sensor=True, dinamica=False,
                                            restitucion=0, amortiguacion=0)
        self.estamina = 0
    def actualizar(self):
        if self.estamina:
            self.cinta.imagen.avanzar(5)
            self.estamina -= 1
        self.mc.x, self.mc.y, self.piso.x, self.piso.y = self.x, self.y, self.x, self.y - 50

pilas.actores.vincular(Pendorcho)
pilas.actores.vincular(Elementos)
pilas.actores.vincular(Ruedolph)

ruedolph = Ruedolph(pilas)
rodillo.escala = 1
ruedolph.figura.x = 0
ruedolph.figura.y = 0
ruedolph.movete()

grilla_cinta_rota = pilas.imagenes.cargar_grilla(SMALL_IMG_DIR + 'cinta-rota-grilla.png', 3)
cinta_rota = pilas.actores.Elementos(x=0, y=0, es='cinta-rota')
cinta_rota.z = 2
cinta_rota.imagen = grilla_cinta_rota
rodillo.aprender('arrastrable')
rodillo = Pendorcho(pilas, 17, -63, SMALL_IMG_DIR + 'rodillo-3.png', cinta_rota)
rodillo.z = 1

bloque = Elementos(pilas, x=-58, y=200, es='bloque-bronce-sano')
bloque.imagen = SMALL_IMG_DIR + 'bronce.png'
bloque.escala = 0.7
bloque.z = 1
bloque.rotacion = 10
bloque.aprender('arrastrable')

pilas.eventos.pulsa_tecla.conectar(verificar)
pilas.colisiones.agregar(ruedolph, rodillo, girar)
pilas.ejecutar()
