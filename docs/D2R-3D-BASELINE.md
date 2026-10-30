# Baseline V0 · Playwright + Chromium

## Alcance

Infraestructura de QA independiente del simulador. No modifica HTML, funciones, fases, duraciones, clasificación, contadores, señales ni Safety. Las acciones se realizan con botones reales de SIM/HMI. La observación interna usa Chrome DevTools Protocol (CDP), sin invocar funciones de negocio.

La auditoría anterior (`D2R-3D-AUDIT.md`) documentó un ensayo acelerado e instrumentado. Sus resultados son históricos: no acreditan ausencia de errores durante el ciclo real. Este baseline lo sustituye como procedimiento de validación y conserva sus limitaciones a la vista.

## Referencia inmutable

`tests/baseline/V0.html` contiene exactamente los bytes del HTML original en `6e23c34bdef6a1f82f6b6013d50c51df48405f8a`.

SHA256: `fb09ee9b8ef9ee635ea138283f1faaaf2d75b0ad9025a05395d77715948a76b3`.

El manifiesto `tests/baseline/V0.sha256` y la constante del runner permiten detectar cualquier alteración. No actualizar V0 al aprobar futuros cambios visuales. Git conserva su historia; no es una protección contra un usuario que deliberadamente cambie archivo y hash. El runner aborta si V0 deja de coincidir.

```sh
sha256sum -c tests/baseline/V0.sha256
git show 6e23c34bdef6a1f82f6b6013d50c51df48405f8a:D2R-3D-001_Prototipo_Funcional_v11.html | sha256sum
```

El HTML funcional en la raíz permanece sin cambios. Las futuras pruebas pueden seleccionar ese archivo con `--target`; nunca deben reemplazar V0.

## Instalación y ejecución

Requiere Python 3.10+, acceso a jsDelivr para Three.js 0.164.1, Playwright y Chromium. Desde la raíz del repositorio:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/run_baseline.py
```

En Linux sin bibliotecas de sistema, la instalación de Chromium puede requerir `python -m playwright install --with-deps chromium` y privilegios para el gestor de paquetes. Alternativamente, usar Chromium ya instalado:

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/run_baseline.py
```

Para comprobar versiones futuras sin alterar la referencia:

```sh
CHROMIUM_PATH=/usr/bin/chromium python tests/run_baseline.py \
  --target D2R-3D-001_Prototipo_Funcional_v11.html \
  --output test-results/current --timeout 600
```

El servidor HTTP inicia y se cierra automáticamente en `127.0.0.1` con puerto asignado por el SO. No requiere proceso previo ni puerto fijo. La respuesta HTML no se intercepta ni reescribe. Se descarga el módulo Three.js y se sirve su contenido exacto al interceptar únicamente la URL CDN; su SHA256 se registra. Esto no prueba la disponibilidad del CDN desde la red de un usuario.

`--timeout` limita cada espera de escenario en segundos reales; no cambia el reloj de simulación. La ejecución puede tardar varios minutos con renderizado por software. Salida 0: todas las comprobaciones PASS; salida 1: al menos un FAIL, incluidos errores JavaScript. No hay xfail que convierta un defecto conocido en éxito.

## Adaptador de observación

`tests/observer.js` es una función de lectura separada del HTML. El runner coloca un breakpoint CDP antes del arranque, captura una referencia a esa función en el ámbito del módulo y elimina el breakpoint inmediatamente. Después continúa con el reloj Three.Clock y requestAnimationFrame originales. La pausa inicial del debugger sucede antes de crear el reloj.

El observador lee estado, coordenadas, señales, texto del Watch, cámaras y renderer.info. No llama a update/reset/processValues ni escribe estado del simulador. Los clics Playwright son las únicas órdenes de operación. Un callback requestAnimationFrame adicional registra intervalos de presentación sin reemplazar animate ni el reloj. Existe perturbación por CDP, sondeo, capturas y software rendering; se declara al interpretar rendimiento.

El adaptador depende de los nombres internos y de la línea de arranque para obtener el ámbito CDP. Si cambian, debe adaptarse el observador; no se debe inyectar un reemplazo funcional para forzar un PASS.

## Cobertura

- AUTO completo, orden del lote, 7 piezas, 4 OK y 3 NOK; muestreo de cada descarga en PUSH_RETRACT, posición final y DI_ExitA/DI_ExitB.
- Modo PIEZA mediante HMI; START/STOP tanto SIM como HMI; RESET SIM durante marcha y RESET HMI parado.
- Pausa/reanudación desde SIM: congelación de elapsed y posiciones, y avance al reanudar. **HMI no tiene control de pausa**: no se inventa ni se añade.
- F01/F02, alarma, enclavamiento, congelación BOOL/numérica, rearme y pieza de recuperación sin fallo.
- BOOL e inventario INT/DINT/REAL/TIME, valores presentados y duraciones declaradas.
- Muestreo de coordenadas de pieza, gate y arm por fase; envolventes de recorrido y destinos. Estas comprobaciones no prueban contacto, colisiones o física real.
- Cinco vistas, capturas READY, inspección, descarga, lote final y fallos. Son evidencias de estados observados, no comparación pixel-perfect aprobada ni validación de todos los ángulos.
- pageerror durante toda la ejecución, con contador total y hasta 12 ejemplos con stack y último estado observado.
- Intervalos rAF y renderer.info cuando están disponibles.

