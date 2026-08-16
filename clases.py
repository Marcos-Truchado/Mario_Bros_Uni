import pyxel
from sprites import (
    BLOQUE_SPRITE, tortuga_sprite, tortuga_sprite_2_derecha, tortuga_sprite_2_izquierda,
    tortuga_sprite_izquierda, MOSCA_SPRITE,CANGREJO_SPRITE, MONEDA_SPRITE,)
class Mario:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y
        self.GRAVEDAD = 0.8
        self.ALTURA_SALTO = 10
        self.velocidad_y = 0
        self.bloques = [
            *[(x, 150) for x in range(0, 90)],
            *[(x, 150) for x in range(190, 285)],
            *[(x, 118) for x in range(250, 285)],
            *[(x, 118) for x in range(0, 35)],
            *[(x, 92) for x in range(70, 210)],
            *[(x, 45) for x in range(0, 95)],
            *[(x, 45) for x in range(175, 285)],
            *[(x, 20) for x in range(130, 140)]]
        self.pow = [(x, 143) for x in range(143, 150)]
        self.__vidas = 3
        self.salto = False
        self.monedas = 0
        self.puntos = 0
        self.kills=0
        self.mario_size = (16, 16)
        self.tablero=[]
    @property
    def x(self) -> int:
        return self.__x
    @property
    def y(self) -> int:
        return self.__y
    @property
    def sprite(self) -> tuple:
        return (0, 0, 0, self.mario_size[0], self.mario_size[1])
    def frame_sprite(self, direccion: int, frame: int) -> tuple:
        """Devuelve el sprite animado de Mario (banco 2): direccion 1 =
        derecha, 2 = izquierda, frame 0 = quieto, 1-2 = pasos de caminar."""
        fila = 0 if direccion == 1 else 16
        return (2, frame * 16, fila, self.mario_size[0], self.mario_size[1])
    @property
    def vidas(self) -> int:
        return self.__vidas
    @x.setter
    def x(self, x: int):
        self.__x = x
    @y.setter
    def y(self, y: int):
        self.__y = y
    @vidas.setter
    def vidas(self, vidas: int):
        self.__vidas = vidas
    def mover(self, direccion: str, tamaño: int):
        # funcion para mover a mario incluimos el teletransporte de mario
        # cuando este supera los limites
        if direccion.lower() == "derecha":
            self.x = (self.x + 2)
            if self.x>288:
                self.x=0
        elif direccion.lower() == "izquierda":
            self.x = (self.x - 2)
            if self.x<0:
                self.x=288
        if self.x > 270 and self.y >160:
            self.x=20
            self.y=30
        if self.x < 20 and self.y >160:
            self.x=238
            self.y=30
    def aplicar_gravedad(self, size: int):
        mario_y_size = self.mario_size[1]
        # Almacena la posición previa de Mario antes de aplicar la gravedad
        old_y = self.y
        # Si se mantiene presionada la tecla de espacio y Mario está en el suelo o encima de un bloque, realiza el salto
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) and (
                self.tocando_plataforma()):
            self.velocidad_y = self.ALTURA_SALTO
        else:
            self.y=old_y
        self.y -= self.velocidad_y
        self.velocidad_y -= self.GRAVEDAD
        if self.y >= size - mario_y_size:
            self.y = size - mario_y_size
            self.velocidad_y = 0
    def tocando_plataforma(self):
        # Verifica si Mario está tocando alguna plataforma
        return any(
            self.y + self.mario_size[1] == y_pos for y_pos in [150, 118, 92,45,202,20])
    def perder_vida(self):
        #funcion paea perder vidas
        self.__vidas-=1
        self.__x=130
        self.__y=0
        if self.__vidas==0:
            pyxel.quit()
    def ganar_monedas(self):
        self.monedas+=1
    def realizar_salto(self, direccion: str):
        if (direccion.lower() == 'up' and self.velocidad_y==0 and (
                self.tocando_plataforma ())):
            self.velocidad_y = self.ALTURA_SALTO
    def recolectar_moneda(self):
        self.monedas += 1
    def ganar_puntos(self):
        self.puntos += self.kills*2
