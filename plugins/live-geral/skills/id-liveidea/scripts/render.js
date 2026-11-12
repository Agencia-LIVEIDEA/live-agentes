#!/usr/bin/env node
/* Renderiza peças LIVEIDEA em PNG com as fontes e tokens da versão baixada (Playwright/Chromium).
 *
 *   node render.js --kit KIT --ghost "<b>IDEIAS </b><em>QUE</em> GANHAM <b>VIDA</b>" --size 280 --out ghost.png
 *       Ghost transparente do tamanho do slide (1920x1080 por padrão), centralizado, sangrando a base,
 *       âmbar a 50%. Se a frase passar da largura útil (largura - 2x60px), o corpo diminui até caber.
 *   node render.js --kit KIT --svg KIT/assets/Logos/liveidea-nevoa.svg --width 1200 --out logo.png
 *       SVG em PNG transparente (logos e ícones para PowerPoint/Word, que não aceitam SVG via python-pptx).
 *   node render.js --kit KIT --html pagina.html --out pagina.png [--width 1920 --height 1080] [--transparent]
 *       Página HTML com tokens.css e fontes injetados (prévia de slide, revisão visual, peça de rede).
 *
 * Opções: --scale 1|2 (densidade), --width, --height.
 */
const fs = require('fs');
const path = require('path');

function args() {
  const a = {}; const v = process.argv.slice(2);
  for (let i = 0; i < v.length; i++) {
    if (v[i].startsWith('--')) {
      const k = v[i].slice(2);
      a[k] = (v[i + 1] && !v[i + 1].startsWith('--')) ? v[++i] : true;
    }
  }
  return a;
}

(async () => {
  const a = args();
  if (!a.kit || !a.out) { console.error('Uso: ver o cabeçalho do arquivo. --kit e --out são obrigatórios.'); process.exit(1); }
  let chromium;
  try { ({ chromium } = require('playwright')); } catch (e) {
    console.error('Playwright não encontrado. Instale (npm i playwright) ou exporte o Ghost/lettering em outra ferramenta.');
    process.exit(2);
  }
  const kit = path.resolve(a.kit);
  const css = fs.readFileSync(path.join(kit, 'fonts-inline.css'), 'utf8') + '\n' +
              fs.readFileSync(path.join(kit, 'tokens.css'), 'utf8');
  const W = parseInt(a.width || 1920, 10), H = parseInt(a.height || 1080, 10);
  const scale = parseFloat(a.scale || 1);
  let html, transparent = !!a.transparent;

  if (a.ghost) {
    transparent = true;
    const size = parseFloat(a.size || 307);
    html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}
      html,body{margin:0;background:transparent}
      .page{position:relative;width:${W}px;height:${H}px;overflow:hidden}
      .g{position:absolute;left:50%;bottom:0;margin:0;white-space:nowrap;font-family:var(--font-display);
         font-weight:400;font-size:${size}px;line-height:.74;letter-spacing:-.02em;text-transform:uppercase;
         color:var(--ambar);opacity:var(--opacity-watermark,.5);transform:translate(-50%,.2em)}
      .g b,.g strong{font-weight:700}.g em,.g i{font-weight:300;font-style:italic;text-transform:uppercase}
    </style></head><body><div class="page"><p class="g" id="g">${a.ghost}</p></div></body></html>`;
  } else if (a.svg) {
    transparent = true;
    const svg = fs.readFileSync(path.resolve(a.svg), 'utf8');
    html = `<!doctype html><html><head><style>html,body{margin:0;background:transparent}
      #s svg{display:block;width:${W}px;height:auto}</style></head><body><div id="s">${svg}</div></body></html>`;
  } else if (a.html) {
    const src = fs.readFileSync(path.resolve(a.html), 'utf8');
    const inject = `<style>${css}</style>`;
    html = /<head[^>]*>/i.test(src) ? src.replace(/<head[^>]*>/i, m => m + inject) : inject + src;
  } else { console.error('Informe --ghost, --svg ou --html.'); process.exit(1); }

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: a.svg ? 10 : H }, deviceScaleFactor: scale });
  // Arquivo temporário ao lado do HTML de origem (ou no kit), para os caminhos relativos funcionarem.
  const dir = a.html ? path.dirname(path.resolve(a.html)) : kit;
  const tmp = path.join(dir, `.__render_${process.pid}.html`);
  fs.writeFileSync(tmp, html);
  try { await page.goto('file://' + tmp, { waitUntil: 'load' }); } finally { fs.unlinkSync(tmp); }
  await page.evaluate(() => document.fonts.ready);

  if (a.ghost) {
    // A frase aparece inteira: reduz o corpo até caber com 60px de respiro de cada lado.
    const fit = await page.evaluate((W) => {
      const g = document.getElementById('g'); let s = parseFloat(getComputedStyle(g).fontSize); const s0 = s;
      while (g.scrollWidth > W - 120 && s > 40) { s -= 2; g.style.fontSize = s + 'px'; }
      return { from: s0, to: s, width: g.scrollWidth };
    }, W);
    if (fit.to !== fit.from) console.error(`Ghost reduzido de ${fit.from}px para ${fit.to}px para caber inteiro.`);
    await page.screenshot({ path: a.out, omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } });
  } else if (a.svg) {
    const el = await page.$('#s svg');
    await el.screenshot({ path: a.out, omitBackground: true });
  } else {
    await page.screenshot({ path: a.out, omitBackground: transparent, clip: { x: 0, y: 0, width: W, height: H } });
  }
  await browser.close();
  console.error('PNG salvo em ' + path.resolve(a.out));
})().catch(e => { console.error(e); process.exit(1); });
