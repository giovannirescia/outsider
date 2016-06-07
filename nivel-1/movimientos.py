# coding: utf-8

import pilasengine
from settings import IMG_DIR
# Acciones relacionadas a la cinta

class Mueve_y(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor, stamina):
        self.receptor = receptor
        self.stamina = stamina
    def actualizar(self):
        if self.stamina>0:
            self.receptor.y -= 8
            self.stamina -= 8
        else:
             return True

class Mueve_y_arriba(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor, stamina, rueda):
        self.receptor = receptor
        self.stamina = stamina
        self.rueda = rueda
    def actualizar(self):
        if self.stamina<0:
            self.receptor.y += 8
            self.stamina += 8
        else:
             return True

class Mueve_x(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor, stamina, cinta):
        self.receptor = receptor
        self.cinta = cinta
        self.stamina = stamina
    def actualizar(self):
        if self.stamina>0:
            self.receptor.x += 2
            self.stamina -= 2
            self.cinta.imagen.avanzar(6)
            rg = self.cinta.rodillos
            for r in rg:
                r.rotacion -= 5
        else:
             return True

# para que las ruedas suban la diagonal
class Mueve_x_y(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor, stamina_x, stamina_y, cinta):
        self.receptor = receptor
        self.stamina_x = stamina_x
        self.stamina_y = stamina_y
        self.cinta = cinta
    def actualizar(self):
        velocidad = 1
        if self.stamina_x>0:
            self.receptor.x += velocidad + 1
            self.stamina_x -= (velocidad + 1)
            if self.stamina_y:
                self.receptor.y += velocidad
                self.stamina_y -= velocidad
            self.cinta.imagen.avanzar(6)
            rg = self.cinta.rodillos
            for r in rg:
                r.rotacion -= 5

        else:
             return True

class Eliminar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
    def actualizar(self):
        self.receptor.eliminar()
        return True

class Desaparecer(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
    def actualizar(self):
        if self.receptor.transparencia < 100:
            self.receptor.transparencia += 1
        else:
            # Con retornar True le indicamos a pilas que este
            # comportamiento terminó y tiene que pasar al siguiente.
            return True

class Moverse(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.se_mueve = False
    def actualizar(self):
        self.receptor.aprender('Moverseconelteclado')
        return True

class Escanear(pilasengine.comportamientos.Comportamiento):
    
    def iniciar(self, receptor):
        self.receptor = receptor
        self.prende = True
    def actualizar(self):
        if self.prende:
            if self.receptor.transparencia > 0:
                self.receptor.transparencia -= 10
            else:
                self.prende = False
        else:
            if self.receptor.transparencia < 100:
                self.receptor.transparencia += 10
            else:
                return True

class ApareceTexto(pilasengine.comportamientos.Comportamiento):
    def iniciar(self, receptor):
        receptor.transparencia = 7
    def actualizar(self):
        return True        

def mueve_x(g, stamina, cinta):
    g.hacer("Mueve_x", stamina, cinta)

def mueve_y(g, stamina):
    g.hacer("Mueve_y",stamina)

def mueve_y_arriba(g, stamina, rueda):
    g.hacer("Mueve_y_arriba",stamina, rueda)

def mueve_x_y(g, stamina_x, stamina_y, cinta):
        g.hacer("Mueve_x_y", stamina_x, stamina_y, cinta)

def llevar_rueda(g, r):
    r.imitar(g.sensor)
    g.rotacion =[360], 5

def eliminar(xs):
    for elem in xs:
        elem.hacer("Eliminar")

def cambiar_imagen(actor, imagen):
    actor.imagen = imagen

def desaparecer(g):
    g.hacer("Desaparecer")

def escanear(e):
    e.hacer("Escanear")


def aparece_texto(t):
    t.hacer("ApareceTexto")        
