# D2R-3D · Mejora visual industrial v1.2

Fecha: 2026-10-30. Rama: `visual/industrial-v1.2`. Base del paquete: `f2fc2c25688aa1815bcee3c6a0763eb082815757`.

## Objetivo y alcance

Dar profundidad y lectura de superficies al prototipo existente, sin cambiar el comportamiento del simulador. SSOT: `D2R-3D-001_Prototipo_Funcional_v11.html`. Trabajo autorizado de representación visual; no se reconstruyen todavía las trayectorias del alimentador o del expulsor.

La referencia `tests/baseline/V0.html` permanece inmutable con SHA256 `fb09ee9b8ef9ee635ea138283f1faaaf2d75b0ad9025a05395d77715948a76b3`. No se sustituye por las nuevas capturas ni por el HTML modificado.

## Cambios exactos

| Elemento | Implementación |
| --- | --- |
| Color | THREE.ACESFilmicToneMapping, exposición inicial 1.12, salida SRGB. |
| Entorno | PMREMGenerator.fromScene sobre una escena local con tres paneles luminosos de estudio; sin HDRI ni nuevas descargas. Se libera el generador y la geometría/material de los paneles después del bake; se conserva el render target que contiene el entorno. |
| Metales | Reflejos del entorno en aluminio y acero, intensidad 1.05/1.15; aristas .85. Se mantienen los colores y parámetros base de los materiales. |
| Iluminación | Principal cálida #ffe2bc (3.2), relleno frío #b5d5ff (1.0), contraluz frío #9fc7ff (1.6) y hemisférica tenue (.8). |
| Sombras | Solo la principal proyecta sombra, PCFSoft 2048². Frustum ±6.5 en X y ±5.5 en Y, near 1/far 24, orientado a la célula; no intenta cubrir el suelo completo de 22×19. Bias −.00015, normalBias .025. |
| Suelo y cinta | Dos CanvasTexture de 256×256, ruido determinista de albedo; cinta con estrías discretas. RepeatWrapping, mipmaps por defecto, anisotropía máxima 4. Suelo mate y cuadrícula de opacidad .16. |
| Coste de fragmento | Sin bumpMap, normalMap, postprocesado ni sombras adicionales. No se añade un modo que modifique el reloj para compensar el software renderer. |
| Biseles | Chaflán de una subdivisión solo si el espesor mínimo es ≥.08 y la dimensión máxima <15 unidades. Ancho min(.012, espesor×.08); extrusión y contorno retraídos para respetar la envolvente exterior original. Se reutilizan geometrías de caja con dimensiones iguales. Láminas, cristal y suelo quedan sin bisel. |
| Cilindros | Helper con 32 segmentos radiales, posiciones, radios, longitudes y ejes originales. |
| Cristal | No proyecta sombras opacas; conserva transparencia y depthWrite=false originales. |
| Resolución | devicePixelRatio limitado a 2 en arranque y recalculado en resize. |
| Carteles | Eliminadas las siete llamadas y el helper label: ALIMENTADOR, INSPECCIÓN, EXPULSOR, SALIDA A, SALIDA B, ARMARIO y FLUJO. Sin sprites de cartelería ni texturas asociadas. Se conservan los cinco botones y sus presets. |

No hay assets externos nuevos ni dependencias nuevas. Three.js 0.164.1 sigue siendo el único import del HTML. La escena sigue siendo un modelo didáctico de primitivas, no un CAD ni una simulación física validada.

## Invariantes y comprobación estática

El comprobador visual compara con V0:

- HTML de la interfaz anterior al script, byte a byte: preserva HMI, Watch, alarmas, averías y controles.
- Código desde el marcador de máquina determinista hasta el arranque: byte a byte, incluidas fases, tiempos, señales, clasificación, contadores, Safety y callbacks.
- Posiciones y dimensiones de los objetos originales: idénticas tras retirar las llamadas de cartelería y normalizar espacios.
- Animación y reloj originales: idénticos salvo el recálculo de pixel ratio en resize.

La representación visual no redefine sensores como colisiones, el permiso Safety ni las salidas A/B.

## Ejecución reproducible

Usar el entorno Playwright descrito en [D2R-3D-BASELINE.md](D2R-3D-BASELINE.md). Ambos comandos levantan y cierran su propio servidor HTTP en un puerto libre y usan Chromium; el HTML se sirve sin reescribir.

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/check_visual.py
CHROMIUM_PATH=/usr/bin/chromium python tests/run_baseline.py \
  --target D2R-3D-001_Prototipo_Funcional_v11.html \
  --output test-results/visual-functional --width 640 --height 480 --timeout 1200
