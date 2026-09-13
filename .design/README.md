# Team Polaco Scooter · sistema de diseño de UI

Fuentes del lienzo de diseño publicado con Claude Design.

- `*.dc.html` — un artboard por archivo (fundamentos, botones, etiquetas,
  campos, tarjetas, navegación y tres pantallas completas).
- `canvas.json` — posición de cada artboard, páginas y vista de apertura.
- `logo-tps.png` — logo con fondo transparente (520 px).
- `build-icons.py` — expande los marcadores `[[icon:...]]` / `[[illo:...]]`
  a SVG en línea dentro de los `.dc.html`. Se ejecuta in-place:
  `python3 build-icons.py`.

Para regenerar el lienzo después de editar un artboard se vuelve a sembrar
con el helper de la skill `design` y se republica sobre la misma URL.
El HTML sembrado (~2,7 MB) es generado y no se versiona.
