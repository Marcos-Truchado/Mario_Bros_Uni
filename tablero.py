from clases import Mario
from clases import Tortuga
from clases import Mosca
from clases import Cangrejo
from clases import Mario_portada
from clases import Moneda
import random
import pyxel
from sprites import (BLOQUE_SPRITE,TUBERIA_SPRITE, TUBERIA_SPRITE2,salida_sprite,
                    LADRILLO_SPRITE,tortuga_sprite_2_derecha, tortuga_sprite_2_izquierda,
                    tortuga_sprite_tumbada, MOSCA_SPRITE_2,MOSCA_SPRITE_TUMBADA, CANGREJO_SPRITE_2,
                    CANGREJO_SPRITE_TUMBADO,POW_SPRITE, MONEDA_SPRITE, BLOQUE2_SPRITE, BLOQUE3_SPRITE)
class Tablero:
    """Esta clase contiene la información necesaria para representar el tablero"""

    def __init__(self, ancho: int, alto: int):
        # Inicializamos el objeto
        self.ancho = ancho  # Ancho del tablero
        self.alto = alto  # Alto del tablero
        self.camina = True  # Variable para controlar si mario camina tras morir
        self.jugando = False  # Estado del juego
        self.golpes_cangrejo = 0  # Contador de golpes en cangrejos
        self.ULTIMA_DIRECCION = 1  # Última dirección del movimiento
        self.contador_teclas = 0  # Contador de teclas presionadas
        self.fase = 1  # Fase inicial del juego
        self.__tortugas_eliminadas = []  # Lista de tortugas eliminadas
        self.__cangrejos_eliminados = []  # Lista de cangrejos eliminados
        self.__moscas_eliminadas = []  # Lista de moscas eliminadas
        self.__monedas = []  # Lista de monedas
        self.__monedas_eliminadas = []  # Lista de monedas eliminadas
        self.__tortugas = []  # Lista de tortugas presentes
        self.__tortugas_tumbadas = []  # Lista de tortugas tumbadas
        self.__tortugas_izquierda = []  # Lista de tortugas moviéndose a la izquierda
        self.__tortugas_derecha = []  # Lista de tortugas moviéndose a la derecha
        self.__cangrejos = []  # Lista de cangrejos presentes
        self.__cangrejos_tumbados = []  # Lista de cangrejos tumbados
        self.__cangrejos_izquierda = []  # Lista de cangrejos moviéndose a la izquierda
        self.__cangrejos_derecha = []  # Lista de cangrejos moviéndose a la derecha
        self.__moscas = []  # Lista de moscas presentes
        self.__moscas_tumbadas = []  # Lista de moscas tumbadas
        self.__moscas_izquierda = []  # Lista de moscas moviéndose a la izquierda
        self.__moscas_derecha = []  # Lista de moscas moviéndose a la derecha
        self.tiempo_tumbado_tortuga = 0  # Tiempo de tumbado de tortuga
        self.tiempo_tumbado_mosca = 0  # Tiempo de tumbado de mosca
        self.tiempo_tumbado_cangrejo = 0  # Tiempo de tumbado de cangrejo
        self.tiempo_aparicion = 0  # contador para medir el tiempo de
        # aparicion de los enemigos
        self.tiempo_intervalo = 200  # Intervalo de tiempo con el que
        # aparecen los enemigos
        self.TIEMPO_TUMBADO_MAXIMO = 200  # Tiempo max de tumbado de los enemigos
        self.tiempo_desaparicion = 200  # Tiempo de desaparición de la
        # plataforma
        self.tiempo_plataforma = 0  # contador para medir el tiempo que se
        # pasaen la plataforma post-muerte
        self.tiempo_intervalo_moneda = 220  # Intervalo de tiempo para monedas
        self.aparicion_moneda = 0  # Tiempo de aparición de moneda
        self.__eliminados = []  # Lista de enemigos eliminados
        self.__enemigos_tortugas_levantados = []  # Lista de tortugas levantadas
        self.__enemigos_cangrejos_levantados = []  # Lista de cangrejos levantados
        self.__enemigos_moscas_levantados = []  # Lista de moscas levantadas
        self.mario_portada = Mario_portada()  # Instancia de Mario en la portada
        self.usos_pow = 0  # Contador de usos de POW
        # Diferentes bloques usados
        self.bloques = [
            *[(x, 150) for x in range(0, 95)],
            *[(x, 118) for x in range(0, 40)],
            *[(x, 92) for x in range(64, 215)],
            *[(x, 150) for x in range(185, 285)],
            *[(x, 118) for x in range(245, 285)],
            *[(x, 45) for x in range(0, 100)],
            *[(x, 45) for x in range(170, 285)],
            *[(x,20) for x in range(130,140)]]
        self.tuberias=[
            *[(x, 172) for x in range(0, 20)],
            *[(x, 15) for x in range(0, 20)],]
        self.salida=[
            *[(245, 172)],
            *[(245, 15)],]
        self.tuberias2 = [
            *[(x, 172) for x in range(250, 285)],
            *[(x, 15) for x in range(250, 285)],]
        self.ladrillos = [
            *[(x, 202) for x in range(0, 285)],
            *[(x, 210) for x in range(0, 285)],]
        self.pow = [(x, 143) for x in range(139, 140)]
        # creamos titulo
        pyxel.init(self.ancho, self.alto+8, title="Mario Bros")
        # Cargamos el fichero pyxres que vamos a usar
        pyxel.load("assets/mario.pyxres")
        # Creamos a Mario en la mitad de la pantalla en x e y = 200
        # Lo ponemos como privado para que solo el tablero pueda verlo y cambiarlo
        self.__mario = Mario(self.ancho /2, 200)
        # Ejecutamos el juego
        pyxel.run(self.update, self.draw)
    # defino el atributo ancho como propiedad
    @property
    def ancho(self) -> int:
        """ Este es el método que se va a usar para leer el valor
        del atributo"""
        # Aquí debo devolver el valor del atributo como si fuera
        # privado
        return self.__ancho
    # defino el atributo alto como propiedad
    @property
    def alto(self) -> int:
        return self.__alto

    @ancho.setter
    def ancho(self, ancho:int):
        if ancho > 0:
            self.__ancho = ancho
        else:
            self.__ancho = 285
    @alto.setter
    def alto(self, alto:int):
        if alto > 0:
            self.__alto = alto
        else:
            self.__alto = 200
    def crear_moneda(self):
        if len(self.__monedas) < 30:
            self.posicion_moneda = random.randint(0, 1)
            if self.posicion_moneda==0:
                pos_moneda=(40, 30)
                direccion_moneda = 1
                nueva_moneda = Moneda(pos_moneda[0], pos_moneda[1],direccion_moneda)
                self.__monedas.append(nueva_moneda)
            if self.posicion_moneda==1:
                pos_moneda=(238, 30)
                direccion_moneda = -1
                nueva_moneda = Moneda(pos_moneda[0], pos_moneda[1],direccion_moneda)
                self.__monedas.append(nueva_moneda)
    def crear_tortuga(self):
        if len(self.__tortugas) < 30:
            self.posicion_tortuga = random.randint(0, 1)
            if self.posicion_tortuga==0:
                pos_tortuga=(40, 30)
                direccion_tortuga = 1
                nueva_tortuga = Tortuga(pos_tortuga[0], pos_tortuga[1],direccion_tortuga)
                self.__tortugas.append(nueva_tortuga)
                self.__tortugas_derecha.append(nueva_tortuga)
            if self.posicion_tortuga==1:
                pos_tortuga=(238, 30)
                direccion_tortuga = -1
                nueva_tortuga = Tortuga(pos_tortuga[0], pos_tortuga[1],direccion_tortuga)
                self.__tortugas.append(nueva_tortuga)
                self.__tortugas_izquierda.append(nueva_tortuga)
    def crear_cangrejos(self):
        if len(self.__cangrejos) < 30:
            self.posicion_cangrejo = random.randint(0, 1)
            if self.posicion_cangrejo==0:
                pos_cangrejo=(40, 30)
                direccion_cangrejo = 1
                nuevo_cangrejo = Cangrejo(pos_cangrejo[0], pos_cangrejo[1],direccion_cangrejo)
                self.__cangrejos.append(nuevo_cangrejo)
                self.__cangrejos_derecha.append(nuevo_cangrejo)
            if self.posicion_cangrejo==1:
                pos_cangrejo=(238, 30)
                direccion_cangrejo = -1
                nuevo_cangrejo = Cangrejo(pos_cangrejo[0], pos_cangrejo[1],direccion_cangrejo)
                self.__cangrejos.append(nuevo_cangrejo)
                self.__cangrejos_izquierda.append(nuevo_cangrejo)
    def crear_mosca(self):
        if len(self.__moscas)< 30:
            self.posicion_mosca = random.randint(0, 1)
            if self.posicion_mosca==0:
                pos_mosca=(40, 30)
                direccion_mosca = 1
                nueva_mosca = Mosca(pos_mosca[0], pos_mosca[1],direccion_mosca)
                self.__moscas.append(nueva_mosca)
                self.__moscas_derecha.append(nueva_mosca)
            if self.posicion_mosca==1:
                pos_mosca=(238, 30)
                direccion_mosca = -1
                nueva_mosca = Mosca(pos_mosca[0], pos_mosca[1],direccion_mosca)
                self.__moscas.append(nueva_mosca)
                self.__moscas_izquierda.append(nueva_mosca)

    def update(self):
        # Si el usuario presiona la tecla A inicia el juego
        if pyxel.btnp(pyxel.KEY_A):
            if not self.jugando:
                self.jugando = True
                self.fase = 1
            else:
                self.jugando = False
                self.fase = 0

        # Si se presiona la tecla C se sale del juego
        if pyxel.btnp(pyxel.KEY_C):
            if not self.jugando:
                pyxel.quit()
        # Cargamos la portada inicial pre-juego
        if not self.jugando:
            self.mario_portada.actualizar()

        # Lógica y actualizacion del juego cuando se está jugando , incluimos :
        # el estado de los enemigos(tumbados,eliminados,levantados...),
        # las vidas de mario,el uso del pow,el cambio de fase, tumbar enemigos ,
        # cambio de direccion en enemigos y el spawneo de enemigos
        if self.jugando:

            self.estado_enemigos()
            self.mario_vidas()
            self.pow_usados()
            self.cambio_de_fase()
            self.tumbar_enemigos()
            self.direccion_enemigos()
            self.spawneo()

            # Salir del juego al presionar la tecla Q
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

            # Actualización de la posición de Mario y gravedad aplicada a él
            self.actualizar_posicion_mario()
            self.__mario.aplicar_gravedad(self.alto - 8)

            # Lógica para las monedas
            for moneda in self.__monedas:
                if moneda not in self.__monedas_eliminadas:
                    # Aplicar gravedad, colisión con bloques y actualización
                    # de moneda igual que con mario y enemigos
                    moneda.aplicar_gravedad(self.alto - 24)
                    moneda.colision_con_bloques(self.bloques)
                    moneda.actualizar()
                    moneda.actualizar_posicion()

            # Colisión de Mario con las monedas , en caso de colisionar esta
            # se agrega a una lista que serivira para contabilizar las
            # monedas recogidas y la puntuacion
            for moneda in self.__monedas:
                if moneda not in self.__monedas_eliminadas:
                    if (self.__mario.x + self.__mario.sprite[3] > moneda.x and
                            self.__mario.x < moneda.x + MONEDA_SPRITE[3] and
                            self.__mario.y + self.__mario.sprite[
                                4] > moneda.y and
                            self.__mario.y < moneda.y + MONEDA_SPRITE[4]):
                        # Agregar moneda eliminada y actualizar cantidad de monedas de Mario
                        self.__monedas_eliminadas.append(moneda)
                        self.__mario.ganar_monedas()
    def spawneo(self):
        # Fase 1: Tortugas y monedas
        if self.fase == 1 and len(self.__tortugas) < 30:
            #creamos la primera tortuga , esta tortuga no necesita esperar
            # el intervalo para ser creada
            if len(self.__tortugas) == 0:
                self.crear_tortuga()
            else:
                # controlamos la aparicion de las tortugas
                self.tiempo_aparicion += 1
                self.aparicion_moneda += 1
                # Crea una tortuga si se alcanza el intervalo de tiempo
                if self.tiempo_aparicion >= self.tiempo_intervalo:
                    self.tiempo_aparicion = 0
                    self.crear_tortuga()
                # Crea una moneda si se alcanza el intervalo de tiempo para monedas
                if (self.aparicion_moneda >= self.tiempo_intervalo_moneda
                        and len(self.__monedas) < 10):
                    self.aparicion_moneda = 0
                    self.crear_moneda()
        # Fase 2: Cangrejos y monedas
        if self.fase == 2 and len(self.__cangrejos) < 30:
            # creamos el prime cangrejo , este cangrejo no necesita esperar
            # el intervalo para ser creado
            if len(self.__cangrejos) == 0:
                self.crear_cangrejos()
            else:
                # Controla la aparición de cangrejos en intervalos de tiempo
                self.tiempo_aparicion += 1
                # Crea un cangrejo si se alcanza el intervalo de tiempo
                if self.tiempo_aparicion >= self.tiempo_intervalo:
                    self.tiempo_aparicion = 0
                    self.crear_cangrejos()
                # Crea una moneda si se alcanza el intervalo de tiempo para monedas
                if (self.aparicion_moneda >= self.tiempo_intervalo_moneda
                        and len(self.__monedas) < 20):
                    self.crear_moneda()
                    self.aparicion_moneda = 0
        # Fase 3: Moscas y monedas
        if self.fase == 3 and len(self.__moscas) < 30:
            #creamos la primera mosca, esta mosca no necesita esperar
            # el intervalo para ser creada
            if len(self.__moscas) == 0:
                self.crear_mosca()
            else:
                # Controla la aparición de moscas en intervalos de tiempo
                self.tiempo_aparicion += 1
                # Crea una mosca si se alcanza el intervalo de tiempo
                if self.tiempo_aparicion >= self.tiempo_intervalo:
                    self.tiempo_aparicion = 0
                    self.crear_mosca()
                # Crea una moneda si se alcanza el intervalo de tiempo para monedas
                if (self.aparicion_moneda >= self.tiempo_intervalo_moneda
                        and len(self.__monedas) < 30):
                    self.crear_moneda()
                    self.aparicion_moneda = 0
    def direccion_enemigos(self): #funvion para cambiar la direccion de un
        # enemigo tras un chcoque , comenzamos iterando las listas de los
        # enemigos y enemigos tumbados , añadimos un valor 10 para que el
        # cambio de direccion tambien valga cuando un enemigo caiga encima
        # de otro
        enemies1 = [(self.__tortugas, self.__eliminados,
                    self.__tortugas_tumbadas,
                     self.__enemigos_tortugas_levantados, 10),
                    (self.__cangrejos, self.__eliminados,
                    self.__cangrejos_tumbados,
                     self.__enemigos_cangrejos_levantados,10),
                    (self.__moscas, self.__eliminados, self.__moscas_tumbadas,
                    self.__enemigos_moscas_levantados, 10)]
        for enemigos, eliminados, enemigos_tumbados, enemigos_levantados, valor in enemies1:
            # Lógica de colisión entre todos los enemigos
            for enemigo1 in enemigos:
                for enemigo2 in enemigos:
                    if (enemigo1 != enemigo2 and
                            enemigo1 not in eliminados and
                            enemigo2 not in eliminados):
                        # nos aseguramos de que las posiciones en el eje x
                        # cumplen los requisitos
                        if (enemigo1.x < enemigo2.x and
                            enemigo2.x < enemigo1.x + valor and
                            abs(enemigo1.y - enemigo2.y) <= 5):
                            enemigo1.cambiar_direccion()
                            #llamamos a la funcion cambiar direccion ,
                            # presente en la clase de los enemigos
                            enemigo2.cambiar_direccion()
    def estado_enemigos(self):
        #comprobamos el estado de los enemigos , aqui comprobamos que esten
        # tumbados ,levantados o en su estado inicial , hacemos que las
        # diferentes funciones se apliquen en los diversos casos ,
        # comenzamos iterando las listas de los enemigos y las de sus estados
        enemies3 = [(self.__tortugas, self.__tortugas_tumbadas,
                    self.__enemigos_tortugas_levantados),
                    (self.__cangrejos, self.__cangrejos_tumbados,
                    self.__enemigos_cangrejos_levantados),
                    (self.__moscas, self.__moscas_tumbadas,
                    self.__enemigos_moscas_levantados)]
        for enemigos, enemigos_tumbados, enemigos_levantados in enemies3:
            #comenzamos asegurandonos de que la gravedad , las colisiones y
            # la actualicion decposiciones se aplique en los casos
            # correspondientes , en este caso , que este en su estado
            # original o que esten levantados
            for enemigo in enemigos:
                if enemigo not in self.__eliminados:
                    enemigo.aplicar_gravedad(self.alto - 24)
                    enemigo.colision_con_bloques(self.bloques)
                    enemigo.actualizar()
                if enemigo not in enemigos_tumbados and enemigo not in self.__eliminados:
                    enemigo.actualizar_posicion()
            # proceso para borrar a un enemigo de la lista de enemigos
            # tumbados y añadirle a su correspondiente lista de enemigos
            # levantados , en este caso usaremos los indices
            i = 0
            while i < len(enemigos_tumbados):
                enemigo_tumbado = enemigos_tumbados[i]
                enemigo_tumbado.aplicar_gravedad(self.alto - 24)
                enemigo_tumbado.colision_con_bloques(self.bloques)
                enemigo_tumbado.actualizar()
                enemigo_tumbado.tiempo_tumbado += 1
                if enemigo_tumbado.tiempo_tumbado >= enemigo_tumbado.TIEMPO_MAX_TUMBADO:
                    # proceso para que un enemigo se levante , en caso de
                    # que e, tiempo que lleva tumbado sea igual o mayor al
                    # tiempo predefinido
                    enemigo_tumbado.tiempo_tumbado = 0
                    enemigo_tumbado.tumbado = False
                    enemigos_tumbados.remove(enemigo_tumbado)
                    enemigos_levantados.append(enemigo_tumbado)
                    # aumentamos la velocidad del enemigo y llamamos a las
                    # diferentes funciones que necesita emn enemigo en su
                    # estado levantado
                    for enemigo in enemigos_levantados:
                        enemigo.aumentar_velocidad()
                        enemigo.estado()
                        enemigo.cambiar_direccion()  # Cambiar dirección de enemigos levantados
                else:
                    i += 1
    def mario_vidas(self):
        #funcion para que mario pierda vidas , en caso de tocar a un enemigo
        enemies2 = [
            (self.__tortugas, self.__eliminados, self.__tortugas_tumbadas),
            (self.__cangrejos, self.__eliminados, self.__cangrejos_tumbados),
            (self.__moscas, self.__eliminados, self.__moscas_tumbadas)]
        #iteramos todos los enemigos y en todos sus estados
        for enemigos, eliminados, enemigos_tumbados in (enemies2):
            for enemigo in enemigos:
                if (enemigo not in enemigos_tumbados and enemigo not
                    in eliminados and self.__mario.x +
                    self.__mario.sprite[3] > enemigo.x and
                    self.__mario.x < enemigo.x + enemigo.sprite_actual[3]
                    and self.__mario.y + self.__mario.sprite[4] > enemigo.y
                    and self.__mario.y < enemigo.y + enemigo.sprite_actual[4]):
                    # en caso de cumplirse las condiviones ,llamamos a la
                    # funcion perder vida en la clase mario
                    self.__mario.perder_vida()
                    # una vez mario pierde vida cambiamos la varible
                    # self.camina a false parq ue mario se pose sobre la
                    # plataforma y esta no desaparezca
                    self.camina = False
    def cambio_de_fase(self):
        #funcion para cambiar de fase , su funcioamiento se basa en en
        # comprobar que la longitud de la lista enemigos eliminados aumente
        # en 30 por ase cambiada
        enemigos_tumbados = [
            (self.__tortugas_tumbadas, self.__tortugas_eliminadas, 8),
            (self.__cangrejos_tumbados, self.__cangrejos_eliminados, 8),
            (self.__moscas_tumbadas, self.__moscas_eliminadas, 8)]
        for enemigos, _, cantidad_objetivo in enemigos_tumbados:
            for i, enemigo_tumbado in enumerate(enemigos):
                if (self.__mario.x < enemigo_tumbado.x + 16 and
                    enemigo_tumbado.x < self.__mario.x + 16 and
                    self.__mario.y < enemigo_tumbado.y + 16 and
                    enemigo_tumbado.y < self.__mario.y + 16):
                    if enemigo_tumbado not in self.__eliminados:
                        enemigo_tumbado.y = 200
                        self.__eliminados.append(enemigo_tumbado)
                        if len(self.__eliminados) >= 30 and len(
                                self.__eliminados) < 60:
                            self.fase = 2
                        if len(self.__eliminados) >= 60 and len(
                                self.__eliminados) < 90:
                            self.fase = 3
                        if (len(self.__eliminados) >= 90):
                            pyxel.quit()
                        #cuando la longitud de la lista de enemigos
                        # eliminados llegue a 90 acbamos el juego
    def actualizar_posicion_mario(self):
        #funcion para actualizar la posicion de mario , en ella se controla
        # el movimiento lateral y vertical
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.__mario.realizar_salto('up')
        # en este fragmento asumimos que cuando self.camina =False mario ha
        # muerto por tanto esta sobre la plataforma la plataforma , cuando
        # mario esta en la plataforma iniciamos un contador de pasos ,
        # por cada paso seguido que de se sumara 1 , si mario deja de
        # moverse el cotador vuelve a 0 , una vez el contador llegue al
        # maximo definido la plataforma desaparecera del mapa a demas no
        # tendra efecto a la hora de aplicar las coliciones con bloques ,
        # es por ello que solo iteramos los bloques de self.bloques cuya
        # coordenada en el eje y es 20
        if self.camina==False:
            for bloque in self.__mario.bloques:
                if bloque[1]==20:
                    if (self.__mario.x < bloque[0] + BLOQUE_SPRITE[3] and
                        self.__mario.x + self.__mario.sprite[3] > bloque[0] and
                        self.__mario.y + self.__mario.sprite[4] >= bloque[1] and
                        self.__mario.y < bloque[1] + BLOQUE_SPRITE[4]):
                        if self.__mario.velocidad_y < 0:
                            self.__mario.y = bloque[1] - self.__mario.sprite[4]
                            self.__mario.velocidad_y = 0
                            self.__mario.salto = False
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.__mario.mover('derecha', self.ancho)
            self.contador_teclas += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.__mario.mover('izquierda', self.ancho)
            self.contador_teclas += 1
        else:
            self.contador_teclas = 0  # Reinicia el contador si no se presiona ninguna tecla
        if self.contador_teclas >= 25:
            self.camina = True
    def pow_usados(self):
        #funcion para controlar el funcionamiento de pow , cuyo uso esta
        # limitado a tres veces , el funcionamiento para tumbar a los
        # enemigos es igual que la parte dedicada e ello en la funcion
        # def tumbar_enemigos, con la diferencia de que la condicion if que
        # exige que mario tenga la mimsa posicion x y la misma posion y (menos la
        # altura del bloque) se elimina , por tanto con tocar el bloques
        # bastaria para tumbar a un enemigo y añadirlo a la lista
        # correspondiente , hay que recordar que el pow solo funcion para
        # enemgios que toquen una plataforma , aquellos que esten saltando o
        # bajo el efecto de la gravedad no seran afectados por el pow
        if self.usos_pow < 3:
            for pow in self.__mario.pow:
                if (self.__mario.x < pow[0]  and
                        self.__mario.x + self.__mario.sprite[3] > pow[0] and
                        self.__mario.y + self.__mario.sprite[4] >= pow[1] and
                        self.__mario.y < pow[1] + POW_SPRITE[4]):
                    if self.__mario.velocidad_y > 0:
                        self.__mario.y = pow[1] + self.__mario.sprite[4]
                        self.__mario.velocidad_y = 0
                        self.usos_pow += 1
                        for i, tortuga in enumerate(self.__tortugas):
                            self.__tortugas[i].tumbado_tortuga = True
                            self.__tortugas[i].tumbado_por_pow = True
                            self.__tortugas_tumbadas.append(self.__tortugas[i])
                        # Tumbar moscas si chocan con el POW
                        for i, mosca in enumerate(self.__moscas):
                            self.__moscas[i].tumbado_mosca = True
                            self.__moscas[i].tumbado_por_pow = True
                            self.__moscas_tumbadas.append(self.__moscas[i])
                        # Tumbar cangrejos si chocan con el POW
                        for i,cangrejo in enumerate(self.__cangrejos):
                            self.__cangrejos[i].tumbado_cangrejo = True
                            self.__cangrejos[i].tumbado_por_pow = True
                            self.__cangrejos_tumbados.append(self.__cangrejos[i])
    def tumbar_enemigos(self):
        # funcion para tumbar enemigos . FUNCIONAMIENTO (importante) solo
        # funciona para bloques cuya coordenada en el eje y sea diferente a
        # 20 , el funcionamiento consiste en : la diferencia entre
        # coordenadas en el ejex del enemigo y mario debe ser menor / igual
        # a 10 , esto para por que hacer la coordenada sea exactamente igual
        # es complicado , por tanto ponemos un margen de 10 bloques ,
        # la coordenada en el eje y de mario debe ser igual a la del enemigo
        # restando la altura del enemigo al enemgigo y restando la altura
        # del bloque.
        for bloque in self.__mario.bloques:
            if bloque[1]!=20:
                if (self.__mario.x < bloque[0] + BLOQUE_SPRITE[3] and
                    self.__mario.x + self.__mario.sprite[3] > bloque[0] and
                    self.__mario.y + self.__mario.sprite[4] >= bloque[1] and
                    self.__mario.y < bloque[1] + BLOQUE_SPRITE[4]):
                    if self.__mario.velocidad_y < 0:
                        # Si Mario aterriza sobre un bloque su posicion y de
                        # modifica al bloque , sabemos que aterriza debido a
                        # que su velocidad en eje y es negativa
                        self.__mario.y = bloque[1] - self.__mario.sprite[4]
                        self.__mario.velocidad_y = 0
                        self.__mario.salto = False
                    elif self.__mario.velocidad_y > 0:
                        # Si Mario colisiona desde abajo mientras salta,
                        # ajusta su posición , sabemos que choca porque su
                        # velocidad en el eje y es positiva
                        self.__mario.y = bloque[1] + self.__mario.sprite[4]
                        self.__mario.velocidad_y = 0
                        for i, tortuga in enumerate(self.__tortugas):
                            if (abs(self.__mario.x - tortuga.x) <= 10 and
                                self.__mario.y - tortuga.y ==self.__mario.sprite[4]
                                +tortuga.sprite_actual[4]):
                                self.__tortugas[i].tumbado_tortuga = True
                                tortuga.tumbado_tortuga = True
                                self.__tortugas_tumbadas.append(self.__tortugas[i])
                        for i, mosca in enumerate(self.__moscas):
                            if (abs(self.__mario.x - mosca.x) <= 10 and
                                self.__mario.y - mosca.y ==
                                self.__mario.sprite[4] +
                                mosca.sprite_actual[4]):
                                self.__moscas[i].tumbado_mosca = True
                                mosca.tumbado_mosca = True
                                self.__moscas_tumbadas.append(self.__moscas[i])
                        for cangrejo in self.__cangrejos:
                            if (abs(self.__mario.x - cangrejo.x) <= 10 and
                                self.__mario.y - cangrejo.y ==self.__mario.sprite[4]
                                +cangrejo.sprite_actual[4]):
                                cangrejo.golpes_recibidos += 1
                                if cangrejo.golpes_recibidos >= 2:  # Verificar si ha recibido dos golpes
                                    self.__cangrejos_tumbados.append(cangrejo)
                                    cangrejo.golpes_recibidos = 0
    def draw(self):
        """Este código se ejecuta también cada frame, aquí deberías dibujar los objetos."""
        pyxel.cls(0)
        if not self.jugando:
            # Dibujar la pantalla de inicio(portada)
            pyxel.text(125, 70, "MARIO BROS", pyxel.frame_count % 16)
            pyxel.text(105, 100, "Presiona A para jugar", 7)
            pyxel.text(105, 120, "Presiona c para cerrar", 7)
        if not self.jugando:
            self.mario_portada.draw()
        else:
            #dibujamos fases
            if self.fase==1:
                for bloque in self.bloques:
                    if bloque[1] != 20:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE_SPRITE)
            if self.fase==2:
                for bloque in self.bloques:
                    if bloque[1] != 20:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE2_SPRITE)
            if self.fase==3:
                for bloque in self.bloques:
                    if bloque[1] != 20:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE3_SPRITE)
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.ULTIMA_DIRECCION = 1
                pyxel.blt(self.__mario.x, self.__mario.y, *self.__mario.sprite)
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.ULTIMA_DIRECCION = 2
                pyxel.blt(self.__mario.x, self.__mario.y, 2, 0, 0, 16, 16)
            if self.ULTIMA_DIRECCION == 1:
                pyxel.blt(self.__mario.x, self.__mario.y, *self.__mario.sprite)
            elif self.ULTIMA_DIRECCION == 2:
                pyxel.blt(self.__mario.x, self.__mario.y, 2, 0, 0,16, 16)
            if self.camina==False:
                if self.fase==1:
                    for bloque in self.bloques:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE_SPRITE)
                if self.fase==2:
                    for bloque in self.bloques:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE2_SPRITE)
                if self.fase==3:
                    for bloque in self.bloques:
                        pyxel.blt(bloque[0], bloque[1], *BLOQUE3_SPRITE)
            for tuberia in self.tuberias:
                pyxel.blt(tuberia[0], tuberia[1], *TUBERIA_SPRITE)
            for tuberia in self.tuberias2:
                pyxel.blt(tuberia[0], tuberia[1], *TUBERIA_SPRITE2)
            for salida in self.salida:
                pyxel.blt(salida[0], salida[1], *salida_sprite)
            for ladrillo in self.ladrillos:
                pyxel.blt(ladrillo[0], ladrillo[1], *LADRILLO_SPRITE)
            if self.usos_pow<3:
                for pow in self.pow:
                    pyxel.blt(pow[0], pow[1],*POW_SPRITE)
            if self.fase == 1:
                for moneda in self.__monedas:
                    if moneda not in self.__monedas_eliminadas:
                        pyxel.blt(moneda.x, moneda.y, *MONEDA_SPRITE)
                for tortuga in self.__tortugas:
                    if (tortuga not in self.__eliminados and tortuga not in
                            self.__tortugas_tumbadas):
                        if tortuga in self.__enemigos_tortugas_levantados:
                            if tortuga.direccion == 1:
                                pyxel.blt(tortuga.x, tortuga.y,*tortuga_sprite_2_derecha)
                            else:
                                pyxel.blt(tortuga.x, tortuga.y,*tortuga_sprite_2_izquierda)
                        else:
                            pyxel.blt(tortuga.x, tortuga.y,*tortuga.sprite_actual)
                for tortuga in self.__tortugas_tumbadas:
                    if tortuga not in self.__eliminados:
                        pyxel.blt(tortuga.x,tortuga.y+5,*tortuga_sprite_tumbada)
                pyxel.text(135, 120, "FASE 1.", 7)
                pyxel.text(5,5,"Vidas: " + str(self.__mario.vidas), 7)
                pyxel.text(50,5,"puntos: "+str(len(self.__eliminados))+str(self.__mario.monedas),7)
                pyxel.text(100, 5, "Monedas" + str(self.__mario.monedas), 7)
            if self.fase == 2:
                for moneda in self.__monedas:
                    if moneda not in self.__monedas_eliminadas:
                        pyxel.blt(moneda.x, moneda.y, *MONEDA_SPRITE)
                for cangrejo in self.__cangrejos:
                        if (cangrejo not in self.__cangrejos_tumbados and
                                cangrejo not in self.__eliminados):
                            if (cangrejo not in
                                    self.__enemigos_cangrejos_levantados):
                                pyxel.blt(cangrejo.x, cangrejo.y, *cangrejo.sprite_actual)
                            if (cangrejo in
                                    self.__enemigos_cangrejos_levantados):
                                pyxel.blt(cangrejo.x, cangrejo.y,*CANGREJO_SPRITE_2)
                for cangrejo in self.__cangrejos_tumbados:
                    if cangrejo not in self.__eliminados:
                        pyxel.blt(cangrejo.x, cangrejo.y, *CANGREJO_SPRITE_TUMBADO)
                pyxel.text(135, 120, "FASE 2.", 7)
                pyxel.text(5, 5, "Vidas: " + str(self.__mario.vidas), 7)
                pyxel.text(50,5,"puntos: "+str(len(self.__eliminados))+str(self.__mario.monedas),7)
                pyxel.text(100, 5,"Monedas"+ str(self.__mario.monedas), 7)
            if self.fase == 3:
                for moneda in self.__monedas:
                    if moneda not in self.__eliminados:
                        pyxel.blt(moneda.x, moneda.y, *MONEDA_SPRITE)
                for mosca in self.__moscas:
                        if (mosca not in self.__moscas_tumbadas and mosca not in
                                self.__eliminados):
                            if mosca not in self.__enemigos_moscas_levantados:
                                pyxel.blt(mosca.x, mosca.y, *mosca.sprite_actual)
                            if mosca  in self.__enemigos_moscas_levantados:
                                pyxel.blt(mosca.x, mosca.y,*MOSCA_SPRITE_2)
                for mosca in self.__moscas_tumbadas:
                    if mosca not in self.__eliminados:
                        pyxel.blt(mosca.x, mosca.y, *MOSCA_SPRITE_TUMBADA)
                pyxel.text(135, 120, "FASE 3.", 7)
                pyxel.text(5, 5, "Vidas: " + str(self.__mario.vidas), 7)
                pyxel.text(50, 5, "puntos: " + str(len(self.__eliminados))+str(self.__mario.monedas),7)
                pyxel.text(100, 5, "Monedas" + str(self.__mario.monedas), 7)