class Tortuga:
    def __init__(self, x: int, y: int ,direccion:int):
        self.x = x
        self.y = y
        self.tiempo_bloqueo = 0
        self.TIEMPO_BLOQUEO_MAXIMO = 50
        self.sprite_derecha = tortuga_sprite  # Sprite cuando la tortuga se mueve a la derecha
        self.sprite_izquierda = tortuga_sprite_izquierda  # Sprite cuando la tortuga se mueve a la izquierda
        self.sprite_derecha_2=tortuga_sprite_2_derecha
        self.sprite_izquierda_2=tortuga_sprite_2_izquierda
        self.sprite_actual = self.sprite_derecha
        self.tumbado = False
        self.direccion= direccion
        self.velocidad_x = 1
        self.muerta = False
        self.levantado=0
        self.GRAVEDAD = 0.8
        self.girar=False
        self.velocidad_y = 0
        self.tiempo_tumbado = 0
        self.TIEMPO_MAX_TUMBADO = 150

    def aplicar_gravedad(self, suelo: int):
        # Aplicar la lógica de la gravedad a la tortuga
        self.y -= self.velocidad_y
        self.velocidad_y -= self.GRAVEDAD
        if self.y >= suelo:
            self.y = suelo
            self.velocidad_y = 0
    def colision_con_bloques(self, bloques):
        # para conseguir la colision con los bloques iteramos la lista y
        # comprobamos que la velocidad en el ejey sea negativa , lo que
        # significa que esta aterrizando
        for bloque in bloques:
            if (self.x < bloque[0] + BLOQUE_SPRITE[3]-4 and
                self.x + self.sprite_actual[3]-4 > bloque[0] and
                self.y + self.sprite_actual[4] >= bloque[1] and
                self.y < bloque[1] + BLOQUE_SPRITE[4]):
                if self.velocidad_y < 0:
                    self.y = bloque[1] - self.sprite_actual[4]
                    self.velocidad_y = 0
    def cambiar_direccion(self):
        # Invertir la dirección de la tortuga
        if self.tiempo_bloqueo == 0:
            self.direccion *= -1
            self.estado()
            # Cambiar el sprite activo según la dirección
            if self.direccion == 1:
                if self.levantado==1:
                    self.sprite_actual=tortuga_sprite_2_derecha
                else:
                    self.sprite_actual = self.sprite_derecha
            if self.direccion == -1:
                if self.levantado == 1:
                    self.sprite_actual=tortuga_sprite_2_izquierda
                else:
                    self.sprite_actual = self.sprite_izquierda
            self.tiempo_bloqueo = self.TIEMPO_BLOQUEO_MAXIMO
    def actualizar(self):
        if self.tiempo_bloqueo > 0:
            self.tiempo_bloqueo -= 1
    def aumentar_velocidad(self):
        #funcion para aumentar la velocidad en el eje x , esta funcion es
        # llamada cuando el enemigo se levanta
        self.velocidad_x+=0.2
    def estado(self):
        self.levantado=1
    def actualizar_posicion(self):
        #funcion para actualizar la posicion del enemigo cuando este se sale
        # de los limites
        self.x += self.velocidad_x * self.direccion
        if self.x > 288:
            self.x = 0
        if self.x < 0:
            self.x = 288
        if self.x > 235 and self.y >160:
            self.x=40
            self.y=30
        if self.x > 240 and self.y <60:
            self.x=37
            self.y=45
        if self.x < 30 and self.y <60:
            self.x=238
            self.y=30
        if self.x < 37 and self.y >160:
            self.x=238
            self.y=30
        if self.direccion == 1:
            self.sprite_actual = tortuga_sprite  # Sprite para la dirección hacia la derecha
        else:
            self.sprite_actual = tortuga_sprite_izquierda  # Sprite para la dirección hacia la izquierda
