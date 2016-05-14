# coding: utf-8
import pilasengine
import time

pilas = pilasengine.iniciar()

def foo():
    return pilas.actores.Banana()

class Mueve_x(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.stamina = 50
    def actualizar(self):
        if self.stamina:
            self.receptor.x += 1
            self.stamina -= 1
        else:
             return True

class Eliminar(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
    def actualizar(self):
        self.receptor.eliminar()
        return True
class Moverse(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.se_mueve = False
    def actualizar(self):
        self.receptor.aprender('Moverseconelteclado')
        return True
class Mueve_y(pilasengine.comportamientos.Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.stamina = 50
    def actualizar(self):
        if self.stamina:
            self.receptor.y -= 1
            self.stamina -= 1
        else:
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
class Esperar(pilasengine.comportamientos.Comportamiento):
    def iniciar(self, receptor):
        self.receptor = receptor
    def actualizar(self):
        time.sleep(5)
        return True
                                 
pilas.comportamientos.vincular(Desaparecer)
pilas.comportamientos.vincular(Mueve_x)
pilas.comportamientos.vincular(Mueve_y)
pilas.comportamientos.vincular(Eliminar)
pilas.comportamientos.vincular(Esperar)

def aparece():
    mono = foo()
    mono.hacer("Mueve_y")
    mono.hacer("Mueve_x")
    mono.hacer("Mueve_x")
    mono.hacer("Desaparecer")
    mono.hacer("Eliminar")
def aparece2():
    mono = foo()
    mono.aprender('Moverseconelteclado')

def mueve_x(g):
    g.hacer("Mueve_x")
def mueve_y(g):
    g.hacer("Mueve_y")
def eliminar(g):
    g.hacer("Eliminar")
def desaparecer(g):
    g.hacer("Desaparecer")

def general():
    m = foo()
    pilas.tareas.agregar(1, mueve_y, m)
    pilas.tareas.agregar(2, mueve_x, m)
    pilas.tareas.agregar(4, mueve_x, m)
    pilas.tareas.agregar(7, mueve_x, m)
    pilas.tareas.agregar(8, desaparecer, m)
    pilas.tareas.agregar(11, eliminar, m)
#pilas.tareas.agregar(1, aparece)
#pilas.tareas.agregar(5, aparece)
#pilas.tareas.agregar(9, aparece2)
#pilas.tareas.siempre(4,aparece)
pilas.tareas.agregar(1,general)
pilas.tareas.agregar(12,general)
pilas.ejecutar()