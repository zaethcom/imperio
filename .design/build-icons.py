#!/usr/bin/env python3
"""Expande marcadores [[icon:name:size:color:stroke]] y [[illo:name:size:color]]
a SVG en linea dentro de los archivos .dc.html. Se ejecuta in-place."""
import re, sys, glob

I = {
 'cart':'<circle cx="9" cy="20" r="1.6"/><circle cx="18" cy="20" r="1.6"/><path d="M2 3h2.6l2.2 11.2a1.8 1.8 0 0 0 1.8 1.5h9.5a1.8 1.8 0 0 0 1.8-1.4L21.5 7H6"/>',
 'clipboard':'<rect x="4.8" y="4" width="14.4" height="17" rx="2.4"/><rect x="8.6" y="2" width="6.8" height="3.6" rx="1.4"/><path d="M8.8 10.4h6.4M8.8 14h6.4M8.8 17.6h4.2"/>',
 'box':'<path d="M12 2.6 21 7.4v9.2L12 21.4 3 16.6V7.4z"/><path d="M3 7.4 12 12.2l9-4.8"/><path d="M12 12.2v9.2"/>',
 'scooter':'<circle cx="5.2" cy="17.6" r="2.8"/><circle cx="18.8" cy="17.6" r="2.8"/><path d="M8 17.6h8.2L13.9 8.2"/><path d="M13.9 8.2 12.9 4.2h-2.4"/><path d="M12.9 4.2h3.6"/>',
 'transfer':'<path d="M4 8.6h13M13.8 5.4 17 8.6l-3.2 3.2"/><path d="M20 15.4H7M10.2 12.2 7 15.4l3.2 3.2"/>',
 'wrench':'<path d="M15.8 2.9a5.2 5.2 0 0 0-4.5 7.8L3.6 18.4a2.05 2.05 0 1 0 2.9 2.9l7.7-7.7a5.2 5.2 0 0 0 6.6-6.8l-2.9 2.9-2.9-.7-.7-2.9 2.9-2.9a5.3 5.3 0 0 0-1.4-.3z"/>',
 'users':'<circle cx="9.4" cy="8" r="3.7"/><path d="M2.9 20.2a6.5 6.5 0 0 1 13 0"/><path d="M16.4 5.1a3.7 3.7 0 0 1 0 5.8"/><path d="M18.1 14.5a6.5 6.5 0 0 1 3 5.7"/>',
 'chart':'<path d="M4 3.4v17.2h16.6"/><path d="M7.8 16.6v-4.4M12 16.6V8.4M16.2 16.6V5.6"/>',
 'gear':'<circle cx="12" cy="12" r="3.1"/><path d="M12 2.4 13.4 5a7.6 7.6 0 0 1 2 .8l2.7-1 1.8 3.1-2.1 1.9a7.6 7.6 0 0 1 0 2.4l2.1 1.9-1.8 3.1-2.7-1a7.6 7.6 0 0 1-2 .8L13.4 21.6h-2.8L9.2 19a7.6 7.6 0 0 1-2-.8l-2.7 1-1.8-3.1 2.1-1.9a7.6 7.6 0 0 1 0-2.4L2.7 9.9l1.8-3.1 2.7 1a7.6 7.6 0 0 1 2-.8L10.6 2.4z"/>',
 'home':'<path d="M3.4 10.4 12 3.3l8.6 7.1"/><path d="M5.6 8.9v11.8h12.8V8.9"/><path d="M9.7 20.7v-6.3h4.6v6.3"/>',
 'search':'<circle cx="10.9" cy="10.9" r="6.6"/><path d="M20.4 20.4 15.7 15.7"/>',
 'bell':'<path d="M18 8.8a6 6 0 1 0-12 0c0 5.9-2 7.3-2 7.3h16s-2-1.4-2-7.3z"/><path d="M13.7 19.8a2 2 0 0 1-3.4 0"/>',
 'barcode':'<path d="M3.2 5.2v13.6M6.4 5.2v13.6M9.4 5.2v9.4M12.4 5.2v13.6M15.4 5.2v9.4M18.2 5.2v13.6M20.8 5.2v13.6"/>',
 'trash':'<path d="M3.8 6.3h16.4"/><path d="M8.6 6.3V4.6A1.6 1.6 0 0 1 10.2 3h3.6a1.6 1.6 0 0 1 1.6 1.6v1.7"/><path d="M6.3 6.3 7.4 19.5a1.8 1.8 0 0 0 1.8 1.6h5.6a1.8 1.8 0 0 0 1.8-1.6L17.7 6.3"/><path d="M10.3 10.5v6.2M13.7 10.5v6.2"/>',
 'plus':'<path d="M12 5.2v13.6M5.2 12h13.6"/>',
 'minus':'<path d="M5.2 12h13.6"/>',
 'x':'<path d="M6.2 6.2 17.8 17.8M17.8 6.2 6.2 17.8"/>',
 'check':'<path d="M4.6 12.6 9.6 17.6 19.4 6.4"/>',
 'chevron-down':'<path d="M6.2 9.4 12 15.2l5.8-5.8"/>',
 'chevron-right':'<path d="M9.4 6.2 15.2 12l-5.8 5.8"/>',
 'user':'<circle cx="12" cy="8" r="3.8"/><path d="M4.6 20.4a7.4 7.4 0 0 1 14.8 0"/>',
 'user-plus':'<circle cx="9.6" cy="8" r="3.8"/><path d="M2.6 20.4a7 7 0 0 1 14 0"/><path d="M18.4 6.2v5.2M21 8.8h-5.2"/>',
 'card':'<rect x="2.4" y="5" width="19.2" height="14" rx="2.6"/><path d="M2.4 9.8h19.2"/><path d="M6 15h3.6"/>',
 'cash':'<rect x="2.4" y="5.8" width="19.2" height="12.4" rx="2.2"/><circle cx="12" cy="12" r="2.9"/><path d="M6 9.4v5.2M18 9.4v5.2"/>',
 'lock':'<rect x="4.6" y="10" width="14.8" height="11" rx="2.6"/><path d="M8.2 10V7.4a3.8 3.8 0 0 1 7.6 0V10"/><path d="M12 14.4v2.4"/>',
 'printer':'<path d="M7 9.2V3.6h10v5.6"/><rect x="3.4" y="9.2" width="17.2" height="7.4" rx="2.2"/><path d="M7 14.2h10v6.4H7z"/>',
 'clock':'<circle cx="12" cy="12" r="8.6"/><path d="M12 6.8V12l3.4 2"/>',
 'camera':'<path d="M4 8.4h2.8l1.5-2.3h7.4l1.5 2.3H20a1.8 1.8 0 0 1 1.8 1.8v7.2A1.8 1.8 0 0 1 20 19.2H4a1.8 1.8 0 0 1-1.8-1.8v-7.2A1.8 1.8 0 0 1 4 8.4z"/><circle cx="12" cy="13.6" r="3.3"/>',
 'refresh':'<path d="M20.3 11.2a8.3 8.3 0 0 0-14.2-4.6L3.6 9.1"/><path d="M3.7 12.8a8.3 8.3 0 0 0 14.2 4.6l2.5-2.5"/><path d="M3.6 4.6v4.5h4.5M20.4 19.4v-4.5h-4.5"/>',
 'save':'<path d="M4.6 3.4h11.1l4.9 4.9v10.8a1.7 1.7 0 0 1-1.7 1.7H4.6a1.7 1.7 0 0 1-1.7-1.7V5.1a1.7 1.7 0 0 1 1.7-1.7z"/><path d="M7.4 3.4v5.2h8.2V3.4"/><path d="M7.4 20.6v-6.2h9.2v6.2"/>',
 'filter':'<path d="M3.4 5.4h17.2l-6.7 7.9v5.9l-3.8 2.1v-8z"/>',
 'calendar':'<rect x="3.4" y="5.4" width="17.2" height="15.2" rx="2.4"/><path d="M3.4 10.2h17.2M8 3.4v4M16 3.4v4"/>',
 'note':'<path d="M5.4 3.4h9.2l5 5v12.2H5.4z"/><path d="M14.6 3.4v5h5"/><path d="M8.6 12.6h6.8M8.6 16.2h4.4"/>',
 'pin':'<path d="M12 21.2s7-6.2 7-11.2a7 7 0 1 0-14 0c0 5 7 11.2 7 11.2z"/><circle cx="12" cy="9.8" r="2.6"/>',
 'bank':'<path d="M2.8 9.4 12 4l9.2 5.4"/><path d="M5.4 9.4v9.2M9.8 9.4v9.2M14.2 9.4v9.2M18.6 9.4v9.2"/><path d="M2.8 21h18.4"/>',
 'menu':'<path d="M3.6 6.6h16.8M3.6 12h16.8M3.6 17.4h16.8"/>',
 'star':'<path d="m12 3.4 2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8-5.4 2.8 1-6L3.3 9.8l6-.9z"/>',
 'scan':'<path d="M3.4 8.6V5.4a2 2 0 0 1 2-2h3.2M15.4 3.4h3.2a2 2 0 0 1 2 2v3.2M20.6 15.4v3.2a2 2 0 0 1-2 2h-3.2M8.6 20.6H5.4a2 2 0 0 1-2-2v-3.2"/><path d="M3.4 12h17.2"/>',
 'shield':'<path d="M12 2.8 20 6v6c0 5-3.4 7.9-8 9.2C7.4 19.9 4 17 4 12V6z"/><path d="M9.2 12.2 11.4 14.4 15.2 10.2"/>',
 'battery':'<rect x="2.6" y="7.4" width="16.2" height="9.2" rx="2.2"/><path d="M21.4 10.6v2.8"/><path d="M5.8 10.4h3.4v3.2H5.8z"/>',
 'tag':'<path d="M11.2 3.4h9.4v9.4l-9 9a1.8 1.8 0 0 1-2.5 0l-6.9-6.9a1.8 1.8 0 0 1 0-2.5z"/><circle cx="16.3" cy="7.7" r="1.5"/>',
 'truck':'<path d="M2.6 6.4h10.8v10.2H2.6z"/><path d="M13.4 10h3.4l3.8 2.8v3.8h-7.2z"/><circle cx="7" cy="18.6" r="2"/><circle cx="17" cy="18.6" r="2"/>',
 'power':'<path d="M12 3.4v8.2"/><path d="M17.6 6.6a7.8 7.8 0 1 1-11.2 0"/>',
 'flash':'<path d="M13.4 2.6 4.8 13.4h6L10.6 21.4l8.6-10.8h-6z"/>',
 'history':'<path d="M3.6 12a8.4 8.4 0 1 0 2.6-6.1L3.4 8.6"/><path d="M3.4 4.2v4.4h4.4"/><path d="M12 7.6V12l3.2 1.9"/>',
 'dots':'<circle cx="5.4" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="18.6" cy="12" r="1.5"/>',
 'alert':'<path d="M12 3.6 21.4 20H2.6z"/><path d="M12 9.6v4.6M12 17.2v.2"/>',
 'wifi':'<path d="M12 18.4v.2"/><path d="M8.4 14.8a5.2 5.2 0 0 1 7.2 0"/><path d="M5.2 11.4a9.8 9.8 0 0 1 13.6 0"/>',
}

