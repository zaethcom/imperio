# IMPERIO — Análisis del proyecto y recomendaciones

Este documento resume una revisión del código actual (`index.html`, una sola
página con CSS y JS embebidos, servida como sitio estático en GitHub Pages
bajo el dominio `app.vincistore.com.co`) e identifica los problemas más
importantes junto con recomendaciones concretas, ordenadas por prioridad.

## Qué es el proyecto hoy

IMPERIO es una app de control financiero personal y de "disciplina" con
gamificación: cuentas, transacciones, metas de ahorro, hábitos con XP y
niveles, un módulo de ventas para emprendedores, una "academia" de
lecciones estáticas, un calendario de movimientos y un asistente llamado
MILLY IA. Todo corre en el navegador: no hay backend, no hay base de
datos, no hay autenticación — el estado completo (`S`) se guarda solo en
`localStorage` bajo la clave `imperio-v4`.

Esto es razonable para un prototipo de un solo usuario, pero trae
consecuencias que conviene tener explícitas antes de seguir construyendo
encima.

## 1. Crítico: la función de IA (MILLY) está rota en producción

`analyzeImpulse()` y `sendAIMsg()` llaman directamente desde el navegador a:

```js
fetch('https://api.anthropic.com/v1/messages', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({model: 'claude-sonnet-4-20250514', ...})
})
```

Sin ningún header de autenticación (`x-api-key`, `anthropic-version`). La
API de Anthropic exige esa cabecera y además no admite llamadas
directas desde un navegador (CORS). En la práctica, **toda petición a
MILLY falla siempre** y el usuario solo ve el mensaje de error genérico
("Error de conexión..."). Las dos funciones estrella del producto — el
"Escudo Anti-Impulso" y el chat de MILLY — no funcionan hoy para nadie.

**Por qué no se puede arreglar solo agregando la clave en el JS:** este
archivo se sirve tal cual desde GitHub Pages; cualquier persona puede ver
el código fuente. Si se pega una API key de Anthropic ahí, queda pública
y cualquiera puede copiarla y consumir la cuota/facturación del dueño.
Este es el motivo real por el que probablemente se dejó sin la clave.

**Recomendación:** la llamada a la IA necesita un intermediario en
servidor que guarde la clave de forma segura (variable de entorno) y
reciba solo el mensaje del usuario, no el modelo/clave. Opciones simples,
compatibles con seguir sirviendo `index.html` como estático:
- Una función serverless (Cloudflare Worker, Vercel Function, Netlify
  Function) que reciba `{item, price, reason}` o el historial del chat,
  llame a Anthropic con la clave guardada como secreto, y devuelva solo
  el texto de respuesta.
- El frontend cambia una línea: la URL de `fetch` pasa de
  `api.anthropic.com/v1/messages` a la URL de esa función.

Mientras no exista ese proxy, sería más honesto ocultar o marcar como
"próximamente" las secciones de MILLY en vez de dejarlas visibles y
fallando en silencio.

## 2. Crítico: pérdida de datos — todo vive solo en `localStorage`

No hay exportar/respaldar/importar. El botón "🗑️ Borrar todos los
datos" es la única operación masiva disponible. Si el usuario borra
datos del navegador, cambia de dispositivo, o reinstala el navegador,
pierde permanentemente todo su historial financiero (cuentas,
transacciones, metas, ventas, rachas, logros) sin ningún aviso previo ni
forma de recuperarlo.

Para una app que se presenta como "sistema operativo financiero
personal" esto es un riesgo serio, no cosmético.

**Recomendación (orden de esfuerzo creciente):**
1. Mínimo viable: botones "Exportar datos" (descarga el JSON de `S`) e
   "Importar datos" (sube ese JSON y hace `Object.assign(S, data)`).
   Esto ya cubre el caso de respaldo manual y migración de dispositivo.
2. Medio plazo: sincronización real con una cuenta (Supabase, Firebase,
   o similar) para tener respaldo automático y multi-dispositivo.

## 3. Importante: HTML de usuario insertado sin escapar (self-XSS)

Varios campos de texto que el propio usuario escribe se insertan
directamente en `innerHTML` sin escapar, por ejemplo:

- Nombre de cuenta: `value="${a.name}"` (línea ~629)
- Nombre de meta: `${g.name}` (línea ~439, ~700)
- Descripción de transacción: `${tx.desc||tx.category}` (línea ~606)
- Ítem/razón del anti-impulso: `${ic.item}` (línea ~823)
- Producto/cliente de venta: `${v.product}`, `${v.customer}` (línea ~889)

