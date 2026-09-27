# Team Polaco Scooter · sistema de diseño de UI

Fuentes del lienzo de diseño publicado con Claude Design.

- `*.dc.html` — un artboard por archivo (fundamentos, botones, etiquetas,
  campos, tarjetas, navegación y siete pantallas completas: Vender, Taller,
  Escanear, Inicio, Inventario, Órdenes y Reportes).
- `canvas.json` — posición de cada artboard, páginas y vista de apertura.
- `logo-tps.png` — logo con fondo transparente (520 px).
- `build-icons.py` — expande los marcadores `[[icon:...]]` / `[[illo:...]]`
  a SVG en línea dentro de los `.dc.html`. Se ejecuta in-place:
  `python3 build-icons.py`.

Para regenerar el lienzo después de editar un artboard se vuelve a sembrar
con el helper de la skill `design` y se republica sobre la misma URL.
El HTML sembrado (~2,7 MB) es generado y no se versiona.

## Convenciones de las pantallas

- El armazón es el mismo en las siete: menú lateral de 260 px, barra
  superior de 72 px y franja institucional de 52 px. En total 1440 × 900,
  sin desbordes: si se cambia la altura de una tarjeta hay que ajustar las
  demás de su columna para que la suma siga cuadrando.
- **Un solo rojo por pantalla**, el de la acción que cobra, guarda o
  confirma. Por eso los gráficos nunca usan rojo: el énfasis de una barra
  se hace con tinta (`#0B0B0C` sobre el gris `#6B7078` de la serie).
- Los gráficos son de una sola serie y un solo color — nada de degradados
  por valor ni de arcoíris. Retícula de línea continua, extremos de barra
  redondeados a 4 px, 2 px de separación entre barras y etiquetas directas
  solo donde aportan (el máximo, el dato del día).
- Los estados (`En stock`, `Stock bajo`, `Agotado`, estados de orden) van
  siempre con texto, nunca solo con color.
- Las cifras usan `font-variant-numeric: tabular-nums` y la tipografía de
  interfaz (Archivo). Saira Condensed queda reservada para la voz de marca.
