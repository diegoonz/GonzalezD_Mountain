"""Genera la identidad visual de la tienda (logo, icono, portada, cabecera y guía de estilo).

Uso:
    python generar_identidad.py "New Climb"
    python generar_identidad.py "New Climb" --alumno "Diego González" --curso "2º DAM · Curso 2026-2027"

El nombre se reparte en dos líneas: la primera palabra va en la etiqueta y el resto, grande debajo.
Crea la carpeta salida/ con SVG, PNG y PDF. Necesita Microsoft Edge (para convertir a PNG/PDF).
"""

import argparse
import html
import math
import os
import random
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "salida")
NEGRO = "#111111"
BLANCO = "#FFFFFF"
GRIS = "#6B6B6B"
GRIS_C = "#D9D9D9"
GRIS_FONDO = "#E4E4E2"
BREZO = "#8F3F6A"      # color de acento: fucsia ciruela apagado (la flor de brezo de montaña)
BREZO_C = "#EFE3EA"
TITULOS = "'Bahnschrift', 'Impact', sans-serif"
TEXTO = "'Segoe UI', Arial, sans-serif"
LEMA = "ALQUILER DE MATERIAL DE MONTAÑA"
EDGE = [os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe")]


# --------------------------------------------------------------------------- piezas
def curvas_nivel(cx, cy, n, color, opacidad, semilla=7, paso=34, base=60):
    """Curvas de nivel tipo mapa topográfico: círculos deformados concéntricos."""
    rnd = random.Random(semilla)
    fases = [rnd.uniform(0, 6.28) for _ in range(3)]
    trazos = []
    for k in range(n):
        r0 = base + k * paso
        puntos = []
        for i in range(0, 361, 6):
            t = math.radians(i)
            r = r0 * (1 + 0.10 * math.sin(3 * t + fases[0]) + 0.06 * math.sin(5 * t + fases[1] + k * 0.15)
                      + 0.04 * math.sin(2 * t + fases[2]))
            puntos.append(f"{cx + r * math.cos(t):.1f},{cy + r * 0.78 * math.sin(t):.1f}")
        grosor = 2.2 if k % 5 == 4 else 1.1
        trazos.append(f'<polyline points="{" ".join(puntos)}" fill="none" stroke="{color}" '
                      f'stroke-width="{grosor}" stroke-opacity="{opacidad}"/>')
    return "\n".join(trazos)


def lineas_nombre(nombre):
    palabras = nombre.upper().split()
    if len(palabras) < 2:
        return "", nombre.upper()
    return palabras[0], " ".join(palabras[1:])


def mosqueton(tinta, papel, uid):
    """Mosquetón horizontal muy grueso, con la cordillera saliendo de su borde superior.

    Lienzo de 600 x 400. `tinta` es el color del mosquetón y `papel` el del interior.
    """
    cuerpo = "M150 92 L432 92 Q536 92 536 196 Q536 300 432 304 L176 312 Q64 312 64 202 Q64 92 150 92 Z"
    return f"""
  <g id="mosqueton-{uid}">
    <!-- cuerpo -->
    <path d="{cuerpo}" fill="{papel}" stroke="{tinta}" stroke-width="44" stroke-linejoin="round"/>
    <!-- cordillera que nace del borde superior -->
    <path d="M196 100 L262 34 L292 66 L330 14 L404 100 Z" fill="{tinta}" stroke="{tinta}" stroke-width="6" stroke-linejoin="round"/>
    <path d="M330 14 L314 37 L325 33 L333 45 L343 32 L351 41 Z" fill="{papel}"/>
    <path d="M262 34 L251 48 L260 45 L266 54 L274 45 Z" fill="{papel}"/>
    <!-- hueco del gatillo en el lado inferior -->
    <path d="M214 286 L404 280 L404 330 L214 336 Z" fill="{papel}"/>
    <!-- gatillo -->
    <line x1="206" y1="320" x2="414" y2="314" stroke="{tinta}" stroke-width="20" stroke-linecap="round"/>
    <!-- remaches de las bisagras -->
    <circle cx="198" cy="312" r="9" fill="{papel}" stroke="{tinta}" stroke-width="5"/>
    <!-- casquillo de seguridad (rosca) -->
    <rect x="322" y="294" width="78" height="40" rx="9" fill="{tinta}"/>
    <line x1="338" y1="300" x2="338" y2="328" stroke="{papel}" stroke-width="4"/>
    <line x1="352" y1="300" x2="352" y2="328" stroke="{papel}" stroke-width="4"/>
    <line x1="366" y1="300" x2="366" y2="328" stroke="{papel}" stroke-width="4"/>
    <line x1="380" y1="300" x2="380" y2="328" stroke="{papel}" stroke-width="4"/>
  </g>"""


def logo_svg(nombre, tinta=NEGRO, papel=BLANCO, con_lema=True, uid="logo"):
    """Logo principal: mosquetón + nombre en dos líneas en el centro."""
    l1, l2 = lineas_nombre(nombre)
    tam2 = max(56, min(112, 340 / (0.62 * max(len(l2), 1))))
    alto = 450 if con_lema else 372
    etiqueta = ""
    if l1:
        ancho_et = max(120, len(l1) * 46 + 44)
        etiqueta = f"""
    <g transform="rotate(-5 300 148)">
      <rect x="{300 - ancho_et / 2:.0f}" y="118" width="{ancho_et:.0f}" height="58" rx="6" fill="{tinta}"/>
      <text x="300" y="165" text-anchor="middle" font-family="{TITULOS}" font-weight="700" font-size="50"
            letter-spacing="10" fill="{papel}">{html.escape(l1)}</text>
    </g>"""
    y2 = 278 if l1 else 236
    lema = f"""<text x="300" y="420" text-anchor="middle" font-family="{TITULOS}" font-weight="600" font-stretch="condensed"
        font-size="24" letter-spacing="4.5" fill="{tinta}">{LEMA}</text>""" if con_lema else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {alto}" width="600" height="{alto}">
  {mosqueton(tinta, papel, uid)}
  {etiqueta}
  <text x="300" y="{y2}" text-anchor="middle" font-family="{TITULOS}" font-weight="700" font-size="{tam2:.0f}"
        letter-spacing="2" fill="{tinta}" stroke="{tinta}" stroke-width="5" stroke-linejoin="round"
        paint-order="stroke">{html.escape(l2)}</text>
  {lema}
</svg>"""


def icono_svg(nombre, uid="icono"):
    """Icono cuadrado (para el módulo de Odoo): mosquetón blanco sobre negro con las iniciales."""
    iniciales = "".join(p[0] for p in nombre.upper().split()[:2]) or "?"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="104" fill="{NEGRO}"/>
  <g transform="translate(256 262) scale(0.74) translate(-300 -196)">{mosqueton(BLANCO, NEGRO, uid)}</g>
  <text x="256" y="314" text-anchor="middle" font-family="{TITULOS}" font-weight="700" font-size="128"
        letter-spacing="4" fill="{BLANCO}" stroke="{BLANCO}" stroke-width="5" stroke-linejoin="round"
        paint-order="stroke">{html.escape(iniciales)}</text>
</svg>"""


def pagina(cuerpo, ancho, alto, extra_css=""):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
  @page {{ size: {ancho} {alto}; margin: 0; }}
  html, body {{ margin: 0; width: {ancho}; height: {alto}; background: transparent; }}
  {extra_css}
</style></head><body>{cuerpo}</body></html>"""


def portada_html(nombre, alumno, curso):
    logo_neg = logo_svg(nombre, BLANCO, NEGRO, con_lema=True, uid="portada")
    contornos = curvas_nivel(640, 210, 16, BLANCO, 0.14, semilla=11, paso=26, base=40)
    contornos2 = curvas_nivel(120, 1060, 12, NEGRO, 0.09, semilla=3, paso=24, base=40)
    css = f"""
  .hoja {{ position: relative; width: 210mm; height: 297mm; overflow: hidden; background: {BLANCO};
          font-family: {TEXTO}; color: {NEGRO}; }}
  .banda {{ position: absolute; inset: 0 0 auto 0; height: 168mm; background: {NEGRO}; overflow: hidden; }}
  .banda svg.topo, .pie-topo {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
  .logo {{ position: absolute; left: 50%; top: 30mm; width: 150mm; transform: translateX(-50%); }}
  .logo svg {{ width: 100%; height: auto; display: block; }}
  .textos {{ position: absolute; left: 0; right: 0; top: 190mm; text-align: center; }}
  .modulo {{ font-family: {TITULOS}; font-stretch: condensed; font-weight: 600; letter-spacing: 3pt;
            font-size: 12pt; color: {GRIS}; }}
  .titulo {{ font-family: {TITULOS}; font-weight: 700; font-size: 32pt;
            letter-spacing: .5pt; margin: 4mm 0 2mm; line-height: 1.08; text-transform: uppercase; }}
  .linea {{ width: 60mm; height: 1.4mm; background: {NEGRO}; margin: 6mm auto 0; }}
  .pie {{ position: absolute; left: 18mm; right: 18mm; bottom: 16mm; display: flex; justify-content: space-between;
         align-items: flex-end; border-top: .5mm solid {NEGRO}; padding-top: 4mm; font-size: 10.5pt; }}
  .pie b {{ font-family: {TITULOS}; font-stretch: condensed; font-size: 12pt; letter-spacing: 1pt; text-transform: uppercase; }}
  .pie .der {{ text-align: right; color: {GRIS}; }}"""
    cuerpo = f"""<div class="hoja">
  <div class="banda"><svg class="topo" viewBox="0 0 794 635" preserveAspectRatio="xMidYMid slice">{contornos}</svg></div>
  <svg class="pie-topo" viewBox="0 0 794 1123" preserveAspectRatio="none">{contornos2}</svg>
  <div class="logo">{logo_neg}</div>
  <div class="textos">
    <div class="modulo">SISTEMAS DE GESTIÓN EMPRESARIAL</div>
    <div class="titulo">Trabajo SGE<br>Diseño de una app en Odoo</div>
    <div class="linea"></div>
  </div>
  <div class="pie"><div><b>{html.escape(alumno)}</b><br>{html.escape(curso)}</div>
    <div class="der">Logotipo y portada realizados con ayuda de IA,<br>con permiso del profesor.</div></div>
</div>"""
    return pagina(cuerpo, "210mm", "297mm", css)


def cabecera_html(nombre, ancho=1600):
    logo_neg = logo_svg(nombre, BLANCO, NEGRO, con_lema=False, uid="cabecera")
    contornos = curvas_nivel(ancho - 350, 260, 22 + (ancho - 1600) // 60, BLANCO, 0.14, semilla=5, paso=30, base=30)
    css = f"""
  .cab {{ position: relative; width: {ancho}px; height: 480px; background: {NEGRO}; overflow: hidden; color: {BLANCO};
         font-family: {TEXTO}; }}
  .cab svg.topo {{ position: absolute; inset: 0; }}
  .logo {{ position: absolute; left: 80px; top: 50%; width: 560px; transform: translateY(-50%); }}
  .logo svg {{ width: 100%; height: auto; display: block; }}
  .txt {{ position: absolute; left: 720px; top: 50%; transform: translateY(-50%); }}
  .lema {{ font-family: {TITULOS}; font-stretch: condensed; font-weight: 700; font-size: 54px; line-height: 1.05;
          letter-spacing: 3px; text-transform: uppercase; }}
  .sub {{ font-size: 26px; letter-spacing: 5px; text-transform: uppercase; color: {GRIS_C}; margin-top: 18px; }}
  .linea {{ width: 140px; height: 6px; background: {BLANCO}; margin-top: 26px; }}"""
    cuerpo = f"""<div class="cab"><svg class="topo" width="{ancho}" height="480">{contornos}</svg>
  <div class="logo">{logo_neg}</div>
  <div class="txt"><div class="lema">Alquiler de material<br>de montaña</div>
    <div class="sub">Escalada · Trekking · Nieve</div><div class="linea"></div></div></div>"""
    return pagina(cuerpo, f"{ancho}px", "480px", css)


def guia_html(nombre):
    logo = logo_svg(nombre, uid="guia1")
    logo_neg = logo_svg(nombre, BLANCO, NEGRO, uid="guia2")
    icono = icono_svg(nombre, uid="guia3")
    muestra = lambda color, nombre_c, uso, borde="": f"""<div class="color"><div class="m" style="background:{color};{borde}"></div>
        <b>{nombre_c}</b><code>{color}</code><span>{uso}</span></div>"""
    css = f"""
  .g {{ width: 1200px; padding: 56px 64px; background: {BLANCO}; color: {NEGRO}; font-family: {TEXTO}; box-sizing: border-box; }}
  h1 {{ font-family: {TITULOS}; font-weight: 700; font-size: 44px; margin: 0; text-transform: uppercase; letter-spacing: 1px; }}
  h2 {{ font-family: {TITULOS}; font-stretch: condensed; font-weight: 700; font-size: 24px; margin: 36px 0 14px;
       text-transform: uppercase; letter-spacing: 2px; border-bottom: 3px solid {NEGRO}; padding-bottom: 6px; }}
  p.sub {{ color: {GRIS}; margin: 6px 0 0; font-size: 17px; }}
  .fila {{ display: grid; grid-template-columns: 300px 300px 150px; gap: 28px; align-items: center; }}
  .fila svg {{ width: 100%; height: auto; display: block; }}
  .neg {{ background: {NEGRO}; padding: 18px; border-radius: 10px; }}
  .nota {{ font-size: 15px; color: {GRIS}; line-height: 1.6; margin-top: 14px; }}
  .colores {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }}
  .color .m {{ height: 80px; border-radius: 10px; margin-bottom: 10px; }}
  .color b {{ display: block; font-size: 16px; }} .color code {{ font-size: 15px; }}
  .color span {{ display: block; font-size: 13.5px; color: {GRIS}; margin-top: 4px; }}
  .tipos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
  .t1 {{ font-family: {TITULOS}; font-weight: 700; font-size: 40px; text-transform: uppercase; letter-spacing: 1px; }}
  .t2 {{ font-family: {TEXTO}; font-size: 20px; line-height: 1.5; }}
  .tipos small {{ display: block; color: {GRIS}; font-size: 14px; margin-top: 6px; }}
  ul {{ margin: 0; padding-left: 22px; font-size: 16px; line-height: 1.7; }}"""
    cuerpo = f"""<div class="g">
  <h1>{html.escape(nombre)} · Guía de estilo</h1>
  <p class="sub">Identidad visual para el trabajo de SGE (documento y app de Odoo).</p>
  <h2>Logotipo</h2>
  <div class="fila"><div>{logo}</div><div class="neg">{logo_neg}</div><div>{icono}</div></div>
  <div class="nota"><b>Positivo</b> sobre fondos claros · <b>Negativo</b> sobre fondos oscuros (portada, cabeceras) ·
    <b>Icono</b> para tamaños pequeños, como el del módulo de Odoo (<code>static/description/icon.png</code>).
    No deformes el logo ni le añadas colores: siempre en blanco y negro.</div>
  <h2>Colores</h2>
  <div class="colores">
    {muestra(NEGRO, "Negro roca", "Fondos, títulos y logotipo")}
    {muestra(BLANCO, "Blanco nieve", "Fondo del documento", f"border:1px solid {GRIS_C};")}
    {muestra(GRIS, "Gris piedra", "Subtítulos y pies de imagen")}
    {muestra(GRIS_C, "Gris niebla", "Líneas, bordes y tablas")}
    {muestra(BREZO, "Brezo (acento)", "Marcos, destacados e iconos")}
    {muestra(BREZO_C, "Brezo claro", "Fondos de notas y tablas")}
  </div>
  <h2>Tipografías</h2>
  <div class="tipos">
    <div><div class="t1">Títulos en Bahnschrift</div><small>Bahnschrift Bold, MAYÚSCULAS (viene con Windows)</small></div>
    <div><div class="t2">El texto del documento va en Segoe UI o Calibri, a 11 pt y con interlineado 1,15.</div><small>Segoe UI / Calibri, normal</small></div>
  </div>
  <h2>Cómo aplicarlo en el documento</h2>
  <ul>
    <li>Títulos de apartado en Bahnschrift Bold y mayúsculas, con una línea negra debajo.</li>
    <li>Cabecera de cada página con <code>cabecera.png</code> pequeña o con el icono a la izquierda.</li>
    <li>Tablas con cabecera negra y texto blanco; filas separadas por líneas gris niebla.</li>
    <li>Capturas de pantalla con un borde fino gris y un pie de imagen en gris piedra.</li>
  </ul>
</div>"""
    return pagina(cuerpo, "1200px", "1180px", css)


def fondo_gris_html(ancho=2480, alto=3508):
    """Fondo de página A4 (300 ppp) gris con curvas de nivel negras en dos esquinas, el centro queda limpio."""
    esquina1 = curvas_nivel(ancho * 0.92, alto * 0.06, 26, NEGRO, 0.22, semilla=21, paso=46, base=60)
    esquina2 = curvas_nivel(ancho * 0.06, alto * 0.96, 24, NEGRO, 0.18, semilla=8, paso=48, base=60)
    css = f"body {{ background: {GRIS_FONDO}; }} svg {{ display: block; }}"
    cuerpo = f"""<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">
  <rect width="{ancho}" height="{alto}" fill="{GRIS_FONDO}"/>
  <g transform="scale(1)">{esquina1.replace('stroke-width="1.1"', 'stroke-width="2.4"').replace('stroke-width="2.2"', 'stroke-width="4.5"')}{esquina2.replace('stroke-width="1.1"', 'stroke-width="2.4"').replace('stroke-width="2.2"', 'stroke-width="4.5"')}</g>
</svg>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


def marco_html(ancho=1800, alto=1100):
    """Marco tipo tarjeta: interior blanco, borde en brezo, esquinas de visor y pestaña para el título."""
    m, r = 40, 34           # margen exterior y radio
    x2, y2 = ancho - m, alto - m
    L = 120                 # largo de los ángulos de las esquinas
    esquinas = f"""
    <path d="M{m - 22} {m + L} L{m - 22} {m - 22} L{m + L} {m - 22}"/>
    <path d="M{x2 - L} {m - 22} L{x2 + 22} {m - 22} L{x2 + 22} {m + L}"/>
    <path d="M{x2 + 22} {y2 - L} L{x2 + 22} {y2 + 22} L{x2 - L} {y2 + 22}"/>
    <path d="M{m + L} {y2 + 22} L{m - 22} {y2 + 22} L{m - 22} {y2 - L}"/>"""
    css = "body { background: transparent; } svg { display: block; }"
    cuerpo = f"""<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">
  <!-- tarjeta -->
  <rect x="{m}" y="{m}" width="{x2 - m}" height="{y2 - m}" rx="{r}" fill="{BLANCO}" stroke="{BREZO}" stroke-width="10"/>
  <!-- línea interior cosida, como el borde de un parche -->
  <rect x="{m + 22}" y="{m + 22}" width="{x2 - m - 44}" height="{y2 - m - 44}" rx="{r - 14}" fill="none"
        stroke="{NEGRO}" stroke-opacity=".35" stroke-width="2.5" stroke-dasharray="14 10"/>
  <!-- ángulos de visor en las esquinas -->
  <g fill="none" stroke="{BREZO}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round">{esquinas}</g>
  <!-- pestaña para el título (escribe encima en Word) -->
  <path d="M{m + 70} {m - 5} L{m + 640} {m - 5} L{m + 640} {m + 60} Q{m + 640} {m + 80} {m + 620} {m + 80}
           L{m + 90} {m + 80} Q{m + 70} {m + 80} {m + 70} {m + 60} Z" fill="{BREZO}"/>
  <!-- pequeño mosquetón en la esquina inferior derecha -->
  <g transform="translate({x2 - 150} {y2 - 112}) scale(0.18)">{mosqueton(BREZO, BLANCO, "marco")}</g>
</svg>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


def banner_mascota_html(nombre, ancho=1600, alto=480):
    """Banner negro con la mascota (íbice) a la izquierda, el logo en el centro y el lema a la derecha."""
    from mascota import ibice
    logo_neg = logo_svg(nombre, BLANCO, NEGRO, con_lema=False, uid=f"bm{ancho}")
    contornos = curvas_nivel(ancho - 300, 240, 22 + (ancho - 1600) // 60, BLANCO, 0.10, semilla=17, paso=30, base=30)
    css = f"""
  .ban {{ position: relative; width: {ancho}px; height: {alto}px; background: {NEGRO}; overflow: hidden; color: {BLANCO};
         font-family: {TEXTO}; }}
  .ban svg.capa {{ position: absolute; inset: 0; }}
  .logo {{ position: absolute; left: 470px; top: 50%; width: 460px; transform: translateY(-50%); }}
  .logo svg {{ width: 100%; height: auto; display: block; }}
  .txt {{ position: absolute; left: 1000px; top: 50%; transform: translateY(-50%); }}
  .lema {{ font-family: {TITULOS}; font-stretch: condensed; font-weight: 700; font-size: 50px; line-height: 1.05;
          letter-spacing: 2px; text-transform: uppercase; }}
  .lema b {{ color: {BREZO_C}; font-weight: 700; }}
  .sub {{ font-size: 22px; letter-spacing: 5px; text-transform: uppercase; color: {GRIS_C}; margin-top: 16px; }}
  .linea {{ width: 120px; height: 6px; background: {BREZO}; margin-top: 22px; border-radius: 3px; }}"""
    cuerpo = f"""<div class="ban">
  <svg class="capa" width="{ancho}" height="{alto}">{contornos}</svg>
  <svg class="capa" width="440" height="{alto}" viewBox="40 80 560 520" preserveAspectRatio="xMinYMax meet">{ibice(BLANCO, NEGRO, BREZO, uid=f"ib{ancho}")}</svg>
  <div class="logo">{logo_neg}</div>
  <div class="txt"><div class="lema">Tu próxima cumbre<br><b>empieza aquí</b></div>
    <div class="sub">Escalada · Trekking · Nieve</div><div class="linea"></div></div>
</div>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


def mascota_html(tinta, fondo, lado=1024):
    """La mascota sola, sin fondo, para usarla suelta en el documento."""
    from mascota import ibice
    css = "body { background: transparent; } svg { display: block; }"
    cuerpo = f'<svg width="{lado}" height="{lado}" viewBox="0 0 600 600">{ibice(tinta, fondo, BREZO, uid="suelta")}</svg>'
    return pagina(cuerpo, f"{lado}px", f"{lado}px", css)


def separador_html(ancho=4080, alto=192, etiqueta="", titulo=""):
    """Separador de partes del documento: rectángulo negro (60 % más bajo que el banner) con el íbice en blanco a la derecha.

    Si se pasa `etiqueta` y `titulo`, se escriben a la izquierda, alineados con el margen del documento (3 cm de 21).
    """
    from mascota import ibice
    alto_ibice = alto * 0.82
    ancho_ibice = alto_ibice * 360 / 380
    x = ancho - 300 - ancho_ibice
    x_texto = round(ancho * 3 / 21)
    texto = ""
    if titulo:
        texto = f"""
  <text x="{x_texto}" y="{alto / 2 + 25:.0f}" font-family="{TITULOS}" font-weight="700">
    <tspan font-size="40" letter-spacing="8" fill="{BREZO_C}">{html.escape(etiqueta.upper())}</tspan>
    <tspan dx="34" font-size="56" fill="{GRIS}">|</tspan>
    <tspan dx="34" font-size="74" letter-spacing="3" fill="{BLANCO}">{html.escape(titulo.upper())}</tspan>
  </text>"""
    css = "body { background: transparent; } svg { display: block; }"
    cuerpo = f"""<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">
  <rect width="{ancho}" height="{alto}" fill="{NEGRO}"/>{texto}
  <svg x="{x:.0f}" y="{(alto - alto_ibice) / 2:.0f}" width="{ancho_ibice:.0f}" height="{alto_ibice:.0f}" viewBox="170 92 360 380">
    {ibice(BLANCO, NEGRO, BLANCO, uid="separador", con_roca=False)}
  </svg>
</svg>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


def marco_nota_html(ancho=1800, alto=620):
    """Marco H3 para aclaraciones: todo negro, sin contorno, con un icono de información discreto."""
    r = 28
    css = "body { background: transparent; } svg { display: block; }"
    cuerpo = f"""<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">
  <rect x="0" y="0" width="{ancho}" height="{alto}" rx="{r}" fill="{NEGRO}"/>
  <!-- icono de información en la esquina superior izquierda -->
  <circle cx="74" cy="74" r="30" fill="none" stroke="{BLANCO}" stroke-width="5"/>
  <circle cx="74" cy="60" r="4.5" fill="{BLANCO}"/>
  <rect x="70" y="70" width="8" height="24" rx="4" fill="{BLANCO}"/>
  <!-- guía muy sutil donde empieza el texto -->
  <rect x="128" y="72" width="70" height="4" rx="2" fill="{GRIS}"/>
</svg>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


def marco_negro_html(ancho=1800, alto=1100):
    """Marco 'normal' y ligero: borde negro fino, dos ángulos discretos y una barra corta bajo el título.

    Sin color de acento: el brezo se reserva para el marco de cosas a destacar.
    """
    m, r = 30, 26
    x2, y2 = ancho - m, alto - m
    L = 80
    css = "body { background: transparent; } svg { display: block; }"
    cuerpo = f"""<svg width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">
  <rect x="{m}" y="{m}" width="{x2 - m}" height="{y2 - m}" rx="{r}" fill="{BLANCO}" stroke="{NEGRO}" stroke-width="4"/>
  <!-- ángulos discretos: arriba a la izquierda y abajo a la derecha -->
  <g fill="none" stroke="{NEGRO}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">
    <path d="M{m - 14} {m + L} L{m - 14} {m - 14} L{m + L} {m - 14}"/>
    <path d="M{x2 + 14} {y2 - L} L{x2 + 14} {y2 + 14} L{x2 - L} {y2 + 14}"/>
  </g>
  <!-- barra corta bajo la zona del título -->
  <rect x="{m + 60}" y="{m + 118}" width="160" height="7" rx="3.5" fill="{NEGRO}"/>
  <rect x="{m + 232}" y="{m + 118}" width="40" height="7" rx="3.5" fill="{GRIS_C}"/>
</svg>"""
    return pagina(cuerpo, f"{ancho}px", f"{alto}px", css)


# ------------------------------------------------------------------------- render
def edge():
    for ruta in EDGE:
        if os.path.isfile(ruta):
            return ruta
    sys.exit("No encuentro Microsoft Edge para generar los PNG/PDF.")


def a_png(html_ruta, png_ruta, ancho, alto):
    subprocess.run([edge(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                    f"--window-size={ancho},{alto}", f"--screenshot={png_ruta}", "file:///" + html_ruta.replace("\\", "/")],
                   capture_output=True, timeout=60)


def a_pdf(html_ruta, pdf_ruta):
    subprocess.run([edge(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_ruta}",
                    "file:///" + html_ruta.replace("\\", "/")], capture_output=True, timeout=60)


def escribir(nombre, contenido):
    ruta = os.path.join(SALIDA, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def svg_a_png(nombre_archivo, svg, ancho, alto, fondo="transparent"):
    svg = svg.replace('width="600"', f'width="{ancho}"', 1).replace('width="512" height="512"', f'width="{ancho}" height="{alto}"', 1)
    svg = svg.replace(f'height="450"', f'height="{alto}"', 1).replace(f'height="372"', f'height="{alto}"', 1)
    h = escribir(f"_{nombre_archivo}.html", pagina(svg, f"{ancho}px", f"{alto}px", f"body {{ background: {fondo}; }} svg {{ display: block; }}"))
    a_png(h, os.path.join(SALIDA, f"{nombre_archivo}.png"), ancho, alto)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("nombre", nargs="?", default="New Climb")
    p.add_argument("--alumno", default="Diego González")
    p.add_argument("--curso", default="2º DAM · Curso 2026-2027")
    a = p.parse_args()
    os.makedirs(SALIDA, exist_ok=True)
    for f in os.listdir(SALIDA):
        os.remove(os.path.join(SALIDA, f))

    logo = logo_svg(a.nombre)
    logo_neg = logo_svg(a.nombre, BLANCO, NEGRO, uid="neg")
    logo_simple = logo_svg(a.nombre, con_lema=False, uid="simple")
    icono = icono_svg(a.nombre)
    escribir("logo.svg", logo)
    escribir("logo_negativo.svg", logo_neg)
    escribir("logo_sin_lema.svg", logo_simple)
    escribir("icono.svg", icono)

    svg_a_png("logo", logo, 1200, 900)
    svg_a_png("logo_negativo", logo_neg, 1200, 900, NEGRO)
    svg_a_png("logo_sin_lema", logo_simple, 1200, 744)
    svg_a_png("icono", icono, 512, 512)
    svg_a_png("icon", icono, 256, 256)

    h = escribir("portada.html", portada_html(a.nombre, a.alumno, a.curso))
    a_pdf(h, os.path.join(SALIDA, "portada.pdf"))
    a_png(h, os.path.join(SALIDA, "portada.png"), 794, 1123)

    a_png(escribir("_cabecera.html", cabecera_html(a.nombre)), os.path.join(SALIDA, "cabecera.png"), 1600, 480)
    # Versión ancha (proporción de un A4 a sangre: 21 x 3,15 cm) para el encabezado del documento
    a_png(escribir("_cabecera_ancha.html", cabecera_html(a.nombre, 3200)), os.path.join(SALIDA, "cabecera_ancha.png"), 3200, 480)
    # Versión para el encabezado de Word (21 x 2,47 cm)
    a_png(escribir("_cabecera_word.html", cabecera_html(a.nombre, 4080)), os.path.join(SALIDA, "cabecera_word.png"), 4080, 480)
    a_png(escribir("_guia.html", guia_html(a.nombre)), os.path.join(SALIDA, "guia_estilo.png"), 1200, 1180)
    a_png(escribir("_fondo.html", fondo_gris_html()), os.path.join(SALIDA, "fondo_gris_A4.png"), 2480, 3508)
    a_png(escribir("_marco.html", marco_html()), os.path.join(SALIDA, "marco_brezo.png"), 1800, 1100)
    a_png(escribir("_marco_negro.html", marco_negro_html()), os.path.join(SALIDA, "marco_negro.png"), 1800, 1100)
    a_png(escribir("_marco_nota.html", marco_nota_html()), os.path.join(SALIDA, "marco_nota.png"), 1800, 620)
    a_png(escribir("_separador.html", separador_html()), os.path.join(SALIDA, "separador.png"), 4080, 192)
    for n, titulo in ((1, "La empresa y la app"), (2, "Desarrollo"), (3, "Conclusión")):
        a_png(escribir(f"_sep{n}.html", separador_html(etiqueta=f"Parte {n}", titulo=titulo)),
              os.path.join(SALIDA, f"separador_parte{n}.png"), 4080, 192)
    a_png(escribir("_banner_mascota.html", banner_mascota_html(a.nombre)), os.path.join(SALIDA, "banner_mascota.png"), 1600, 480)
    a_png(escribir("_banner_mascota_w.html", banner_mascota_html(a.nombre, 4080)), os.path.join(SALIDA, "banner_mascota_word.png"), 4080, 480)
    a_png(escribir("_mascota_b.html", mascota_html(BLANCO, NEGRO)), os.path.join(SALIDA, "mascota_blanca.png"), 1024, 1024)
    a_png(escribir("_mascota_n.html", mascota_html(NEGRO, BLANCO)), os.path.join(SALIDA, "mascota_negra.png"), 1024, 1024)

    for f in os.listdir(SALIDA):
        if f.startswith("_"):
            os.remove(os.path.join(SALIDA, f))
    print("Generado en", SALIDA)
    for f in sorted(os.listdir(SALIDA)):
        print(" -", f)


if __name__ == "__main__":
    main()