Las muestras persistidas se reducen para evitar trazas voluminosas; las aserciones de la ejecución final del runner procesan las muestras antes de reducirlas. Si un escenario termina por excepción, se guarda el informe parcial y se marca FAIL.

## Evidencias y limitaciones

Resultados seleccionados en `tests/evidence/`; todos los artefactos regenerables por defecto en `test-results/`, ignorado por Git junto con entornos, node_modules y cachés. No versionar trazas completas ni todas las capturas de cada ejecución.

FPS estimado = 1000 / media de intervalos del observador rAF; se registran media, p50, p95 y máximo de intervalo. No son tiempos exclusivos de GPU ni tiempos exclusivos del render del simulador. Incluyen interacción, capturas y CDP; renderer.info representa el último render, no el coste consolidado de todos los pases de sombra. Headless con SwiftShader no equivale al rendimiento de una GPU de usuario. Texturas es un recuento, no bytes de VRAM.

Pendientes fuera del alcance mínimo: móvil/HiDPI, navegadores adicionales, prueba prolongada, medición GPU real, contacto físico, comparación visual aprobada y STOP en cada fase/intervalo. No existe PLC real ni validación funcional Safety.

## Resultado observado

Ejecución real completada el 2026-10-30 con Playwright 1.62.0 y Chromium 154.0.8037.57, viewport 960×640, deviceScaleFactor=1. Comando: `CHROMIUM_PATH=/usr/bin/chromium python tests/run_baseline.py`. **Código de salida 1: baseline FAIL**, sin ocultar ni corregir el defecto.

- AUTO terminó 7/7, 4 OK/3 NOK; los siete destinos y las siete fases fueron observados y comprobaron PASS.
- PIEZA, START/STOP desde SIM/HMI, ambos RESET en sus condiciones, pausa/reanudación SIM, F01/F02, snapshots y recuperación de una pieza tras cada fallo: PASS.
- 18 BOOL y 10 registros numéricos presentes. Envolventes y sentido de posiciones por fase, carrera gráfica de actuadores, lote/duraciones declarados y valores tipados: PASS en las muestras conservadas.
- Las validaciones adicionales de posiciones/tipos de `validate_observations.py` se ejecutaron a posteriori sobre las muestras reducidas del informe real, sin volver a simular. Se declara ese alcance en `observation_validation_scope`. El runner final integra esas mismas aserciones antes de reducir muestras en futuras ejecuciones; no se afirma una segunda ejecución completa de esa integración.
- Total en el informe seleccionado: 43 PASS y 2 FAIL. Los dos FAIL son ausencia de errores JS durante AUTO y ausencia de errores JS global, ambos por el mismo defecto original.

### Defecto original reproducido: refreshUX durante intervalo

145 eventos pageerror, todos durante el AUTO de esta ejecución; se conservan 12 ejemplos y el contador total. Primer mensaje:

```text
TypeError: Cannot read properties of undefined (reading 'id')
    at refreshUX (.../tests/baseline/V0.html:327:875)
    at animate (.../tests/baseline/V0.html:329:361)
```

El informe conserva observaciones con `phase=7`, `partIndex=1`, `running=true`, `betweenCycles=0.9` (y siguientes intervalos observados). El arreglo `phases` tiene índices 0…6. Tras contabilizar una pieza en AUTO, update deja phase en 7 durante la espera entre piezas; refreshUX intenta leer `phases[phase].id`. La primera muestra asociada al evento puede ser del frame anterior, por el sondeo: las muestras específicas del intervalo son la evidencia complementaria. No se atribuye a cada evento un estado capturado en el mismo instante.

`animate` agenda el siguiente requestAnimationFrame antes de ejecutar update/refreshUX, por lo que el ciclo continúa aunque la actualización de UX lance errores. Esto explica que completar el lote y estar libre de errores sean criterios independientes. El número de eventos depende del ritmo de frames, no constituye un valor fijo esperado. **No corregido en esta etapa.**

### Rendimiento observado en este entorno

3869 intervalos rAF: media 153.56 ms, p50 150.00 ms, p95 299.90 ms, máximo 616.70 ms; estimación por intervalo medio: 6.51 FPS. Último renderer.info: 161 draw calls, 7214 triángulos, 152 geometrías y 8 texturas. Incluye escenarios, capturas y CDP, con SwiftShader: **no es un benchmark de GPU de usuario ni tiempo exclusivo de render**. El dt original está limitado a .04 s, de modo que a esta cadencia el tiempo simulado avanza más lento que el real. No se ajustó el reloj para compensarlo.

### Evidencias seleccionadas

[Informe JSON](../tests/evidence/V0-results.json), cinco capturas de vistas, DISCHARGE y F02 en [tests/evidence](../tests/evidence/). Hashes de capturas en `tests/evidence/screenshots.sha256`. Se revisó visualmente la captura de DISCHARGE; las cinco vistas fueron ejercitadas y capturadas, sin afirmar aprobación visual exhaustiva de todas ellas. F01, inspección y fin de lote también se capturaron durante la ejecución, pero se dejan como artefactos regenerables sin versionar. Las imágenes no prueban contacto físico real.

El HTML funcional y V0 siguen coincidiendo con el hash original. No se cambiaron lógica PLC, Safety, fases, duraciones, señales, clasificación ni contadores. El ensayo acelerado anterior se retira del árbol activo, conservando sus referencias históricas en la auditoría.
