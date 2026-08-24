import base64, pathlib
B = pathlib.Path(__file__).resolve().parent

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

ASSETS = {
    '__SAIRA__': b64(B / 'saira-800-latin.woff2'),
    '__SANS__':  b64(B / 'source-sans-3.woff2'),
    '__ICON__':  b64(B.parent / 'hero-1.1' / 'app-icon.jpg'),
}

for tmpl, out in (('onepager.tmpl.html', 'onepager.html'),
                  ('onepager-en.tmpl.html', 'onepager-en.html')):
    html = (B / tmpl).read_text()
    for k, v in ASSETS.items():
        html = html.replace(k, v)
    (B / out).write_text(html)
    print(f'{out}: {len(html)//1024} KB')
