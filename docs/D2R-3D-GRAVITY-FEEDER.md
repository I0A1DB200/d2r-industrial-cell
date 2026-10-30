# Cargador abierto y alimentación cinemática

2026-10-30. Base del paquete: e273a2ba7394b3d3ccbad6590932f2e88347dc6f. Rama visual/industrial-v1.2.

## Geometría verificada y reconstruida

El HTML anterior tenía feed.x=-2.98, ocho piezas decorativas sin consumo y pieza activa en X=-3. Se conserva feed.x y se sitúa el cargador en X local=-1.02 (mundial=-4). Una pieza activa inferior y hasta seis superiores reutilizan part(), de .52×.135×.38, paso .135. Los cinco cilindros oscuros que simulan taladros quedan enrasados en la cara superior, evitando que sobresalgan dentro de la siguiente pieza apilada; no son perforaciones CAD ni medición de calidad.

Cuatro guías abiertas se apoyan en el bastidor. Los travesaños inferiores dejan .15 de altura libre sobre y=1.2925, con .015 de margen sobre la pieza inferior. Las guías están fuera de los lados de la pieza; dos patines llegan hasta X mundial=-3.54, inicio de cinta. Corredera estrecha entre los patines, empujador naranja en reposo X local=-1.32 y lengüeta de acero posterior con cara superior1.4275 sostienen la pila al extraer la pieza inferior. La lengüeta queda fuera del cargador antes de descender.

Cilindro fijo orientado +X: centro(-2.25,1.10,0), longitud1.20, boca-1.65, trasera-2.85. Vástago de longitud variable entre anclaje interno-1.70 y reverso de la corredera/gate.x-.04. Tapas y cuerpo no siguen al empujador. Patas, bancada y apoyos bajo el cuerpo; la corredera discurre entre los apoyos de patines.

Cinta: cara superior1.2925, centro1.265 y espesor.055; plataforma centro1.13/alto.215; rodillos centro1.13/radio.16; guías laterales1.31. La pieza conserva centroY1.36, cara inferior1.2925. Vista feed: cámara[-4.9,3.4,-4.6], objetivo[-4.05,1.45,0]. Los otros mecanismos no se reposicionan en este paquete.

## Trayectoria gráfica dentro de FEED original

u=elapsed/.8 limitado a[0,1]. Avance 0… .45 con ease(u/.45), carrera1.0 y contacto constante entre empujador y cara trasera de pieza. Retorno .45… .75 con 1-ease((u-.45)/.30); pieza permanece enX=-3. Espera .75… .78. Descenso .78…1 cuadrático de un paso .135. Es animación cinemática de gravedad, sin solver, fuerzas ni validación física.

Número de superiores=longitud del lote−índice−pieza activa. Al empezar una pieza, la inferior pasa a ser el único mesh activo; al terminar, se oculta y el índice avanza en el instante anterior. No se crean piezas durante el ciclo. RESET recarga el mismo lote y devuelve ambos mecanismos a su pose inicial. Watch X conserva su conversión anterior: el tramo previo a X=-3 se muestra0 por el clamp existente.

No se cambian duración de FEED (.8), intervalo(.9), fases, transiciones, señales, conteo, rutas OK/NOK ni Safety. La válvula sigue las condiciones originales; no se afirma una neumática física a partir de esa señal.

## Validación ejecutada

`CHROMIUM_PATH=/usr/bin/chromium python tests/check_feeder.py`

HTTP automático, Chromium, clics reales y observador CDP externo. Sin modificar funciones/reloj. Capturas a640×480; lote completo observado a256×192 para limitar el coste de software. Resultado: todas las comprobaciones PASS, salida0, cero pageerror.

- Carga inicial7, activa en(-4,1.36,0).
- Capturas de avance, retorno y descenso durante FEED; contacto del empujador en avance, pieza quieta en cinta durante retorno, descenso después de retraer.
- Extremo interno y conexión de rod en cada captura; cuerpo fijo.
- Pausa conserva todas las observaciones y pose en esas tres etapas.
- Todo el lote: visible=7−índice en cada muestra; agotamiento7→6→5→4→3→2→1→0, sin duplicados observados. Fin4 OK/3 NOK.
- RESET desde lote vacío:7 visibles, empujador y pieza inferior en reposo.

[Informe y capturas](../tests/evidence/feeder/): loaded, advance, return, drop, empty y reset. Se revisó visualmente advance. Estos ensayos no prueban tolerancias de fabricación, resistencia, fricción o gravedad real. La transferencia OK posterior se documenta en [D2R-3D-PUSHER-TRANSFER.md](D2R-3D-PUSHER-TRANSFER.md).
