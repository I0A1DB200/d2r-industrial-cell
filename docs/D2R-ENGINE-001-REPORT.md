# D2R ENGINE-001 — PLC Engineering Mode

## Alcance y base

Cambios preparados en `feature/d2r-engineering-mode`, creada desde `visual/industrial-v1.3` en el commit `1886f78b022cd469d391cd711c1936db948345ad`. El trabajo queda en una rama de revisión; no modifica `main` ni la web principal de Digital2Real.

Esta etapa retira los mecanismos de inyección artificial F01/F02 del simulador actual. No incorpora módulos formativos ni nuevas condiciones de alarma.

## Archivos modificados

- `D2R-3D-001_Prototipo_Funcional_v11.html`
- `tests/protected_contract.py`
- `tests/check_visual.py`
- `tests/check_transfer.py`
- `tests/check_controls.py`
- `tests/controls-observer.js`
- `tests/transfer-observer.js`
- Este informe.

La referencia V0 en `tests/baseline/V0.html`, su SHA256 y su runner histórico `tests/run_baseline.py` permanecen intactos. Las pruebas dedicadas a F01/F02 que operaban sobre el simulador actual se retiraron de `check_transfer.py`; las comprobaciones históricas de V0 se conservan en su runner.

## Funcionalidades retiradas

Se eliminaron el botón y panel de averías, el selector F01/F02, su botón de rearme y los mensajes específicos de inyección. También se retiraron las ramas que forzaban timeout de cámara o falta de confirmación del expulsor, el latch que congelaba el ciclo para diagnóstico y la congelación de valores Watch asociada a esos snapshots.

No quedan selectores ocultos de avería en la interfaz actual. La prueba de controles ahora comprueba que SIM RESET conserva el panel abierto que el usuario ya tenía seleccionado y no abre un panel de diagnóstico; HMI RESET conserva su comportamiento de reset detenido y cierre del panel actual.

## Funcionalidades y datos conservados

Se mantienen START, STOP al final de pieza, RESET, AUTO/PIEZA, pausa/reanudación, lote continuo, los siete resultados predefinidos, contadores, clasificación OK → A y NOK → B, movimientos de alimentación e inspección, trayectoria NOK y secuencia original. No se alteraron fases, duraciones, señales normales, transforms 3D ni Safety.

PLC Watch conserva los 7 DI, 4 DQ y 5 estados BOOL normales, además de los 9 valores de proceso: 2 INT, 3 DINT, 3 REAL y 1 TIME. Se conservan filtros, selección de sensor y enfoque de cámara. El panel Alarmas y la función genérica de severidad siguen disponibles; no se añadieron condiciones nuevas ni se simularon alarmas de proceso.

## Variables retiradas y motivo

- `fault`: selección local del escenario de inyección F01/F02.
- `faultLatched`: latch usado exclusivamente para detener la secuencia por esas inyecciones.
- `numericFrozen`: bloqueo de actualización que retenía snapshots de diagnóstico.
- `Diag_VisionTimeout` y `Diag_PusherMismatch`: BOOL exclusivos de las dos inyecciones.
- `DB_VisionTimeout`: TIME constante que solo documentaba el timeout artificial F01.
- `latchFault()`: captura de snapshots y mensajes asociados a escenarios artificiales.

Las señales de cámara, expulsor, seguridad y demás variables normales mantienen nombres, tipos, escalas y fórmulas. La conversión de `DB_PieceX` y `DB_PusherPos` permanece igual que en V0; la comparación estática se realiza en el contrato de protección.

## Pruebas y resultados

**Comprobaciones estáticas ejecutadas en esta sesión**

- PASS — sintaxis del módulo JavaScript inline mediante parseo V8, retirando la línea de import de Three.js para el parseo. Esto no ejecuta la página ni valida la carga de CDN.
- PASS — ausencia en el HTML actual de `faultSelect`, `pane-faults`, `faultReset`, tags diagnósticos, latch y estados exclusivos.
- PASS — comparación de lote, fases, registros normales, conversiones Watch, I/O, transición de ciclo y trayectoria NOK contra V0, normalizando solo los campos exclusivos de F01/F02.
- PASS — equivalencia de las fórmulas y unidades de `DB_PieceX` y `DB_PusherPos` contra V0.

**Cobertura Playwright adaptada, ejecución pendiente**

El entorno de ejecución no estuvo disponible: las llamadas a comandos devolvieron “No usable execution environment is available”. Por ello no pude iniciar Chromium ni ejecutar las pruebas. No registro como PASS resultados que no se han medido.

Quedan pendientes las verificaciones en navegador de carga y errores JavaScript, AUTO completo (7 piezas: 4 OK/3 NOK), PIEZA, mandos SIM/HMI, Watch y tipos en vivo, selección 3D, alarmas, reset, Safety y posiciones numéricas durante el ciclo. Las pruebas de geometría, alimentador, controles y transferencias siguen en el repositorio para ejecutarse allí.

Comandos previstos con las dependencias de `tests/requirements.txt` instaladas:

```bash
python tests/check_visual.py
python tests/check_controls.py
python tests/check_feeder.py
python tests/check_transfer_geometry.py
python tests/check_transfer.py
```

El runner `tests/run_baseline.py` continúa reservado para la referencia V0 inmutable y no sustituye las pruebas del HTML actual.

## Captura y riesgos pendientes

**Captura de la nueva interfaz: pendiente.** Chromium no estuvo disponible, por lo que no generé ni adjunté una captura falsa o histórica. `check_controls.py` guarda capturas por viewport cuando se ejecuta correctamente.

El riesgo principal antes de integrar es la falta de validación dinámica del cambio en Chromium. La aceptación de ENGINE-001 queda pendiente de ejecutar las pruebas Playwright y revisar la captura resultante. La sintaxis y las equivalencias indicadas arriba son comprobaciones de código, no evidencia de comportamiento físico ni de rendimiento GPU.
