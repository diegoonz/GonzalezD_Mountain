"""Mascota de New Climb: un íbice geométrico (cabra montés) subido a una roca, con un mosquetón al cuello.

Lienzo de 600 x 600. `tinta` es el color de la figura, `fondo` el del recorte de las facetas y `acento` el del mosquetón.
"""


def ibice(tinta="#FFFFFF", fondo="#111111", acento="#8F3F6A", uid="ibice", con_roca=True):
    facetas = "".join(f'<path d="{d}"/>' for d in (
        # facetas sutiles: cadera, costado, hombro y cuello (estilo geométrico)
        "M234 300 L256 382", "M300 291 L326 385", "M362 285 L344 384", "M414 291 L392 379",
        "M436 240 L452 300",
    ))
    cuernos_marcas = "".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for x1, y1, x2, y2 in (
            (452, 196, 434, 202), (446, 170, 427, 180), (434, 146, 416, 160),
            (417, 126, 402, 144), (396, 112, 386, 132), (372, 106, 368, 126),
        ))
    roca = f"""
    <!-- roca / cumbre -->
    <path d="M96 600 L196 470 L238 482 L300 452 L360 466 L420 454 L470 482 L560 600 Z" fill="{tinta}"/>
    <path d="M196 470 L238 520 L300 452 M300 452 L330 520 L420 454 M420 454 L452 540" fill="none" stroke="{fondo}" stroke-width="3.5" stroke-linejoin="round" stroke-opacity=".6"/>""" if con_roca else ""
    return f"""
  <g id="{uid}">{roca}
    <!-- patas -->
    <path d="M226 372 L214 462 L234 462 L256 384 Z" fill="{tinta}"/>
    <path d="M262 380 L262 456 L280 456 L286 380 Z" fill="{tinta}"/>
    <path d="M382 372 L380 452 L398 452 L408 376 Z" fill="{tinta}"/>
    <path d="M408 360 L424 446 L442 446 L430 352 Z" fill="{tinta}"/>
    <!-- cuerpo -->
    <path d="M196 330 L232 300 L300 290 L362 284 L414 290 L438 330 L414 378 L362 384 L300 386 L244 382 L206 366 Z" fill="{tinta}"/>
    <!-- cola -->
    <path d="M200 322 L182 306 L196 336 Z" fill="{tinta}"/>
    <!-- cuello y cabeza mirando a la cumbre -->
    <path d="M402 296 L436 236 L466 222 L506 240 L512 258 L490 266 L470 286 L440 338 Z" fill="{tinta}"/>
    <!-- barba -->
    <path d="M488 266 L478 300 L470 284 Z" fill="{tinta}"/>
    <!-- oreja -->
    <path d="M446 232 L424 222 L440 244 Z" fill="{tinta}"/>
    <!-- ojo -->
    <circle cx="478" cy="240" r="5" fill="{fondo}"/>
    <!-- cuernos: gran arco hacia atrás con anillos -->
    <path d="M458 226 C 470 160, 420 92, 352 100 C 330 104, 318 116, 312 132
             C 336 118, 360 116, 384 124 C 420 138, 442 178, 440 230 Z" fill="{tinta}"/>
    <g stroke="{fondo}" stroke-width="5" stroke-linecap="round">{cuernos_marcas}</g>
    <!-- facetas -->
    <g fill="none" stroke="{fondo}" stroke-width="3" stroke-linecap="round" stroke-opacity=".45">{facetas}</g>
    <!-- mosquetón al cuello (color de acento) -->
    <g transform="translate(424 292) rotate(-28)">
      <rect x="-15" y="-24" width="30" height="48" rx="13" fill="none" stroke="{acento}" stroke-width="7"/>
      <rect x="-21" y="-2" width="10" height="16" rx="3" fill="{acento}"/>
    </g>
  </g>"""


def mascota_svg(tinta="#FFFFFF", fondo="#111111", acento="#8F3F6A", con_fondo=True):
    rect = f'<rect width="600" height="600" fill="{fondo}"/>' if con_fondo else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  {rect}{ibice(tinta, fondo, acento)}
</svg>"""


if __name__ == "__main__":
    import os
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida", "_prueba_mascota.svg")
    open(ruta, "w", encoding="utf-8").write(mascota_svg())
    print(ruta)
