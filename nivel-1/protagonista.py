# coding: utf-8
import pilasengine
from settings import IMG_DIR
from circulo_personalizado import Mi_Circulo
# Variable global
en_colision = False
pilas = pilasengine.iniciar()


class Ruedolph(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = SMALL_IMG_DIR + 'ruedolph.png'
        self.radio_de_colision = 20
        self.figura = pilas.fisica.Circulo(-0,-0, 50,
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
        # La camara sigue a Ruedolph
        if self.x >=0:
            if self.x + 1000.0/(cam.escala)<=1000:
                cam.x = self.x
            else:
                cam.x = 1000 - 1000.0/(cam.escala)
        else:
            if self.x - 1000.0/(cam.escala) > -1000:
                cam.x = self.x
            else:
                cam.x = -1000 + 1000.0/(cam.escala)
        if self.y >=0:
            if self.y + 540.0/(cam.escala) <= 540:
                cam.y = self.y
            else:
                cam.y = 540 - 540.0/(cam.escala)
        else:
            if self.y - 540.0/(cam.escala) > -540:
                cam.y = self.y
            else:
                cam.y = -540 + 540.0/(cam.escala)
        
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


class Pendorcho(pilasengine.actores.Actor):
    def iniciar(self, x, y):
        self.imagen = IMG_DIR + '/tornillo.png'
        self.y = y
        self.x = x
        self.escala = 0.1
        self.radio_de_colision = 10
        self.mc = Mi_Circulo(fisica=pilas.fisica, pilas=pilas, x=x, y=y,
            radio=self.radio_de_colision, sensor=True, dinamica=False)
        self.piso = pilas.fisica.Rectangulo(x, y - 50, 30, 5,
                sensor=True, dinamica=False, restitucion=0, amortiguacion=0)

pilas.actores.vincular(Pendorcho)
pilas.actores.vincular(Ruedolph)
r = Ruedolph(pilas)
t1 = Pendorcho(pilas, 0, -110)
t2 = Pendorcho(pilas, 180, -5)
t3 = Pendorcho(pilas, -12, 90)
t4 = Pendorcho(pilas, 165, 188)
t5 = Pendorcho(pilas, -80, -47)

pendorchos = pilas.actores.Grupo()
pendorchos.agregar(t1)
pendorchos.agregar(t2)
pendorchos.agregar(t3)
pendorchos.agregar(t4)
pendorchos.agregar(t5)

def verificar(evento):
    global en_colision
    if en_colision and pilas.control.boton:
        en_colision = False
        aux = None
        xs = r.figura.figuras_en_contacto
        for elem in xs:
            if isinstance(elem, pilasengine.fisica.circulo.Circulo):
                if r.figura != elem:
                    aux = elem
        r.figura.x = aux.x
        r.figura.y = aux.y
        pilas.fisica.gravedad_y = 0
        r.figura.velocidad_y = 0


def encajar(r, pendorchos):
    global en_colision
    en_colision = True

pilas.eventos.pulsa_tecla.conectar(verificar)
pilas.colisiones.agregar(r, pendorchos, encajar)

pilas.ejecutar()
