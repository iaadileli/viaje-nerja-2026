#!/usr/bin/env python3
"""Genera sitios.js, la lista que usa «¿qué tengo cerca?».
Las coordenadas se piden a Nominatim (OpenStreetMap) y se cachean en
datos-fuente/coordenadas.json para no repetir peticiones. Ejecutar tras
cambiar los sitios de comer del index.html."""
import json, subprocess, os, sys, time
from urllib.parse import quote

# (nombre, zona, sección de la web, sello, consulta para Maps y para geocodificar)
SITIOS = [
 # los que recomienda un amigo que ha estado van con el sello 'a'
 ('Puerta del Mar',           'C/ Gómez',           'Nerja',      'a', 'Puerta del Mar, Calle Gómez, Nerja'),
 ('Chiringuito Mauri',        'Macaca, N-340a',     'Nerja',      'a', 'Chiringuito Mauri, Nerja'),
 ('El Pulguilla',             'Centro de Nerja',    'Nerja',      'a', 'El Pulguilla, Calle Almirante Ferrándiz 26, Nerja'),
 ('La Marina',                'Plaza la Marina',    'Nerja',      'a', 'La Marina, Plaza la Marina, Nerja'),
 ('El Sevillano',             'Centro de Nerja',    'Nerja',      'a', 'Sevillano La Tasquita, Nerja'),
 ('Merendero Ayo',            'Playa de Burriana',  'Nerja',      'v', 'Merendero Ayo Nerja'),
 ('Chiringuito de la playa de Maro','Maro',         'Nerja',      'b', 'Playa de Maro, Nerja'),
 ('Gloria Bendita',           'Frigiliana',         'Frigiliana', 'a', 'Gloria Bendita, Frigiliana'),
 ('El Adarve',                'Frigiliana',         'Frigiliana', '',  'Restaurante El Adarve, Frigiliana'),
 ('Taberna del Sacristán',    'Frigiliana',         'Frigiliana', 'l', 'Taberna del Sacristán, Frigiliana'),
 ('Bodegas de moscatel',      'Cómpeta',            'Frigiliana', '',  'Cómpeta, Málaga'),
 ('El Chiringuito',           'Sedella',            'Sedella',    'a', 'El Chiringuito, Avenida Villa del Castillo 24, Sedella, Málaga'),
 ('Bodegas de moscatel de Cómpeta','Cómpeta, de camino','Sedella','',  'Cómpeta, Málaga'),
 ('Antigua Casa de Guardia',  'Alameda Principal',  'Málaga',     'v', 'Antigua Casa de Guardia, Alameda Principal 18, Málaga'),
 ('El Tintero',               'El Palo',            'Málaga',     'l', 'Restaurante El Tintero, El Palo, Málaga'),
 ('Mercado de Atarazanas',    'Centro de Málaga',   'Málaga',     'b', 'Mercado de Atarazanas, Málaga'),
]
# centro de cada zona, como último recurso si Nominatim no encuentra el sitio
CENTROS = {'Nerja':(36.7452,-3.8746), 'Frigiliana':(36.7896,-3.8940),
           'Sedella':(36.8686,-4.0186), 'Málaga':(36.7213,-4.4213)}
CACHE = 'generador/datos-fuente/coordenadas.json'

def nominatim(q):
    cmd = ['curl','-s','--max-time','20','-H','User-Agent: guia-viaje-personal-adil','-G',
           'https://nominatim.openstreetmap.org/search',
           '--data-urlencode','q='+q, '--data-urlencode','format=json','--data-urlencode','limit=1']
    try:
        r = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
        if r: return float(r[0]['lat']), float(r[0]['lon'])
    except Exception: pass
    return None

# El sello va con su NOMBRE, no con una letra: el JS del «qué tengo cerca» y el
# CSS usan 'amigo'/'leyenda'/'local'/'barato'. Con las letras salía «undefined».
NOMBRE_SELLO = {'a': 'amigo', 'v': 'leyenda', 'l': 'local', 'b': 'barato', '': ''}

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
out, aprox = [], []
for nombre, zona, seccion, sello, consulta in SITIOS:
    if nombre in cache:
        la, lo, ap = cache[nombre]
    else:
        r = nominatim(consulta)
        if r: la, lo, ap = r[0], r[1], 0
        else: la, lo = CENTROS[seccion]; ap = 1
        cache[nombre] = [la, lo, ap]
        time.sleep(1.1)               # Nominatim pide 1 petición por segundo
    if ap: aprox.append(nombre)
    out.append({'n': nombre, 'z': zona, 'e': seccion, 's': NOMBRE_SELLO.get(sello, sello),
                'la': la, 'lo': lo, 'ap': ap, 'q': quote(consulta)})

json.dump(cache, open(CACHE,'w'), ensure_ascii=False, indent=1)
open('sitios.js','w').write('const SITIOS=' + json.dumps(out, ensure_ascii=False, separators=(',',':')) + ';\n')
print('sitios.js regenerado:', len(out), 'sitios')
if aprox: print('  con coordenadas aproximadas (centro de zona):', aprox)
