# D2R-3D-001 · Auditoría de la base v11

> Documento histórico. El ensayo instrumentado descrito aquí no comprobaba todo el ciclo con el reloj original. Para ejecución actual y errores de refreshUX consultar [D2R-3D-BASELINE.md](D2R-3D-BASELINE.md).

Fecha: 2026-10-30 (Europe/Madrid). Clasificación: EXPERIENCE; auditoría visual y funcional del prototipo, sin cambios de implementación.

## Objetivo y estado inicial

Establecer una base verificable antes de reconstruir el alimentador por gravedad y el expulsor OK por contacto. Éxito de esta etapa: HTML idéntico al original, auditoría y evidencias versionadas y publicadas en la rama autorizada.

- Repositorio: `I0A1DB200/d2r-industrial-cell`.
- Rama inicial: `main`, árbol limpio y sincronizado con `origin/main`.
- Base: `6e23c34bdef6a1f82f6b6013d50c51df48405f8a`.
- Rama de trabajo: `visual/industrial-v1.2`, creada desde esa base; no existía localmente ni en origin al comprobarla.
- Inventario inicial: HTML y README de dos líneas. Sin AGENTS.md, tests, manifiesto de dependencias, documentación técnica adicional ni comandos de QA propios.
- SSOT: `D2R-3D-001_Prototipo_Funcional_v11.html`. El alcance de esta etapa se limita a `docs/`.

## Referencia original inmutable

