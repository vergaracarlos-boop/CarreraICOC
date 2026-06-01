import re
import pymupdf

CAP_REGEX = re.compile(r'^\s*(?:cap[ií]tulo\s+\d+|\d+\.)\s+(?!\d)', re.I)
SUB_REGEX = re.compile(r'^\s*\d+\.\d+')
TOC_SUB_REGEX = re.compile(r'^\s*\d+\.\d+\b')
NUMERO_CAP = re.compile(r'^\s*(cap[ií]tulo\s+\d+|\d+)', re.I)


def extraer_capitulos(pdf):
    with pymupdf.open(pdf) as doc:
        toc = doc.get_toc()
        if toc:
            capitulos = {}
            for lvl, title, page in toc:
                if not title or page <= 0:
                    continue
                title = title.replace('\r', ' ').strip()
                if lvl == 2 and (CAP_REGEX.match(title) or title.lower().startswith('capítulo')):
                    capitulos[page] = title
            if capitulos:
                return capitulos

        capitulos = {}
        for i in range(len(doc)):
            page = doc.load_page(i)
            top = page.rect.height * 0.25
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    texto = ''.join(span.get('text', '') for span in line.get('spans', [])).strip()
                    if not texto or SUB_REGEX.match(texto):
                        continue
                    if CAP_REGEX.match(texto):
                        y0 = line['spans'][0].get('bbox', [0, 0, 0, 0])[1] if line.get('spans') else 0
                        if y0 <= top and (i + 1) not in capitulos:
                            capitulos[i + 1] = texto
                            break
        return capitulos


def rangos_capitulos(capitulos, total_paginas):
    paginas = sorted(capitulos)
    pares = []
    for i, inicio in enumerate(paginas):
        fin = paginas[i + 1] - 1 if i + 1 < len(paginas) else total_paginas
        pares.append((inicio, fin))
    return pares


if __name__ == '__main__':
    ruta_del_pdf = '/home/carlosv/Descargas/Uso de aisladores y disipadores en estructuras.pdf'
    print(f'Analizando el archivo: {ruta_del_pdf}')
    capitulos = extraer_capitulos(ruta_del_pdf)

    if not capitulos:
        print('No se detectaron capítulos principales.')
    else:n
        print('\n--- Capítulos detectados ---')
        for pagina, titulo in sorted(capitulos.items()):
            nombre = NUMERO_CAP.match(titulo.strip())
            print(f"- {(nombre.group(0).strip() if nombre else titulo.strip())} -> página {pagina}")
        print('\n--- Fin de la lista de capítulos detectados ---')

        respuesta = input('¿Está correcto lo anterior? (s/n): ').strip().lower()
        if respuesta in ('s', 'si', 'y', 'yes'):
            with pymupdf.open(ruta_del_pdf) as doc:
                total = doc.page_count
            pares = rangos_capitulos(capitulos, total)
            print('\nListado de rangos de capítulos:')
            print(pares)
        else:
            print('No se generó el listado de rangos. Ajusta la detección y vuelve a ejecutar.')