sha256sum -c tests/baseline/V0.sha256
git diff --check
```

`tests/visual-observer.js` es un adaptador CDP separado de solo lectura: mide límites de vértices, configuración de luces/materiales, geometrías y estado del renderer. No se introducen funciones de prueba en el HTML ni se sustituye el reloj.

El runner funcional admite ahora width/height configurables, manteniendo 960×640 como valor por defecto. También marca explícitamente como incompleto un informe interrumpido, en lugar de dejar únicamente los PASS parciales.

## Evidencias y resultado

Ejecutado en Chromium 154.0.8037.57 con Playwright 1.62.0:

- Comprobación visual específica: **20 PASS, salida 0**. ACES/exposición/entorno, única sombra 2048², todos los vértices de objetos que proyectan sombra dentro del frustum en READY, envolventes exteriores de las cajas, chaflanes presentes, cilindros de 32 segmentos, cristal sin sombras, texturas 256², ausencia de bump, cero sprites de cartelería, cinco botones, cuadrícula y resize: conformes.
- DPR emulado 3 → renderer 2; DPR emulado 1.25 → renderer 1.25 tras redimensionar. Sin pageerror en ese ensayo.
- Regresión funcional con reloj original a 640×480: **43 PASS y 2 FAIL, salida 1**. AUTO 7/7, 4 OK→A/3 NOK→B, PIEZA, START/STOP SIM/HMI, RESET, pausa/reanudación SIM, F01/F02, congelación del diagnóstico, rearme, recuperación, tipos de datos y posiciones por fase: PASS. Las aserciones de posiciones y tipos se ejecutaron sobre toda la secuencia muestreada antes de reducir las muestras persistidas.
- Los dos FAIL son los criterios de ausencia de errores JavaScript durante AUTO y globalmente: **159 pageerror**. Los ejemplos registrados muestran `Cannot read properties of undefined (reading 'id')` en refreshUX durante el intervalo con phase=7. Es el defecto original documentado; no se convierte en PASS ni se corrige aquí. Se conserva el contador total y una selección de stacks/observaciones, sin afirmar que las muestras de sondeo sean simultáneas con cada excepción.
- Código funcional y HTML de UI idénticos a V0; animación idéntica salvo DPR en resize. No hay imports nuevos. SHA256 de V0, sintaxis Python y git diff --check: comprobados.

Informes seleccionados: [configuración](../tests/evidence/visual-v1.2/config-results.json), [regresión funcional](../tests/evidence/visual-v1.2/functional-results.json) y [procedencia/hash de capturas](../tests/evidence/visual-v1.2/captures.json). Los tres identifican el mismo SHA256 del HTML modificado. El resto de artefactos regenerables queda en test-results/ sin versionar.

| General | Alimentación | Inspección | Expulsión | Armario |
| --- | --- | --- | --- | --- |
| [Captura](../tests/evidence/visual-v1.2/view-all.png) | [Captura](../tests/evidence/visual-v1.2/view-feed.png) | [Captura](../tests/evidence/visual-v1.2/view-inspect.png) | [Captura](../tests/evidence/visual-v1.2/view-sort.png) | [Captura](../tests/evidence/visual-v1.2/view-cab.png) |

### Rendimiento observado

3983 intervalos rAF: **3.72 FPS** por intervalo medio; media 269.03 ms, p50 266.60 ms, p95 533.30 ms, máximo 1066.60 ms. Último renderer.info: **154 draw calls, 11512 triángulos, 4 texturas y 110 geometrías**. El recuento del renderer corresponde al último render, no al total de todos los pases de sombra ni a bytes de VRAM.

La cadencia fue baja incluso a 640×480 con SwiftShader. No se presenta como una mejora de FPS ni se extrapola a una GPU de usuario. El entorno/reflejos, luces y mayor detalle tienen coste; bajar draw calls y texturas no garantiza menor tiempo de frame. Los intervalos incluyen interacción, capturas y CDP, y no son tiempo exclusivo de GPU. No se establece una comparación cuantitativa con V0 a 960×640 porque la resolución difiere. Con el límite original dt≤.04, esta cadencia alarga el ciclo en tiempo de pared; no se alteró ese límite para ocultarlo.

Las cinco capturas de vistas a 960×640 provienen del HTML final de este paquete. Se han revisado visualmente: reflejos y chaflanes dan lectura a rodillos, bastidor y armario; el cristal deja ver la cinta sin una sombra opaca; la cuadrícula queda en segundo plano; no aparecen los carteles. Los presets existentes siguen recortando algunos elementos en primer plano y la HMI ocupa parte de la imagen: no se cambian sus encuadres en este paquete.

Se interrumpió explícitamente un primer ensayo funcional a 960×640 durante la segunda pieza por su coste en SwiftShader (salida 130). Solo se usan de ese ensayo las cinco capturas ya completadas; no se presenta como ejecución funcional completa. Se reinició el ensayo funcional a 640×480, con el reloj real del simulador y mayor timeout de espera. Los FPS de resoluciones diferentes no son comparables directamente; tampoco representan una GPU de usuario. El muestreo rAF empieza después del arranque, por lo que no mide el coste inicial de generar PMREM.

## Límites y siguiente paquete

Conservar el defecto conocido de refreshUX durante intervalos entre piezas, pendiente de una corrección posterior autorizada. Este paquete no incluye una refactorización general, recuperación de trayectorias previas ni cambios de lógica. Contacto del expulsor, alimentación por gravedad, colisiones, comportamiento físico real, matriz móvil/HiDPI visual completa y medición en GPU de usuario quedan fuera de esta entrega.