class Mosca:
    def __init__(self, x: int, y: int ,direccion:int):
        self.x = x
        self.y = y
        self.tiempo_bloqueo = 0
        self.TIEMPO_BLOQUEO_MAXIMO = 50
        self.sprite_derecha = MOSCA_SPRITE
        self.sprite_izquierda = MOSCA_SPRITE
        self.sprite_actual = self.sprite_derecha
        self.tumbado_mosca = False
        self.tiempo_tumbado = 0
        self.TIEMPO_MAX_TUMBADO = 150
        self.direccion= direccion
        self.velocidad_x = 1
        self.levantado=0
        self.muerta = False  # Variable para determinar si la tortuga está muerta
        self.GRAVEDAD = 0.3  # Reducir la fuerza de la gravedad
        self.velocidad_y = 0  # Ajustar la velocidad vertical
        self.timer_salto = 0.2
    def aplicar_gravedad(self, suelo: int):
        self.y -= self.velocidad_y
        self.velocidad_y -= self.GRAVEDAD
        # Limitar la velocidad de caída para que se mantenga más tiempo en el aire
        if self.velocidad_y < -0.7:  # Puedes ajustar este límite según sea
            # necesario
            self.velocidad_y = -0.7
        # Restringir el límite inferior para evitar que la mosca atraviese el suelo
        if self.y >= suelo:
            self.y = suelo
            self.velocidad_y = 0
    def estado(self):
        self.levantado=1
    def saltar(self):
        # Generar una fuerza hacia arriba para simular el salto
        if self.velocidad_y==0:
            self.velocidad_y = 5
    def colision_con_bloques(self, bloques):
        for bloque in bloques:
            if bloque[1]!=20:
                if (self.x < bloque[0] + BLOQUE_SPRITE[3]-4 and
                    self.x + self.sprite_actual[3]-4 > bloque[0] and
                    self.y + self.sprite_actual[4] >= bloque[1] and
                    self.y < bloque[1] + BLOQUE_SPRITE[4]):
                    if self.velocidad_y < 0:
                        self.y = bloque[1] - self.sprite_actual[4]
                        self.velocidad_y = 0
                    elif self.velocidad_y > 0:
                        self.y = bloque[1] + BLOQUE_SPRITE[4]
                        self.velocidad_y = 0
    def cambiar_direccion(self):
        # Invertir la dirección de la tortuga
        if self.tiempo_bloqueo == 0:
            self.direccion *= -1
            # Cambiar el sprite activo según la dirección
            if self.direccion == 1:
                self.sprite_actual = self.sprite_derecha
            else:
                self.sprite_actual = self.sprite_izquierda
            self.tiempo_bloqueo = self.TIEMPO_BLOQUEO_MAXIMO
    def actualizar(self):
        if self.tiempo_bloqueo > 0:
            self.tiempo_bloqueo -= 1
    def aumentar_velocidad(self):
        self.velocidad_x+=0.2
    def actualizar_posicion(self):
        # Actualizar la posición horizontal de la tortuga
        self.x += self.velocidad_x * self.direccion
        if self.x > 288:
            self.x = 0
        if self.x < 0:
            self.x = 288
        if self.x > 235 and self.y >160:
            self.x=20
            self.y=30
        if self.x > 240 and self.y <60:
            self.x=37
            self.y=45
        if self.x < 37 and self.y >160:
            self.x=238
            self.y=30
        if self.x < 3 and self.y <60:
            self.x=238
            self.y=30
        self.timer_salto -= 1
        if self.timer_salto <= 0:
            self.saltar()
            self.timer_salto = 35
        self.aplicar_gravedad(202)
        if self.direccion == 1:
            self.sprite_actual = MOSCA_SPRITE
        else:
            self.sprite_actual = MOSCA_SPRITE
