# 01 · Especificación funcional

**Estado:** borrador didáctico v0.2 · revisión pendiente
**Objetivo:** convertir el escenario del documento 00 en comportamientos y criterios que puedan revisarse antes de diseñar o programar.

> El simulador permite observar una propuesta de secuencia. Los puntos descritos aquí no son requisitos firmados ni pruebas de una máquina física.

## Entradas y alcance

- Entrada principal: documento 00 · Brief del cliente y sus preguntas pendientes de producto, producción, inspección, interfaces y Safety.
- Incluye: alimentación individual, transporte, captura de inspección, decisión OK/NOK, descarga y operación desde HMI.
- No incluye: algoritmo de visión real, elección de sensores, cálculo de capacidad, hardware elegido ni funciones Safety implementadas.
- La secuencia actual del HTML es una referencia didáctica; sus duraciones no son consignas de producción.

## Comportamiento observable de referencia

| Fase del prototipo | Duración del modelo | Comportamiento representado |
| --- | ---: | --- |
| `FEED` | 0,8 s | Libera una pieza desde el alimentador. |
| `TRAVEL_VISION` | 2,2 s | Transporta la pieza a inspección. |
| `INSPECT` | 1,5 s | Detiene la cinta y presenta el disparo/captura lógica. |
| `TRAVEL_SORT` | 1,9 s | Transporta la pieza hacia clasificación. |
| `SORT_STOP` | 0,5 s | Detiene la pieza en la posición de clasificación. |
| `DISCHARGE` | 2,2 s | Representa expulsión OK o avance hacia salida B. |
| `PUSH_RETRACT` | 1,1 s | Representa retorno y confirmación de salida. |

El lote fijo `OK, NOK, OK, NOK, OK, OK, NOK` solo verifica las dos rutas: `OK → A` y `NOK → B`. No define una proporción de calidad real.

## Secuencia funcional desglosada

| Paso | Entrada/condición de avance | Acciones representadas | Confirmación o salida |
| --- | --- | --- | --- |
| Preparado | RESET completado y condiciones operativas disponibles. | No se ejecuta movimiento; se espera START. | Estado READY; lote preparado. |
| `FEED` | START y pieza disponible en el modelo. | Pulso/ventana de alimentación; la pieza inferior sale del cargador. | Pieza activa sobre cinta. |
| `TRAVEL_VISION` | Alimentación termina. | Cinta en marcha hacia inspección. | `DI_InspectionPresent` pasa a 1 en la fase siguiente. |
| `INSPECT` | Pieza en posición de cámara. | Cinta parada; `DO_VisionTrigger` activo; cámara lógica lista. | `InspectionDone`, `InspectionValid` y resultado simulados. |
| `TRAVEL_SORT` | Resultado registrado en el modelo. | Cinta vuelve a transportar la pieza. | Llegada a zona de clasificación. |
| `SORT_STOP` | Pieza en posición de clasificación. | Cinta parada; resultado ya conocido por el ciclo. | Posición de clasificación simulada. |
| `DISCHARGE` | Resultado OK/NOK disponible. | OK: expulsor mueve la pieza por transferencia A. NOK: cinta la conduce hacia B. | Pieza abandona la posición de clasificación. |
| `PUSH_RETRACT` | Fin de la descarga OK o confirmación de salida B. | OK: expulsor retorna; NOK: termina la salida de cinta. | Contador actualizado y ciclo completo. |
| Entre piezas | Fin de una pieza y lote con unidades pendientes. | Espera de `0,9 s` en el reloj del prototipo. | Se inicia la pieza siguiente o se queda detenido por FIN DE PIEZA. |

Los nombres y tiempos de fase anteriores son los del modelo de Three.js. La máquina real necesitará transiciones por sensores y requisitos del cliente; no se debe programar una máquina real con transiciones basadas solo en temporizadores.

### Secuencia de señales simuladas

| Fase | Cinta `DO_ConveyorRun` | `DO_FeederValve` | `DO_PusherValve` | Visión lógica |
| --- | --- | --- | --- | --- |
| `FEED` | 0 | Activa durante parte de la fase | 0 | Sin captura |
| `TRAVEL_VISION` | 1 | 0 | 0 | Sin captura |
| `INSPECT` | 0 | 0 | 0 | Trigger activo; presencia 1; ready simulado 1 |
| `TRAVEL_SORT` | 1 | 0 | 0 | Resultado ya registrado por el lote |
| `SORT_STOP` | 0 | 0 | 0 | Sin nuevo disparo |
| `DISCHARGE` OK | 0 | 0 | 1 | Resultado OK retenido en el ciclo |
| `DISCHARGE` NOK | 1 | 0 | 0 | Resultado NOK retenido en el ciclo |
| `PUSH_RETRACT` OK | 0 | 0 | 1 | Salida A representada |
| `PUSH_RETRACT` NOK | 0 | 0 | 0 | Salida B representada |

