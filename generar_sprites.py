"""
Genera los sprites del juego y los guarda en assets/mario.pyxres.

Cada sprite se define como arte ASCII: cada caracter es un color de la
paleta de Pyxel. Se dibujan en los bancos de imagen con pyxel.image().set()
usando exactamente las coordenadas que el juego espera (ver sprites.py)
y se guardan en formato .pyxres con pyxel.save().

Uso:
    .venv/bin/python generar_sprites.py
"""

import sys
import pyxel

# Paleta de Pyxel: cada letra del arte ASCII mapea a un color
# (paleta por defecto: 0 negro, 3 verde oscuro, 4 marron, 6 gris claro,
# 7 blanco, 8 rojo, 9 naranja, 10 amarillo, 11 verde, 12 azul,
# 13 indigo, 14 piel)
PALETA = {
    ".": 0,   # negro (fondo)
    "g": 3,   # verde oscuro
    "N": 4,   # marron
    "k": 5,   # gris oscuro
    "s": 6,   # gris claro
    "W": 7,   # blanco
    "R": 8,   # rojo
    "O": 9,   # naranja
    "Y": 10,  # amarillo
    "V": 11,  # verde
    "B": 12,  # azul
    "I": 13,  # indigo
    "P": 14,  # piel
    "p": 15,  # rosa
}

# Paleta clasica de Pyxel (la que usa el arte): la de Pyxel 2 / PICO-8 estilo
PALETA_CLASICA = [
    0x000000,  # 0 negro
    0x1D2B53,  # 1 azul oscuro
    0x7E2553,  # 2 morado oscuro
    0x008751,  # 3 verde oscuro
    0xAB5236,  # 4 marron
    0x5F574F,  # 5 gris oscuro
    0xC2C3C7,  # 6 gris claro
    0xFFF1E8,  # 7 blanco
    0xFF004D,  # 8 rojo
    0xFFA300,  # 9 naranja
    0xFFEC27,  # 10 amarillo
    0x00E436,  # 11 verde
    0x29ADFF,  # 12 azul
    0x83769C,  # 13 indigo
    0xFF77A8,  # 14 piel/rosa
    0xFFCCAA,  # 15 rosa claro
]


def pintar(img: int, u: int, v: int, filas: list[str]) -> None:
    """Vuelca un conjunto de filas ASCII al banco de imagen."""
    ancho = len(filas[0])
    for fila in filas:
        assert len(fila) == ancho, f"sprite con filas de distinto ancho: {fila!r}"
    datos = ["".join(hex(PALETA[c])[2:] for c in fila) for fila in filas]
    pyxel.images[img].set(u, v, datos)


def espejo(filas: list[str]) -> list[str]:
    """Devuelve el arte espejado horizontalmente."""
    return [fila[::-1] for fila in filas]


# ---------------------------------------------------------------- MARIO ----
# Mario quieto (derecha), 16x16. Tambien usado en la portada (banco 0).
MARIO_QUIETO = [
    "....RRRRRRRR....",  # gorra
    "...RRRRRRRRRR...",
    "...RRRRRRRWWW...",  # brillo de la gorra
    "..RRRRRRRWWWW...",
    "..RRRRRRRRWWRR..",  # pelo lateral
    "..PPPPPPWWWPPP..",  # cara y ojos
    "..PPPPPPPPPPPP..",
    "...PPPPPPPPPP...",
    "...PPPPPPPPPP...",  # barbilla
    "....BBBBBBBB....",  # mono azul
    "..BBBBBBBBBBB...",
    ".BBBBBBBBBBBB...",
    ".BBYBBBBBBBBYB..",  # botones
    "..BBYYBBBBYYB...",
    "..NNNN..NNNN....",  # botas
    "..NNNN..NNNN....",
]

# Paso 1 de caminar (pierna izquierda adelantada)
MARIO_PASO1 = [
    *MARIO_QUIETO[:14],
    "..NNNN..NNN.....",
    "..NNNN...NNN....",
]

# Paso 2 de caminar (pierna derecha adelantada)
MARIO_PASO2 = [
    *MARIO_QUIETO[:14],
    "...NNN..NNNN....",
    "...NNN...NNNN...",
]