class Cangrejo:
    def __init__(self, x: int, y: int, direccion: int):
        self.x = x
        self.y = y
        self.tiempo_bloqueo = 0
        self.TIEMPO_BLOQUEO_MAXIMO = 50
        self.sprite_derecha = CANGREJO_SPRITE
        self.sprite_izquierda = CANGREJO_SPRITE
        self.sprite_actual = self.sprite_derecha
        self.tumbado_cangrejo = False
        self.tiempo_tumbado = 0
        self.TIEMPO_MAX_TUMBADO=150
        self.direccion = direccion
        self.velocidad_x = 1
        self.muerta = False
        self.levantado=0
        self.GRAVEDAD = 0.8
        self.golpes_recibidos = 0
        self.velocidad_y = 0
        self.golpes_recibidos = 0
    def aplicar_gravedad(self, suelo: int):
        # Aplicar la lógica de la gravedad a la tortuga
        self.y -= self.velocidad_y
        self.velocidad_y -= self.GRAVEDAD
        if self.y >= suelo:
            self.y = suelo
            self.velocidad_y = 0
    def estado(self):
        self.levantado=1
    def colision_con_bloques(self, bloques):
        for bloque in bloques:
            if (self.x < bloque[0] + BLOQUE_SPRITE[3] - 4 and
                self.x + self.sprite_actual[3] - 4 > bloque[0] and
                self.y + self.sprite_actual[4] >= bloque[1] and
                self.y < bloque[1] + BLOQUE_SPRITE[4]):
                if self.velocidad_y < 0:
                    self.y = bloque[1] - self.sprite_actual[4]
                    self.velocidad_y = 0
    def cambiar_direccion(self):
        # Invertir la dirección de la tortuga
        if self.tiempo_bloqueo == 0:
            self.direccion *= -1
            # Cambiar el sprite activo según la dirección
            if self.direccion == 1:
                self.sprite_actual = self.sprite_derecha
            else:
                self.sprite_actual = self.sprite_izquierda
            self.tiempo_bloqueo = self.TIEMPO_BLOQUEO_MAXIMO
    def aumentar_velocidad(self):
        self.velocidad_x+=0.2
    def actualizar(self):
        if self.tiempo_bloqueo > 0:
            self.tiempo_bloqueo -= 1
    def actualizar_posicion(self):
        # Actualizar la posición horizontal de la tortuga
        self.x += self.velocidad_x * self.direccion
        if self.x > 288:
            self.x = 0
        if self.x < 0:
            self.x = 288
        if self.x > 235 and self.y > 160:
            self.x = 20
            self.y = 30
        if self.x > 240 and self.y < 60:
            self.x = 37
            self.y = 45
        if self.x < 37 and self.y > 160:
            self.x = 238
            self.y = 30
        if self.x < 3 and self.y < 60:
            self.x = 238
            self.y = 30
        if self.direccion == 1:
            self.sprite_actual = CANGREJO_SPRITE  # Sprite para la dirección hacia la
        else:
            self.sprite_actual = CANGREJO_SPRITE
class Mario_portada:
    def __init__(self):
        self.x = 0
        self.y = 150
        self.velocidad = 3
    def actualizar(self):
        self.x += self.velocidad
        if self.x >260:
            self.x = 0  # Posición inicial
    def draw(self):
        # Dibujar a Mario
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
class Moneda:
    def __init__(self, x: int, y: int ,direccion:int):
        self.x = x
        self.y = y
        self.direccion= direccion
        self.velocidad_x = 0
        self.GRAVEDAD = 0.8
        self.velocidad_y = 0
        self.tiempo_bloqueo=0
    def aplicar_gravedad(self, suelo: int):
        # Aplicar la lógica de la gravedad a la tortuga
        self.y -= self.velocidad_y
        self.velocidad_y -= self.GRAVEDAD
        if self.y >= suelo :
            self.y = suelo
            self.velocidad_y = 0
    def actualizar(self):
        if self.tiempo_bloqueo > 0:
            self.tiempo_bloqueo -= 1
    def colision_con_bloques(self, bloques):
        for bloque in bloques:
            if (
                    self.x < bloque[0] + BLOQUE_SPRITE[3]-4 and
                    self.x + MONEDA_SPRITE[3]-4 > bloque[0] and
                    self.y + MONEDA_SPRITE[4] >= bloque[1] and
                    self.y < bloque[1] + BLOQUE_SPRITE[4]
            ):
                if self.velocidad_y < 0:
                    self.y = bloque[1] - MONEDA_SPRITE[4]
                    self.velocidad_y = 0
    def actualizar_posicion(self):
        # Actualizar la posición horizontal de la tortuga
        self.velocidad_x=1
        self.x += self.velocidad_x * self.direccion
        if self.x > 288:
            self.x = 0
        if self.x < 0:
            self.x = 288
        if self.x > 235 and self.y >160:
            self.x=40
            self.y=30
        if self.x < 37 and self.y >160:
            self.x=238
            self.y=30
