#!/usr/bin/env python3
"""Genera catalogo.js a partir de los MP3 existentes. Ejecutar tras generar.sh."""
import os, json, glob
from mutagen.mp3 import MP3

# slug -> (titulo, día de la web (data-dia) o 'tren', tipo)
#   tipo: 'capsula' (corto, delante del sitio) | 'guia' (largo) | 'fondo' (contexto)
META = {
 # fondo general: para el tren y para el coche
 '00-axarquia-historia':   ('La Axarquía: por qué esta esquina no se parece a las demás', 'tren', 'fondo'),
 '00-moriscos':            ('Los moriscos y la rebelión de 1569', 'tren', 'fondo'),
 '00-comida-malaguena':    ('La comida de esta costa: qué pedir y por qué', 'tren', 'fondo'),
 # Nerja
 '01-nerja-historia':      ('Historia de Nerja: de alquería a plató', 'nerja-1', 'fondo'),
 '01-balcon-europa-capsula':('El Balcón de Europa', 'nerja-1', 'capsula'),
 '02-cuevas-nerja-guia':   ('Las Cuevas de Nerja', 'nerja-2a', 'guia'),
 '03-maro-acantilados':    ('Los acantilados de Maro y Cerro Gordo', 'nerja-3', 'fondo'),
 '04-rio-chillar':         ('El río Chíllar: por qué se anda por dentro', 'nerja-4', 'guia'),
 '07-verano-azul':         ('Verano azul: cómo una serie construyó un pueblo', 'nerja-7', 'fondo'),
 '08-el-dia-de-volver':    ('El día de volver', 'nerja-8', 'fondo'),
 # Frigiliana y la Axarquía
 '02-frigiliana-guia':     ('Frigiliana: cómo se lee un pueblo morisco', 'frigiliana-2b', 'guia'),
 '06-competa-vino':        ('Cómpeta, el moscatel y las pasas', 'axarquia-6', 'guia'),
 # Málaga
 '05-malaga-historia':     ('Málaga: tres mil años de puerto', 'malaga-5', 'fondo'),
 '05-alcazaba-capsula':    ('La Alcazaba y Gibralfaro', 'malaga-5', 'capsula'),
 '05-picasso':             ('Picasso y Málaga: una relación rara', 'malaga-5', 'fondo'),
}

pistas = []
for slug, (titulo, sec, tipo) in META.items():
    f = slug + '.mp3'
    if not os.path.exists(f):
        print('  FALTA:', f); continue
    a = MP3(f)
    pistas.append({'id': slug, 't': titulo, 's': sec, 'k': tipo,
                   'd': int(a.info.length), 'mb': round(os.path.getsize(f)/1048576, 1)})

js = 'const AUDIOS=' + json.dumps(pistas, ensure_ascii=False, separators=(',', ':')) + ';\n'
open('catalogo.js', 'w').write(js)
tot = sum(p['d'] for p in pistas); peso = sum(p['mb'] for p in pistas)
print(f"{len(pistas)} pistas · {tot//3600}h {(tot%3600)//60}min · {peso:.0f} MB")
