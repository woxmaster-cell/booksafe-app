import base64, pathlib
B = pathlib.Path(__file__).resolve().parent
D = B.parent

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

SHARED = {
    '__SAIRA__': b64(D / 'presse-onepager' / 'saira-800-latin.woff2'),
    '__SANS__':  b64(D / 'presse-onepager' / 'source-sans-3.woff2'),
    '__ICON__':  b64(D / 'hero-1.1' / 'app-icon.jpg'),
}

SPRACHEN = {
    'de': {
        '__LANG__': 'de',
        '__HEADLINE__': 'Deine Bibliothek<br>gehört <em>dir.</em>',
        '__SUB__': 'Die Buch-App ohne Konto, ohne Tracking, ohne Abo.',
        '__PHONE__': b64(B / 'shot-today-de.jpg'),
        '__WATCH__': b64(B / 'shot-watch-de.jpg'),
    },
    'en': {
        '__LANG__': 'en',
        '__HEADLINE__': 'Your library<br>belongs to <em>you.</em>',
        '__SUB__': 'The book app with no account, no tracking, no subscription.',
        '__PHONE__': b64(B / 'shot-today-en.jpg'),
        '__WATCH__': b64(B / 'shot-watch-en.jpg'),
    },
}

tmpl = (B / 'card.tmpl.html').read_text()
for code, werte in SPRACHEN.items():
    html = tmpl
    for k, v in {**SHARED, **werte}.items():
        html = html.replace(k, v)
    (B / f'card-{code}.html').write_text(html)
    print(f'card-{code}.html: {len(html)//1024} KB')
