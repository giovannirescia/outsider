# coding: utf-8
pilas = pilasengine.iniciar(alto=900,ancho=1600)

class Ruedolph(pilasengine.actores.Actor):
    def iniciar(self):
        self.radio_de_colision = 50
        self.imagen = "/home/giovanni/proyectos/outsider/imagenes/nivel-1/ruedolph_small.png"
     
    def actualizar(self):
       aux_speed = 10
       aux_rot =3
       if self.pilas.control.izquierda:
          self.figura.velocidad_x = -aux_speed
          self.rotacion += aux_rot
       elif self.pilas.control.derecha:
          self.figura.velocidad_x = aux_speed
          self.rotacion -= aux_rot
       else:
          self.figura.velocidad_x = 0

pilas.actores.vincular(Ruedolph)
ruedolph = Ruedolph(pilas)
c = pilas.fisica.Circulo(y=-300, x=-500, radio=50, amortiguacion=0,restitucion=0,)
ruedolph.imitar(c)
xs = []
for i in range(0,30):
    xs.append(pilas.fisica.Rectangulo(ancho=200,alto=2, y=-190-20*i, x=500-150*i,
        plataforma=1, dinamica=False,amortiguacion=1))

pilas.fisica.definir_gravedad_y(-100)

pilas.ejecutar()