Archivo en la base: [HTML original en GitHub](https://github.com/I0A1DB200/d2r-industrial-cell/blob/6e23c34bdef6a1f82f6b6013d50c51df48405f8a/D2R-3D-001_Prototipo_Funcional_v11.html).

SHA256 de sus bytes:

```text
fb09ee9b8ef9ee635ea138283f1faaaf2d75b0ad9025a05395d77715948a76b3
```

Verificación reproducible, sin duplicar el HTML:

```sh
git show 6e23c34bdef6a1f82f6b6013d50c51df48405f8a:D2R-3D-001_Prototipo_Funcional_v11.html | sha256sum
sha256sum D2R-3D-001_Prototipo_Funcional_v11.html
git diff 6e23c34bdef6a1f82f6b6013d50c51df48405f8a -- D2R-3D-001_Prototipo_Funcional_v11.html
```

Ejecutado: ambos hashes coinciden; diff vacío. El commit base conserva la referencia recuperable sin añadir una segunda copia editable.

## Entorno y método

Node v24.19.0 disponible; Python y Playwright ya instalados, Chromium en `/usr/bin/chromium`. Se sirve por HTTP local y se usa Chromium headless con SwiftShader; no se añade dependencia de producción ni se cambia el HTML.

Three.js 0.164.1 se importa desde jsDelivr. Para el ensayo se descargó ese mismo módulo y se interceptó exclusivamente su URL para servir los bytes locales. Esto comprueba ejecución con esa versión, pero no disponibilidad del CDN en el navegador del usuario.

Dos capas de comprobación:

1. HTML sin instrumentar: arranque WebGL, errores JavaScript, START, pausa/reanudación, SIM RESET, cinco vistas, apertura de Watch y captura revisada visualmente a 1440×900.
2. Respuesta HTTP instrumentada solo en memoria: se exponen estado y funciones existentes y se suspende requestAnimationFrame después de su primer render. Se invoca `update(.02)` repetidamente para comprobar el ciclo sin esperar tiempo real. No se reimplementan fases ni se escriben cambios en el archivo. Esta capa no demuestra fluidez de animación ni duración de reloj de pared.

Evidencia estructurada: [resultado histórico](https://github.com/I0A1DB200/d2r-industrial-cell/blob/28effc20c4e93056afe37ab19ad53aafe5061612/docs/qa/baseline-results.json). Harness: [harness histórico retirado](https://github.com/I0A1DB200/d2r-industrial-cell/blob/28effc20c4e93056afe37ab19ad53aafe5061612/docs/qa/audit-baseline.py). Ejecución histórica (ya retirada): `python docs/qa/audit-baseline.py` (requiere Python, Playwright y Chromium existentes; descarga el módulo de jsDelivr y usa un directorio temporal). Su salida JSON permite repetir y comparar las aserciones; no instala paquetes. La primera ejecución del smoke necesitó esperar a que el siguiente frame actualizara la HMI tras pulsar pausa; se corrigió la sincronización del ensayo, sin cambiar el producto.

## Geometría y representación

Inspección estática del HTML, contrastada con vista general en Chromium:

- Ejes: cinta hacia +X; expulsor hacia −Z. Primitivas BoxGeometry, CylinderGeometry de 18 segmentos, esferas de marcadores y cono de visión; sin CAD, colisiones ni solver físico.
- Bastidor, cinta, rodillos, patas, cerramiento transparente, cámara, armario, rampa A y cajas A/B construidos en unidades gráficas. No son dimensiones industriales validadas.
- Alimentador en X≈−2.98: ocho placas estáticas; pieza activa independiente en X=−3, Y=1.36. La pila no disminuye con el lote de siete. FEED mueve lateralmente `gate`; no representa caída por gravedad.
- `part()` dibuja placas con cilindros negros superficiales para aparentar cinco orificios; no son taladros geométricos. El resultado NOK no procede de una medición de esos orificios.
- Expulsor: cuerpo fijo; grupo `arm` con vástago y pala. Pieza OK recorre −2.25 unidades en Z, mientras arm recorre −1.48 con el mismo easing: no hay contacto impuesto. La pala inicial en Z=.12 solapa la extensión de la pieza centrada en Z=0 (semifondo .19). Reconstrucción posterior debe revisar contacto, carrera y salida sin alterar señales ni tiempos.
- Caídas a cajas A/B y confirmaciones de salida son trayectorias y señales programadas. Al finalizar la pieza se oculta, no se acumula en cajas.

## Materiales, iluminación y cámaras

- MeshStandardMaterial compartidos: aluminio y acero con metalness .7–.77; cinta oscura rugosa; colores didácticos naranja, verde, rojo, azul y amarillo.
- Cristal MeshPhysicalMaterial transparente, opacity .105, DoubleSide, depthWrite false. Cono de visión transparente; riesgo de ordenación y solapes.
- HemisphereLight intensidad 2.3 y DirectionalLight 3.0; sombras PCFSoft 2048². ColorSpace SRGB, niebla 15–35; sin tone mapping explícito ni texturas PBR externas.
- Cámara Perspective 44°, near .08, far 100. Cinco presets: general, alimentación, inspección, clasificación y armario. Órbita manual por pointer, zoom limitado 2–20; sin OrbitControls ni transición interpolada entre presets.
- Carteles: CanvasTexture con supersampling 2, mipmaps, anisotropía hasta 16 y depthTest false. Permanecen visibles a través de objetos: posible superposición y alto consumo de textura en rótulos largos.
- Revisión visual: panel Watch tapa parte derecha de la máquina/salida B; algunos carteles se solapan. No se ha validado legibilidad móvil ni todas las oclusiones desde cada ángulo.

## Ciclo y controles: contrato a conservar

Secuencia predefinida `OK,NOK,OK,NOK,OK,OK,NOK`: cuatro OK → A lateral; tres NOK → B final. La inspección publica el resultado al salir de INSPECT, no por decisión del alumno.

| Fase | Duración s | Motor / cámara |
| --- | ---: | --- |
| FEED | 0.8 | 0 / 0 |
| TRAVEL_VISION | 2.2 | 1 / 0 |
| INSPECT | 1.5 | 0 / 1 |
| TRAVEL_SORT | 1.9 | 1 / 0 |
| SORT_STOP | 0.5 | 0 / 0 |
| DISCHARGE | 2.2 | motor solo NOK / 0 |
| PUSH_RETRACT | 1.1 | 0 / 0 |

Suma nominal: 10.2 s por pieza; intervalo entre piezas .9 s, seis intervalos, total nominal 76.8 s. Cálculo estático, no cronometraje real. El frame limita dt a .04 s y procesa una transición por llamada; el tiempo simulado puede alejarse del tiempo real con baja frecuencia de frames.

| Función | Inspección y resultado ejecutado |
| --- | --- |
| AUTO / START | START inicia lote; lote completo probado: 7, OK=4, NOK=3, running=false. START tras lote completo reinicia por código; ese caso específico queda pendiente de ensayo. |
| PIEZA | Cambia solo parado; START ejecuta una pieza y se detiene. Probado: 1 OK, total 1. |
| STOP | Solicita fin de pieza, sin parada inmediata; probado durante transporte: total 1, stopped. |
| Pausa / reanudación | Congela update, no implica parada PLC ni Safety; probado estado sin avance durante 100 ticks y avance al reanudar. BOOL de motor puede permanecer activo durante pausa. |
| HMI RESET | Solo parado; reset(true) borra lote y cierra panel por código. Caso de borrado con lote parcial pendiente de ensayo directo. |
| SIM RESET | Disponible en marcha, resetea lote; ejecutado en smoke UI. |
| Rearmar simulación | reset(false), retiene contadores/índice, libera fallo y vuelve a FEED para repetir pieza. Probado tras F01/F02 en primera pieza; retención tras varias piezas pendiente. |

## HMI y PLC Watch

HMI READY/RUN/FAULT/SAFETY*, contadores y estado; paneles Watch/Alarmas/Averías, selección de fallos y filtros ALL/DI/DQ/DB. Watch presenta 18 BOOL y 10 registros numéricos; recuentos comprobados en navegador.

| Tipo presentado | Tags / significado |
| --- | --- |
| BOOL | 7 DI, 4 DO y 7 estados lógicos; conversión JavaScript Boolean. |
| INT | DB_SequenceStep (10…70 activo, 0 parado), DB_PieceIndex. |
| DINT | DB_CountOK, DB_CountNOK, DB_CountTotal. |
| REAL | DB_BeltSpeed 0/.10 m/s ilustrativo; DB_PieceX y DB_PusherPos derivados de objetos 3D, dos decimales. |
| TIME | DB_StageElapsed=elapsed×1000 y DB_VisionTimeout=1500 ms. |

Son tipos etiquetados didácticos sobre números JavaScript, sin memoria PLC, validación de rangos INT/DINT ni semántica de overflow/TIME de un fabricante. X se convierte linealmente a 0…800 mm; C02 convierte |arm.z|/1.48 a 0…200 mm. Velocidad mostrada no se calcula derivando la trayectoria suavizada.

Seis DI tienen marcadores 3D: InspectionPresent, RejectPosition, PusherRetracted, PusherExtended, ExitA y ExitB. MagazinePart y señales sin marcador muestran texto lógico al seleccionarse. La selección cambia escala/color y centro de cámara, no estado funcional. Filtros y correspondencia visual de cada marcador: inspeccionados en código, ensayo interactivo completo pendiente.

SafetyReady=true y LED SAFETY* siempre encendido; la interfaz declara permiso supuesto, sin Safety funcional implementada. Cerramiento visual sin ingeniería de seguridad. Esta auditoría no añade ni reinterpreta Safety.

## Alarmas, fallos, snapshots y recuperación

Alarmas muestran el evento actual, sin histórico persistente. Selector de fallo se lee al START; cambiarlo durante marcha no cambia `fault` hasta otro arranque.

- F01: al alcanzar 1.5 s de INSPECT sin handshake. Ensayo: phase=2, ningún contador incrementado; VisionTimeout=true, trigger=true, Done/Valid=false, conveyor=false. Watch numérico congelado en etapa 30, 1500 ms.
- F02: en pieza OK al alcanzar 2.2 s de DISCHARGE. Ensayo: phase=5, sin conteo; PusherMismatch=true, valve=true, Extended/Retracted=false, conveyor=false. Etapa 60, 2200 ms; posición gráfica ya casi en salida y carrera numérica ≈199.95 mm. Es falta de confirmación simulada, no demostración de atasco físico.
- Snapshots BOOL y texto numérico permanecieron iguales tras 100 ticks y otro START rechazado. Se conserva `VisionOK=true` previo en F02 aunque Done/Valid se fuerzan false; documentar como evidencia base, sin corregir ahora.
- Rearme probado en ambos: libera snapshot, seleccionar «Sin avería», START completa 4 OK/3 NOK. Dejar fallo seleccionado vuelve a inyectarlo por diseño. No se verificó pérdida de energía ni reconexión: no existen conexiones PLC reales.

## Acoplamientos y riesgos de regresión

| Acoplamiento | Riesgo / control para siguientes paquetes |
| --- | --- |
| update → piece, arm, gate | Trayectorias gráficas y fases comparten función. Limitar cambios a fórmulas visuales autorizadas; comparar fases, t, condiciones y contadores. |
| clearPiece/reset → posiciones | Actualizar representación debe seguir reseteándose sin duplicar piezas ni dejar mecanismos desplazados. |
| processValues → piece.x y arm.z | Cambiar pivotes/carrera puede cambiar Watch REAL aun sin tocar lógica. Mantener explícitamente la calibración original y validar valores. |
| refreshIO → phase/elapsed/mode | Sensores son derivados de estado y umbrales, no raycasts ni contacto. No sustituir condiciones al mejorar el contacto visual. |
| fault snapshot → io + processValues | Ensayar F01/F02 y congelación después de cada paquete. |
| Marcadores, etiquetas y presets → coordenadas | Cambiar geometría puede desalinearlos u ocultarlos; revisión visual específica. |
| mode / visionResult / workpieceBatch | Conservar propiedad de clasificación y revelado tras inspección. |

## Rendimiento

Render continuo incluso parado/pausado; Watch BOOL usa innerHTML en cada refresh, numéricos se publican en refreshIO y animate; HMI se actualiza cada frame. No hay reutilización sistemática de geometrías ni instancing. Sombras habilitadas en muchas primitivas y transparencias pueden costar más que el bajo número de polígonos sugiere.

Lectura ejecutada de renderer.info en render inicial del harness: 161 draw calls, 7214 triángulos, 152 geometrías, 8 texturas, 27 hijos directos de scene (no total de nodos). No son presupuesto GPU ni benchmark de FPS; no incluyen una medición consolidada de todos los pases de sombras. Pixel ratio limitado a 2 en arranque; resize ajusta tamaño/aspecto pero no recalcula pixel ratio.

Pendiente: FPS/tiempo CPU/GPU en hardware real, móvil y HiDPI, memoria de texturas y estabilidad prolongada. No se propone optimización general en esta etapa.

## Validación y siguientes paquetes

PASS ejecutado: arranque Chromium sin pageerror; smoke UI descrito; lote determinista; PIEZA; STOP; pausa/reanudación; F01/F02; snapshots; recuperación. Captura general revisada con las limitaciones visuales indicadas. No equivale a QA visual exhaustiva de todo el ciclo en tiempo real.

Pendientes: matriz móvil/responsive, todos los filtros y selección de marcadores, todos los ángulos y trayectorias frame a frame, STOP durante pausa/intervalo, F02 en NOK, retención de lote parcial tras fallos y rendimiento real. No se ocultan estas comprobaciones tras el PASS de los ensayos funcionales.

Siguiente paquete sugerido: representación del alimentador por gravedad; después contacto visual del expulsor OK. Ambos requieren instrucciones concretas posteriores. Mantener HTML sin cambios durante esta primera etapa; no eliminar HMI, Watch, alarmas, averías ni controles, y no modificar PLC, Safety, clasificación, tiempos, señales o contadores. No hay refactorización general, cambios binarios ni dependencias de producción en esta auditoría.
