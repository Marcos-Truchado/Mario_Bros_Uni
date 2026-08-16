# Mario Bros Uni

Clon del arcade Mario Bros hecho con [Pyxel](https://github.com/kitao/pyxel).

## Jugar en el ordenador

```bash
python3 -m venv .venv          # una sola vez
.venv/bin/pip install pyxel    # una sola vez
.venv/bin/python main.py
```

Controles: flechas / WASD para moverse, espacio para saltar, A para empezar o
pausar, C para salir.

## Regenerar los sprites

Los sprites se definen como arte ASCII en `generar_sprites.py` y se convierten
en `assets/mario.pyxres` (imagenes) y `assets/mario.pyxpal` (paleta):

```bash
.venv/bin/python generar_sprites.py        # genera los assets
.venv/bin/python generar_sprites.py --check   # valida el arte
.venv/bin/python generar_sprites.py --preview # crea assets/vista_previa.png
```

## Version web (movil)

1. Empaqueta y genera el HTML jugable:

   ```bash
   .venv/bin/pyxel package . main.py
   .venv/bin/pyxel app2html Mario_Bros_Uni.pyxapp
   mv Mario_Bros_Uni.html index.html
   rm Mario_Bros_Uni.pyxapp
   ```

2. Sublica `index.html` en GitHub Pages (Settings -> Pages -> Deploy from a
   branch -> rama `main`, carpeta `/`). El juego se abre en el movil en
   `https://<usuario>.github.io/<repo>/` con el gamepad virtual en pantalla
   (cruz = moverse, boton = saltar / empezar, menu = pausa / salir).

Nota: la version web necesita conexion a internet (carga el motor
`pyxel.js` desde un CDN).