# Una semana en Nerja · 2026

Del **7 al 14 de septiembre de 2026**, siete noches con base fija en Nerja.
Tren hasta Málaga María Zambrano y coche de alquiler allí mismo.

👉 **Ver la web:** https://iaadileli.github.io/viaje-nerja-2026/

Nada a más de cuarenta minutos salvo el día de Málaga: las calas de Maro, el río Chíllar,
Frigiliana, los pueblos del moscatel de la Axarquía y un día en la capital.
Mapa, día a día con fotos, qué y dónde comer, playas, presupuesto y audioguía.

## Cómo está montado

Sale del patrón de [viaje-tailandia-2026](https://github.com/iaadileli/viaje-tailandia-2026):
mismo CSS y mismos scripts (plan de «hoy», buscador, modo oscuro, «qué tengo cerca»,
service worker), con la paleta cambiada a tonos de costa.

El `index.html` **no se edita entero a mano**: se monta juntando las piezas de
`generador/plantilla/` en este orden.

```bash
python3 generador/montar.py       # rehace index.html desde las piezas
python3 generador/sitios-nerja.py # regenera sitios.js (el «¿qué tengo cerca?»)
python3 generador/portada.py      # regenera img/portada.jpg y los iconos
```

Las piezas son: `head-nuevo.html` (metadatos), `css-base.html` (todo el CSS),
`c1-cabecera.html` (hero, menú y la semana), `c2-mapa.html` (el SVG dibujado a mano),
`c3-nerja.html`, `c4-frigiliana.html` (Frigiliana + la Axarquía), `c6-malaga.html`,
`c7-comer.html`, `c8-practico.html`, `c9-footer.html` y `3-scripts.html`.

Los bloques de «qué y dónde comer» viven aparte, en `generador/plantilla/comer/`, y `montar.py`
los inyecta dentro de la sección que les toca: el JS del plan de «hoy» busca el `.comer`
**dentro** de la sección del día, así que tienen que estar ahí y no en una sección suelta.

## Audioguía

15 pistas, unos 50 minutos, en `audio/`. Los guiones son la fuente (`audio/guiones/*.txt`).

```bash
cd audio && ./generar.sh && ~/.local/venvs/tts/bin/python catalogo.py
```

Cada pista se ata a un día por su `data-dia` en el diccionario `META` de `catalogo.py`.
Las de contexto general van con la sección `tren`, para escuchar de camino.

## Fotos

De Wikimedia Commons, con sus licencias apuntadas en `generador/datos-fuente/creditos-fotos.json`.

```bash
python3 generador/buscafotos.py <busquedas.json> <candidatas.json>
python3 generador/hoja-contacto.py <candidatas.json> <carpeta-hojas>
```

**Hay que mirarlas antes de usarlas.** La búsqueda por texto de Commons devuelve falsos
positivos con mucha alegría: buscando «Cómpeta» salen cinco fotos de una calle llamada Cómpeta
en la ciudad de Málaga, que no tienen nada que ver con el pueblo. Por eso está la hoja de contacto.

## Revisar antes de dar nada por bueno

```bash
node generador/revisar.mjs        # abre la página de verdad y la recorre
```

Comprueba con la página **en marcha** lo que no se ve leyendo el HTML: que ningún texto se
pinte dos veces, que las flechas ‹ › recorran los 8 días, que todos los días tengan dónde comer,
que las tablas no desborden en móvil, que no haya enlaces internos rotos ni errores de
JavaScript. Sale con código 1 si algo falla.
Necesita Playwright (`npm i -D playwright && npx playwright install chromium`).

## Pendiente

- Rellenar la sección `#hoteles` con el alojamiento real (nombre, dirección, si tiene garaje).
- Comprobar sobre el terreno las direcciones y horarios de los sitios de comer.