# -------------------------------------------------------------- TORTUGA ----
TORTUGA_DERECHA = [
    "..VVVVVV....",   # cabeza
    ".VVVVVVVV...",
    ".VVVVVVVV...",
    "..PPPPPP....",   # cara
    "..PWPPPPW...",   # ojos
    "..VVVVVVVV..",   # caparazon
    ".VVVVVVVVVV.",
    ".VVVVVVVVVV.",
    "VVgVVVVgVV..",
    "VgVVVVVVVg..",
    "VVVVgVVVVV..",
    ".VVVVVVVVVV.",
    "..NNNNNN....",   # pies
    "..NNNNNN....",
    "............",
    "............",
]

TORTUGA_IZQUIERDA = [
    ".VVVVVV....",
    "VVVVVVVV...",
    "VVVVVVVV...",
    ".PPPPPP....",
    ".WPPPPW....",
    ".VVVVVVVV..",
    "VVVVVVVVVV.",
    "VVVVVVVVVV.",
    "VVgVVVVgVV.",
    "VgVVVVVVVg.",
    "VVVVgVVVVV.",
    "VVVVVVVVVV.",
    ".NNNNNN....",
    ".NNNNNN....",
    "...........",
    "...........",
]

# Tortuga levantada (enfadada): cabeza alta, patas alzadas, ojos rojos
TORTUGA_2_DERECHA = [
    "..VVVVVVVVV...",
    ".VVVVVVVVVVV..",
    ".VVVVVVVVVVV..",
    "..RPPPPPPR....",   # ojos rojos de enfado
    "..PWPPPPWPP...",
    "..PPRPP.......",   # boca abierta
    "..PP....PP....",   # patas alzadas
    ".VVVVVVVVVVV..",   # caparazon
    ".VVgVVVVgVVg..",
    "VVgVVVVVVVgVV.",
    "VgVVVVgVVVVgV.",
    "VVVVVVVVVVVVV.",
    ".VVVVVVVVVVV..",
    "..NN.NNNN.NN..",
    "..NN.NNNN.NN..",
    "..............",
]

TORTUGA_2_IZQUIERDA = espejo(TORTUGA_2_DERECHA)

# Tortuga tumbada (panza arriba), 18x11
TORTUGA_TUMBADA = [
    ".PP............PP.",   # patas arriba
    ".VVVVVVVVVVVVVVVV.",
    "VVgVVgVVgVVgVVgVVV",
    "VgVVVVVVVVVVVVVVgV",
    ".VVVVVVVVVVVVVVVV.",
    "..NN..NN..NN..NN..",
    "..................",
    "..................",
    "..................",
    "..................",
    "..................",
]

# ----------------------------------------------------------------- MOSCA ----
MOSCA = [
    ".W..........W.",   # antenas
    "..IIIIIIIIII..",
    ".IIIIIIIIIIII.",
    ".IIWWIIIIWWII.",   # ojos
    ".IIIIIIIIIIII.",
    "..IIIIIIIIII..",
    ".W.IIIIIIII.W.",   # alas
    "..IIIIIIIIII..",
    "...IIIIIIIIII.",
    "....IIIIIIII..",
    ".....IIIIII...",
    ".....IIIIII...",
    ".....IIII.....",
    "....W....W....",   # patas
    "....W....W....",
]

# Mosca levantada: alas subidas
MOSCA_2 = [
    ".W...........W.",
    "..IIIIIIIIIIII.",
    ".IIIIIIIIIIIII.",
    ".IIWWIIIIIIWWI.",
    ".IIIIIIIIIIIII.",
    "..IIIIIIIIIIII.",
    ".WW.IIIIIIII.WW",
    "..IIIIIIIIIIII.",
    "...IIIIIIIIIII.",
    "....IIIIIIIIII.",
    ".....IIIIIIII..",
    ".....IIIIIIII..",
    ".....IIII......",
    "....W.....W....",
    "....W.....W....",
]

# Mosca tumbada (aplastada), 14x14
MOSCA_TUMBADA = [
    "..W........W..",
    ".IIIIIIIIIIII.",
    "IIIIIIIIIIIIII",
    "IIWWIIIIIIWWII",
    "IIIIIIIIIIIIII",
    "IIIIIIIIIIIIII",
    ".IIIIIIIIIIII.",
    "..IIIIIIIIII..",
    "...WWWWWWWW...",
    "..N........N..",
    "..............",
    "..............",
    "..............",
    "..............",
]

