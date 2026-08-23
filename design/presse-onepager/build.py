import base64, pathlib, sys
B = pathlib.Path(__file__).resolve().parent
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
html = (B / 'onepager.tmpl.html').read_text()
html = (html
        .replace('__SAIRA__', b64(B / 'saira-800-latin.woff2'))
        .replace('__SANS__',  b64(B / 'source-sans-3.woff2'))
        .replace('__ICON__',  b64(B.parent / 'hero-1.1' / 'app-icon.jpg')))
out = B / 'onepager.html'
out.write_text(html)
print(f'{out.name}: {len(html)//1024} KB')
