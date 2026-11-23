import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

links = re.findall(r'(?:src|href)="([^"]+)"', html)
print(f"Total links found: {len(links)}")

all_ok = True
for link in links:
    if link.startswith('http') or link.startswith('#') or link.startswith('mailto:'):
        continue
    clean_link = link.split('?')[0].split('#')[0]
    exists = os.path.exists(clean_link)
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {clean_link}")
    if not exists:
        all_ok = False

if all_ok:
    print("\n[SUCCESS] Todos los enlaces locales en index.html apuntan a archivos existentes en disco!")
else:
    print("\n[ERROR] Hay enlaces rotos.")