# -------------------------------------------------------------- CANGREJO ----
CANGREJO = [
    ".RRR........RRR.",   # pinzas grandes
    ".RRR........RRR.",
    "..RRR..W...RRR..",   # ojo
    "....RRRRRRRR....",
    "...RRRRRRRRRR...",
    "..RRRRRRRRRRRR..",
    "..RRRRRRRRRRRR..",
    "..RRRRRRRRRRRR..",
    "...RRRRRRRRRR...",
    "....RRRRRRRR....",
    "...RR...RR...RR.",   # patas
    "...NN...NN...NN.",
    "...NN.NN.NN.NN..",
    "................",
    "................",
    "................",
]

# Cangrejo levantado: pinzas mas altas, ojos rojos de enfado
CANGREJO_2 = [
    ".RRR........RRR.",
    "RRR..........RRR",
    ".RRR...R...RRR..",
    "..RRRRRRRRRR....",
    "...RRRRRRRRRR...",
    "..RRRRRRRRRRRR..",
    "..RRRRRRRRRRRR..",
    "..RRRRRRRRRRRR..",
    "...RRRRRRRRRR...",
    "....RRRRRRRR....",
    "...RR...RR...RR.",
    "...NN...NN...NN.",
    "...NN.NN.NN.NN..",
    "................",
    "................",
    "................",
]