# Ilustraciones de producto sobre lienzo 64x64
L = {
 'scooter':'<circle cx="14" cy="47" r="7.6"/><circle cx="50" cy="47" r="7.6"/><path d="M21.6 47h22.8L37.2 20.6"/><path d="M37.2 20.6 34.4 9.6h-7"/><path d="M34.4 9.6h10.2"/><path d="M18 47h18"/>',
 'tire':'<circle cx="32" cy="32" r="23"/><circle cx="32" cy="32" r="11.6"/><path d="M32 9v8.4M32 46.6V55M9 32h8.4M46.6 32H55M15.7 15.7l6 6M42.3 42.3l6 6M48.3 15.7l-6 6M21.7 42.3l-6 6"/>',
 'helmet':'<path d="M8.4 40.6a23.6 23.6 0 0 1 47.2 0v4.8a3.4 3.4 0 0 1-3.4 3.4H30l-8.6-8.2z"/><path d="M21.4 40.6h34.2"/><path d="M15.6 24.8a23.6 23.6 0 0 1 33 6.4"/>',
 'charger':'<rect x="6" y="24" width="30" height="18" rx="3.4"/><path d="M36 33h6.4a7.6 7.6 0 0 1 7.6 7.6V50"/><circle cx="50" cy="53.4" r="3.6"/><path d="M12.4 30.4h9"/>',
 'brake':'<rect x="8" y="19" width="20" height="26" rx="4"/><rect x="34" y="19" width="20" height="26" rx="4"/><path d="M13.6 25.4h8.8M39.6 25.4h8.8"/>',
 'gloves':'<path d="M18 56V30.8a4 4 0 0 1 8 0v-6.4a4 4 0 0 1 8 0v-2a4 4 0 0 1 8 0v8.4a4 4 0 0 1 7.6-1.8v12A15.6 15.6 0 0 1 34 56z"/><path d="M18 38.4l-5-5a4 4 0 0 1 5.6-5.6l3 3"/>',
 'battery':'<rect x="6" y="22" width="46" height="20" rx="4"/><path d="M56 28.6v6.8"/><path d="M13 28h6.6v8H13zM23 28h6.6v8H23zM33 28h6.6v8H33z"/>',
 'controller':'<rect x="10" y="18" width="34" height="28" rx="3.4"/><path d="M44 24.6h10M44 32h10M44 39.4h10"/><path d="M17 25.6h20M17 32h20M17 38.4h13"/>',
 'lockcable':'<circle cx="22" cy="32" r="13.6"/><path d="M35.4 32h6.2a12 12 0 1 1 0 0z"/><path d="M35.6 32h8.6"/><circle cx="22" cy="32" r="4.6"/>',
 'toolkit':'<rect x="7" y="20" width="50" height="26" rx="4"/><path d="M7 30h50"/><path d="M15 36.4h7M26.6 36.4h7M38.2 36.4h7"/><path d="M24.4 20v-4.6a3 3 0 0 1 3-3h9.2a3 3 0 0 1 3 3V20"/>',
 'light':'<path d="M10 24.6h22l12-7.4v29.6l-12-7.4H10z"/><rect x="44" y="26" width="9" height="12" rx="2.6"/><path d="M20 39.4v8.4"/>',
 'disc':'<circle cx="32" cy="32" r="22.6"/><circle cx="32" cy="32" r="8.4"/><circle cx="32" cy="17.4" r="2.6"/><circle cx="44.6" cy="24.7" r="2.6"/><circle cx="44.6" cy="39.3" r="2.6"/><circle cx="32" cy="46.6" r="2.6"/><circle cx="19.4" cy="39.3" r="2.6"/><circle cx="19.4" cy="24.7" r="2.6"/>',
 'spray':'<rect x="14" y="20" width="16" height="34" rx="3.4"/><path d="M18.6 20v-5.4h6.8V20"/><rect x="34" y="26" width="14" height="28" rx="3"/><path d="M37.6 26v-4.6h6.8V26"/><path d="M18.6 30h7.6"/>',
}

def icon(m):
    p = (m.group(1).split(':') + ['','',''])[:4]
    n = p[0]; s = p[1] or '20'; c = p[2] or 'currentColor'; w = p[3] or '1.75'
    if n not in I: raise SystemExit('icono desconocido: ' + n)
    return ('<svg width="%s" height="%s" viewBox="0 0 24 24" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>') % (s, s, c, w, I[n])

def illo(m):
    p = (m.group(1).split(':') + ['','',''])[:4]
    n = p[0]; s = p[1] or '56'; c = p[2] or '#2C2F36'; w = p[3] or '2.6'
    if n not in L: raise SystemExit('ilustracion desconocida: ' + n)
    return ('<svg width="%s" height="%s" viewBox="0 0 64 64" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true">%s</svg>') % (s, s, c, w, L[n])

files = sys.argv[1:] or sorted(glob.glob('*.dc.html'))
for f in files:
    src = open(f, encoding='utf-8').read()
    out = re.sub(r'\[\[icon:([^\]]+)\]\]', icon, src)
    out = re.sub(r'\[\[illo:([^\]]+)\]\]', illo, out)
    if out != src:
        open(f, 'w', encoding='utf-8').write(out)
        print('expandido:', f)
    else:
        print('sin cambios:', f)
