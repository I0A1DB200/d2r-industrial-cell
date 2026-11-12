# 01 · Especificación funcional

**Estado:** borrador didáctico v0.1 · revisión pendiente  
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

## Decisiones pendientes

Definir el producto y sus referencias, defectos y límites OK/NOK; producción objetivo; política de falta de pieza o atasco; confirmación física de cada salida; y comportamiento requerido ante pérdida de comunicación. El cliente y los responsables de proceso, mantenimiento y Safety deben revisar esos puntos antes de congelar la especificación.

**Artefacto de salida:** especificación funcional aprobada y matriz de trazabilidad.  
**Siguiente etapa:** diseño mecánico, eléctrico y neumático. Los tiempos mostrados no se trasladan automáticamente al diseño real.