# Cangrejo tumbado (aplastado), 16x16
CANGREJO_TUMBADO = [
    "..RRRRRRRRRRRR..",
    ".RRRRRRRRRRRRRR.",
    ".RRWWRRRRWWRR...",
    "RRRRRRRRRRRRRRRR",
    "RRRRRRRRRRRRRRRR",
    ".RRRRRRRRRRRRRR.",
    "..NN.NN..NN.NN..",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

# ------------------------------------------------------------------ POW ----
POW = [
    "WWWWWWWWWWWWWWWW",
    "WRRRRRRRRRRRRRRW",
    "WRPPPROOORWRWRRW",
    "WRPRPRORORWRWRRW",
    "WRPPPROOORWWWRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WRRRRRRRRRRRRRRW",
    "WWWWWWWWWWWWWWWW",
]

# ---------------------------------------------------------------- MONEDA ----
MONEDA = [
    "..YYYY..",
    ".YYYYYY.",
    "YYYYYYYY",
    "YYYYYYYY",
    "YYYYYYYY",
    "YYWYYYYY",   # brillo
    "YYYYYYYY",
    "YYYYYWYY",
    "YYYYYYYY",
    "YYYYYYYY",
    "YYYYYYYY",
    ".YYYYYY.",
    "..YYYY..",
    "..YYYY..",
]

# --------------------------------------------------------------- BLOQUES ----
BLOQUE1 = [   # fase 1
    "NNNNNN",
    "NssssN",
    "NssssN",
    "NssssN",
    "NssssN",
    "NssssN",
    "NNNNNN",
]

BLOQUE2 = [   # fase 2
    "NNNNNNN",
    "NsssssN",
    "NsssssN",
    "NsskssN",
    "NsssssN",
    "NsssssN",
    "NNNNNNN",
]

BLOQUE3 = [   # fase 3
    "NNNNNNN",
    "NkkkkkN",
    "NkkkkkN",
    "NkssskN",
    "NkkkkkN",
    "NkkkkkN",
    "NNNNNNN",
]

# -------------------------------------------------------------- LADRILLO ----
LADRILLO = [
    "NNNNNNNNNNNNNNN",
    "N.NNNNN.NNNNNNN",
    "NNNNNNNNNNNNNNN",
    "NNNNN.NNNNN.NNN",
    "NNNNNNNNNNNNNNN",
    "N.NNNNN.NNNNNNN",
    "NNNNNNNNNNNNNNN",
    "NNNNNNNNNNNNNNN",
]

# --------------------------------------------------------------- TUBERIAS ----
CAP_TUBERIA1 = "V" * 23                          # 23
CAP_TUBERIA2 = "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"  # 35
CUERPO_TUBERIA1 = "gVVVVVVVVVWWWWssssssVVg"         # 23
CUERPO_TUBERIA2 = "gVVVVVVVVVVVVVVVWWWWWWssssssssVVVVg"  # 35

TUBERIA1 = [
    CAP_TUBERIA1,
    *["g" + "V" * 21 + "g"] * 2,
    *[CUERPO_TUBERIA1] * 27,
]

TUBERIA2 = [
    CAP_TUBERIA2,
    *["g" + "V" * 33 + "g"] * 2,
    *[CUERPO_TUBERIA2] * 27,
]

SALIDA = ["gVVWWg"] * 30


def colocar_sprites() -> None:
    """Marca todos los sprites en sus bancos y coordenadas del juego."""
    # Banco 0: Mario (portada), enemigos, POW, moneda
    pintar(0, 0, 0, MARIO_QUIETO)                       # Mario derecha (blt 0,0,0)
    pintar(0, 26, 0, TORTUGA_DERECHA)                   # tortuga_sprite
    pintar(0, 59, 0, TORTUGA_IZQUIERDA)                 # tortuga_sprite_izquierda
    pintar(0, 0, 32, TORTUGA_2_DERECHA)                 # tortuga_sprite_2_derecha
    pintar(0, 32, 32, TORTUGA_2_IZQUIERDA)              # tortuga_sprite_2_izquierda
    pintar(0, 40, 6, TORTUGA_TUMBADA)                   # tortuga_sprite_tumbada
    pintar(0, 1, 16, MOSCA)                             # MOSCA_SPRITE
    pintar(0, 8, 56, MOSCA_2)                           # MOSCA_SPRITE_2
    pintar(0, 16, 16, MOSCA_TUMBADA)                    # MOSCA_SPRITE_TUMBADA
    pintar(0, 32, 16, CANGREJO)                         # CANGREJO_SPRITE
    pintar(0, 48, 32, CANGREJO_2)                       # CANGREJO_SPRITE_2
    pintar(0, 48, 16, CANGREJO_TUMBADO)                 # CANGREJO_SPRITE_TUMBADO
    pintar(0, 72, 0, POW)                               # POW_SPRITE
    pintar(0, 68, 17, MONEDA)                           # MONEDA_SPRITE

    # Banco 1: bloques, ladrillos, tuberias y salida
    # (BLOQUE2 en (16,0) para no solaparse con TUBERIA1 que empieza en x=26)
    pintar(1, 0, 0, BLOQUE1)                            # BLOQUE_SPRITE
    pintar(1, 16, 0, BLOQUE2)                           # BLOQUE2_SPRITE
    pintar(1, 56, 0, BLOQUE3)                           # BLOQUE3_SPRITE
    pintar(1, 0, 8, LADRILLO)                           # LADRILLO_SPRITE
    pintar(1, 26, 0, TUBERIA1)                          # TUBERIA_SPRITE
    pintar(1, 9, 39, TUBERIA2)                          # TUBERIA_SPRITE2
    pintar(1, 0, 38, SALIDA)                            # salida_sprite

    # Banco 2: frames animados de Mario (fila 0 derecha, fila 1 izquierda)
    pintar(2, 0, 0, MARIO_QUIETO)
    pintar(2, 16, 0, MARIO_PASO1)
    pintar(2, 32, 0, MARIO_PASO2)
    pintar(2, 0, 16, espejo(MARIO_QUIETO))
    pintar(2, 16, 16, espejo(MARIO_PASO1))
    pintar(2, 32, 16, espejo(MARIO_PASO2))


def vista_previa() -> None:
    """Genera assets/vista_previa.png con los tres bancos a escala x2."""
    pyxel.init(768, 512, title="Vista previa de sprites")
    pyxel.cls(0)
    for banco in range(3):
        pyxel.blt(banco * 512, 0, banco, 0, 0, 256, 256, scale=2)

    def update() -> None:
        pass

    def draw() -> None:
        pyxel.screenshot("assets/vista_previa.png")
        pyxel.quit()

    pyxel.run(update, draw)


def main() -> None:
    pyxel.init(64, 64, title="Generador de sprites")
    colocar_sprites()
    pyxel.colors[:] = PALETA_CLASICA
    pyxel.save("assets/mario.pyxres")
    pyxel.save_pal("assets/mario.pyxpal")
    print("assets/mario.pyxres y assets/mario.pyxpal guardados", flush=True)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        vista_previa()
    elif "--check" in sys.argv:
        for nombre in dir():
            valor = globals().get(nombre)
            if isinstance(valor, list) and valor and all(isinstance(f, str) for f in valor):
                largos = {len(f) for f in valor}
                assert len(largos) == 1, f"{nombre}: filas de distinto ancho {largos}"
                for f in valor:
                    assert set(f) <= set(PALETA), f"{nombre}: caracter desconocido {set(f) - set(PALETA)}"
        print("sprites validados", flush=True)
    else:
        main()