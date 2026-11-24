"""
Verifica que los enlaces locales (href, src, fetch y redirecciones) de index.html y de los
visores HTML en data/ apunten a archivos existentes, y que no queden rutas absolutas file:///.
Uso: python scripts/verificar_links_index.py   (desde cualquier carpeta)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATRON = re.compile(r'(?:src|href)="([^"]+)"|fetch\(\s*[\'"]([^\'"]+)[\'"]|url=([^"\s]+)"')


def revisar(ruta_html):
    base = os.path.dirname(ruta_html)
    with open(ruta_html, encoding="utf-8") as f:
        html = f.read()
    problemas = []
    if "file:///" in html:
        problemas.append("contiene rutas absolutas file:///")
    for m in PATRON.finditer(html):
        link = next(g for g in m.groups() if g)
        if link.startswith(("http", "#", "mailto:", "data:", "blob:", "javascript:")) or "${" in link:
            continue
        destino = os.path.normpath(os.path.join(base, link.split("?")[0].split("#")[0]))
        if not os.path.exists(destino):
            problemas.append(f"enlace roto: {link}")
    return problemas


def main():
    archivos = [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "looker_studio_borrador.html")] + sorted(glob.glob(os.path.join(ROOT, "data", "**", "*.html"), recursive=True))
    total_err = 0
    for ruta in archivos:
        problemas = revisar(ruta)
        rel = os.path.relpath(ruta, ROOT)
        print(f"[{'OK' if not problemas else 'ERROR'}] {rel}")
        for p in problemas:
            print(f"    - {p}")
        total_err += len(problemas)
    if total_err:
        print(f"\n[ERROR] {total_err} problema(s) encontrados.")
        sys.exit(1)
    print(f"\n[SUCCESS] {len(archivos)} archivos HTML revisados: todos los enlaces locales existen y no hay rutas file:///.")


if __name__ == "__main__":
    main()