Si alguien escribe (o pega desde otro lado) algo como
`<img src=x onerror=alert(1)>` como nombre de una meta o descripción de
gasto, ese fragmento se ejecuta como HTML/JS cada vez que esa vista se
vuelve a renderizar, porque queda guardado tal cual en `localStorage`.

El impacto real es bajo (una sola persona, un solo dispositivo, sin
servidor ni sesión que robar), pero es una corrección barata: basta con
escapar estos campos (una función `esc()` que reemplace
`< > & " '`) antes de interpolarlos en las plantillas de `innerHTML`, o
usar `textContent` para esos nodos específicos en vez de `innerHTML`.

## 4. Sin pruebas, sin build, sin documentación

- El repositorio no tiene `README`, ni `package.json`, ni ningún tipo de
  prueba automatizada o *linting*. Es un único archivo HTML de más de
  1200 líneas con CSS y JS embebidos.
- Al no estar modularizado, un error de sintaxis en cualquier parte del
  `<script>` rompe la aplicación entera (pantalla de carga infinita),
  sin ningún aviso en tiempo de "build" porque no hay build.
- No hay forma de verificar cambios antes de que lleguen a producción
  (no hay CI, ni un entorno de *preview*): cada commit a `main` se
  publica directamente vía GitHub Pages.

**Recomendación:** no es necesario migrar a un framework para tener
algo de red de seguridad. Pasos de bajo costo:
- Agregar un `README.md` que explique qué es el proyecto, cómo se
  despliega (GitHub Pages + `CNAME`), y la limitación conocida de MILLY
  IA (sección 1) para que no se reporte como "bug misterioso".
- Considerar separar el archivo en `index.html` + `app.js` + `styles.css`
  para que los diffs de PRs sean legibles y revisables línea por línea.
- Si el proyecto va a crecer, migrar a una estructura con un paso de
  build simple (Vite, por ejemplo) permitiría lint/tests sin perder el
  despliegue estático.

## 5. Otros hallazgos menores

- **IDs por `Date.now()`**: usados como `id` único de cuentas, metas,
  transacciones y ventas. Funciona en la práctica porque cada creación
  pasa por una interacción de usuario, pero no es un esquema robusto de
  identificadores si en el futuro se agrega importación/fusión de datos
  o creación en lote.
- **Modelo de IA duplicado**: `claude-sonnet-4-20250514` está
  hardcodeado en dos lugares distintos (`analyzeImpulse` y
  `sendAIMsg`). Al resolver el punto 1, conviene declararlo una sola vez.
- **Sin validación de montos negativos**: los campos numéricos de monto
  (`parseFloat(...||0)`) no impiden valores negativos, lo que podría
  descuadrar totales de forma confusa (ej. una "venta" con precio
  negativo).
- **Contraste bajo en textos secundarios**: muchas etiquetas usan
  `rgba(255,255,255,0.28)` o menos sobre fondo `#080808`, lo que puede
  no cumplir con contraste mínimo de accesibilidad (WCAG AA) para texto
  pequeño.
- **Sin instalabilidad/offline real**: no hay `manifest.json` ni
  *service worker*. Como los datos ya viven en `localStorage`, agregar
  soporte PWA (instalar como app + funcionar sin red) sería una mejora
  de bajo costo y alto valor percibido, dado que el público objetivo
  parece ser móvil.

## Resumen priorizado

| # | Hallazgo | Severidad | Esfuerzo estimado |
|---|----------|-----------|--------------------|
| 1 | MILLY IA no funciona (falta proxy con la API key) | Crítico (funcionalidad core rota) | Medio — requiere una función serverless |
| 2 | No hay respaldo/exportación de datos | Crítico (riesgo de pérdida total de datos) | Bajo (exportar/importar JSON) |
| 3 | HTML de usuario sin escapar en `innerHTML` | Medio (self-XSS) | Bajo |
| 4 | Sin README/tests/lint/estructura modular | Medio (mantenibilidad) | Bajo a medio |
| 5 | IDs por `Date.now()`, modelo duplicado, validación de montos, contraste, sin PWA | Bajo | Bajo cada uno |

La recomendación de arranque más razonable es atacar el punto 2
(exportar/importar) primero por ser el de mayor riesgo con menor
esfuerzo, seguido del punto 1 si se quiere mantener la función de IA,
y el punto 3 como limpieza rápida de seguridad.
