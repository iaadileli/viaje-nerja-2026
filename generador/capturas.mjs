// Capturas de la página en marcha, para revisar el diseño mirándolo.
import { existsSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import path from 'node:path';
const RAIZ = path.join(import.meta.dirname, '..');
const donde = ['/home/adil/proyectos-adil/maquetador-libros/node_modules/playwright/index.mjs',
               path.join(RAIZ,'node_modules/playwright/index.mjs')].find(existsSync);
const { chromium } = await import(donde);
const puerto = 8733;
const srv = spawn('python3', ['-m','http.server',String(puerto),'-d',RAIZ,'-b','127.0.0.1'], {stdio:'ignore'});
await new Promise(r => setTimeout(r, 700));
const URL = `http://127.0.0.1:${puerto}/index.html`;
const salida = path.join(RAIZ, 'generador/datos-fuente/capturas');
mkdirSync(salida, { recursive: true });

const nav = await chromium.launch();
// --- escritorio
const p = await nav.newPage({ viewport: { width: 1280, height: 900 } });
await p.goto(URL, { waitUntil: 'networkidle' });
await p.screenshot({ path: `${salida}/1-portada.png` });
for (const [nombre, sel] of [['2-mapa','#mapa'], ['3-nerja','#nerja'], ['4-comida','#nerja .comer'],
                             ['5-axarquia','#axarquia'], ['6-presupuesto','#presupuesto']]) {
  const el = await p.$(sel);
  if (el) { await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(350);
            await p.screenshot({ path: `${salida}/${nombre}.png` }); }
}
// --- modo oscuro
await p.evaluate(() => document.querySelector('#tema')?.click());
await p.evaluate(() => document.querySelector('#nerja')?.scrollIntoView());
await p.waitForTimeout(350);
await p.screenshot({ path: `${salida}/7-oscuro.png` });
// --- móvil
const m = await nav.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
await m.goto(URL, { waitUntil: 'networkidle' });
await m.screenshot({ path: `${salida}/8-movil-portada.png` });
await m.evaluate(() => document.querySelector('#hoy')?.scrollIntoView());
await m.waitForTimeout(300);
await m.screenshot({ path: `${salida}/9-movil-hoy.png` });
await nav.close(); srv.kill();
console.log('capturas en', salida);
