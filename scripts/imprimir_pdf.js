// Convierte catalogo/imprimible.html en PDF tamaño carta.
// Uso: node scripts/imprimir_pdf.js <entrada.html> <salida.pdf>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [entrada, salida] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(entrada), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: salida,
    format: 'Letter',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;padding:0 15mm;color:#777;display:flex;justify-content:space-between"><span>Catálogo de visualizaciones · Borrador v0.1</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '15mm', right: '15mm' },
  });
  await browser.close();
})();
