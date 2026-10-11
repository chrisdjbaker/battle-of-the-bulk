#!/usr/bin/env python3
"""Bundle src/index.html + images into one self-contained HTML file for the USB stick."""
import base64, json, pathlib
root = pathlib.Path(__file__).parent
A = root / 'src' / 'assets'
def uri(p): return 'data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode()
assets = {'logo': uri(A / 'logo.jpg'), 'kitsPoster': uri(A / 'kits_poster.jpg'), 'pricingPoster': uri(A / 'pricing_poster.jpg')}
for p in sorted((A / 'kits').glob('kit*.jpg')): assets[p.stem] = uri(p)
html = (root / 'src' / 'index.html').read_text()
html = html.replace('/*__ASSETS__*/', 'const ASSETS = ' + json.dumps(assets) + ';')
out = root / 'USB' / 'Battle of the Bulk.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html)
print(f'wrote {out} ({out.stat().st_size // 1024} KB)')
# GitHub Pages copy
web = root / 'docs' / 'index.html'
web.parent.mkdir(exist_ok=True)
web.write_text(html)
(root / 'docs' / '.nojekyll').write_text('')
print(f'wrote {web}')
