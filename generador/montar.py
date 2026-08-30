#!/usr/bin/env python3
"""Monta index.html juntando las piezas de generador/plantilla/ e inyectando
los bloques de comida dentro de la sección de cada zona (el JS del plan de «hoy»
busca el .comer dentro de la sección del día, no en una sección aparte)."""
import re, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
P = 'generador/plantilla/'

PIEZAS = ['head-nuevo.html', 'css-base.html', 'c1-cabecera.html', 'c2-mapa.html',
          'c3-nerja.html', 'c4-frigiliana.html', 'c5-sedella.html', 'c6-malaga.html', 'c7-comer.html',
          'c8-practico.html', 'c9-footer.html', '3-scripts.html']
# sección de la web -> fichero de comida
COMIDA = {'nerja': 'nerja', 'frigiliana': 'frigiliana', 'sedella': 'sedella', 'malaga': 'malaga'}

leyenda = open(P + 'comer/leyenda.html').read()
partes = []
for pieza in PIEZAS:
    s = open(P + pieza).read()
    puesta = False
    for sec, fich in COMIDA.items():
        if '<section id="%s" class="etapa-sec">' % sec not in s:
            continue
        bloque = open(P + 'comer/%s.html' % fich).read()
        pon = ('' if puesta or 'leyenda-sellos' in s else leyenda) + bloque
        puesta = True
        pat = re.compile(r'(<section id="%s" class="etapa-sec">.*?)(</section>)' % sec, re.S)
        s, n = pat.subn(lambda m: m.group(1) + '\n' + pon + m.group(2), s, count=1)
        assert n == 1, 'no se pudo inyectar la comida en #' + sec
    partes.append(s)

html = ''.join(partes)
html = html.replace('</style>\n<body>', '</style>\n</head>\n<body>', 1)
if not html.rstrip().endswith('</html>'):
    html = html.rstrip() + '\n</html>\n'
open('index.html', 'w').write(html)
print('index.html montado: %d KB' % (len(html) // 1024))