`VisionReady`, `InspectionDone`, `InspectionValid`, `VisionOK` y `SafetyReady` son señales virtuales de la simulación. La cámara lista y el permiso Safety no representan feedback de equipos reales.

## Matriz de mandos y prioridad

| Mando | Estado permitido en el prototipo | Efecto observado | Definición pendiente para máquina real |
| --- | --- | --- | --- |
| START | READY | Arranca el lote AUTO o una pieza en PIEZA. | Antirrebote, confirmación, condiciones de arranque y reset de orden. |
| FIN DE PIEZA / STOP | RUN | Marca parada solicitada; deja concluir la pieza activa. | Categoría de parada, reacción ante fallo y parada de accionamientos. |
| AUTO / PIEZA | READY | Selecciona ciclo continuo o una unidad por START. | Permiso de cambio de modo y tratamiento de cambio durante proceso. |
| RESET HMI | READY | Reinicia contadores/estado de proceso del modelo. | Alarmas que requieren reconocimiento, origen del reset y prevención de rearranque. |
| PAUSA simulador | RUN | Congela el reloj lógico y la animación. | No trasladar directamente; definir pausa operacional y análisis de riesgo. |
| RESET SIM | Cualquier estado | Reinicia toda la escena de demostración. | No existe equivalente como mando de máquina. |

El orden de diseño recomendado para el programa real es: adquirir entradas → validar comunicaciones y permisos → procesar mandos → actualizar estados/equipos → evaluar transiciones → calcular salidas → publicar diagnósticos. La cadena no sustituye la arquitectura Safety.

## Modos y mandos

- `AUTO`: procesa el lote de demostración de forma continua.
- `PIEZA`: una orden START solicita una pieza; repetir START solicita la siguiente.
- `FIN DE PIEZA`: STOP solicita completar la pieza activa antes de quedar detenido.
- `RESET HMI`: disponible con la máquina detenida; reinicia el estado operativo del modelo.
- `PAUSA` del simulador: congela la animación y el reloj de simulación. No equivale a una pausa segura de una máquina real.
- `RESET SIM`: reinicia el entorno de demostración; no es una orden PLC.

## Criterios propuestos

| ID | Criterio revisable | Trazabilidad | Estado |
| --- | --- | --- | --- |
| `TC-001` | Una pieza se presenta por ciclo, sin duplicación visual. | `REQ-001` | Propuesto; simulación observable |
| `TC-002` | La pieza llega a inspección y la cinta se detiene durante `INSPECT`. | `REQ-002` | Propuesto; captura real pendiente |
| `TC-003` | El resultado aceptado conduce a A o B según el lote. | `REQ-003` | Rutas presentes en el prototipo |
| `TC-004` | AUTO y PIEZA respetan el número de órdenes indicado. | `REQ-004` | Propuesto para revisión de cliente |
| `TC-005` | FIN DE PIEZA completa el ciclo en curso y luego detiene nuevos ciclos. | `REQ-005` | Presente como comportamiento simulado |
| `TC-006` | HMI presenta modo, estado y contadores comprensibles. | `REQ-006` | Borrador; contenido final pendiente |
| `TC-007` | El intercambio de visión se confirma antes de usar un resultado. | `REQ-008` | Requisito propuesto; interfaz real no existe |

### Procedimiento de prueba por requisito

1. Registrar versión de software, modo, lote, pieza e índice inicial.
2. Capturar valores del Watch antes de START y durante cada fase relevante.
3. Confirmar estado de cinta en INSPECT, resultado de visión y ruta de descarga.
4. Conciliar pieza procesada, resultado y contador; repetir con RESET para confirmar estado inicial.
5. Marcar evidencia como **SIM** si procede del HTML, **PLC** si procede de observación online, o **FÍSICA** si se midió en el equipo real.

La evidencia actual solo puede ser **SIM**. El protocolo final necesitará criterios numéricos y firmas de aceptación acordadas con el cliente.

## Decisiones pendientes

Definir el producto y sus referencias, defectos y límites OK/NOK; producción objetivo; política de falta de pieza o atasco; confirmación física de cada salida; y comportamiento requerido ante pérdida de comunicación. El cliente y los responsables de proceso, mantenimiento y Safety deben revisar esos puntos antes de congelar la especificación.

**Artefacto de salida:** especificación funcional aprobada y matriz de trazabilidad.  
**Siguiente etapa:** diseño mecánico, eléctrico y neumático. Los tiempos mostrados no se trasladan automáticamente al diseño real.
