# 03 · Componentes, hardware y mapa de E/S

**Versión:** 0.3 · inventario cotejado con el prototipo
**Estado:** revisión D2R pendiente · selección física y direcciones pendientes
**Objetivo:** traducir las funciones de la célula a una lista trazable de señales y equipos candidatos, sin confundir el Watch del simulador con una configuración PLC.

## 1. Alcance y fuente de verdad

Este documento distingue cuatro niveles:

| Nivel | Propietario previsto | Estado actual |
| --- | --- | --- |
| Animación y lógica didáctica | HTML del simulador | Implementado en software; los sensores y actuadores son proxies gráficos. |
| E/S de campo | PLC y dispositivos físicos | No implementadas ni cableadas. El inventario conceptual contiene 7 DI y 4 DO. |
| Inspección | Cámara Cognex como candidata | No hay cámara conectada ni handshake real. Cognex sigue siendo una posibilidad del caso. |
| HMI y trazabilidad | HMI más gateway/servicio de datos | HMI solo simulada. Gateway y base de datos externa propuestos, sin conexión. |

Los nombres `DI_`, `DO_` y `DB_` son identificadores del Watch del HTML. No asignan direcciones `%I`/`%Q`, no prueban que exista un DB de TIA y no describen señales medidas. El registro fuente del prototipo es `registry` para DI/DO/estados y `processRegistry` para valores numéricos.

La clasificación permanece como en el simulador: **OK → A** y **NOK → B**. La lista no altera fases, tiempos, contadores, señales ni Safety.

## 2. Mapa de E/S discretas

Las DI/DO del registro son BOOL lógicos. El nivel eléctrico, la tecnología y ubicación del sensor, el borne y la dirección física se definirán al seleccionar CPU, módulos y dispositivos.

### Entradas DI · 7 tags

| Tag | Función de campo que habría que resolver | Valor generado por el HTML | Decisión física pendiente |
| --- | --- | --- | --- |
| `DI_MagazinePart` | Detectar pieza en la salida del cargador; sensor de presencia candidato, sujeto a geometría y material. | BOOL: 1 mientras `FEED`; lo genera la fase, no un sensor. | Posición, tecnología final y diagnóstico; validar detección sobre aluminio. |
| `DI_InspectionPresent` | Confirmar pieza en la estación; fotocélula candidata, a validar con la superficie y el montaje. | BOOL: 1 durante `INSPECT`. | Modelo, soporte, repetibilidad, filtro y prevención de reflejos falsos. |
| `DI_RejectPosition` | Confirmar pieza detenida en clasificación. | BOOL: 1 en `SORT_STOP` y durante empuje OK. | Punto de detección y condición de liberación. |
| `DI_PusherRetracted` | Confirmar carro del expulsor en reposo. | BOOL: 1 salvo durante empuje y retorno; calculado por fase. | Sensor de fin de carrera y posición de montaje. |
| `DI_PusherExtended` | Confirmar expulsor extendido. | BOOL: 1 al final de extensión y en el primer tramo del retorno; calculado por fase. | Punto de actuación, histéresis y diagnóstico. |
| `DI_ExitA` | Confirmar salida A; sensor de presencia candidato en la trayectoria final. | BOOL: 1 en la fase final de una pieza OK. | Ubicación y criterio para evitar doble conteo. |
| `DI_ExitB` | Confirmar salida B; sensor de presencia candidato en la trayectoria final. | BOOL: 1 en la fase final de una pieza NOK. | Ubicación y criterio para evitar doble conteo. |

### Salidas DO · 4 tags

| Tag | Función de campo prevista | Valor generado por el HTML | Decisión física pendiente |
| --- | --- | --- | --- |
| `DO_ConveyorRun` | Petición de marcha a la interfaz del accionamiento; no alimenta directamente un motor. | BOOL: 1 en transporte y en el avance NOK hacia B. | Drive, interfaz eléctrica/red, permisos y realimentación. |
| `DO_FeederValve` | Orden lógica del actuador del alimentador. | BOOL: 1 mientras `FEED` y `q < 0.85`; cubre avance y retorno gráfico. | **Interfaz abierta:** el bit cubre avance y retorno gráficos. Definir la estrategia de válvula/salidas antes de seleccionar hardware. |
| `DO_PusherValve` | Orden lógica del expulsor lateral A. | BOOL: 1 durante `DISCHARGE` y `PUSH_RETRACT` OK. | **Interfaz abierta:** un solo BOOL no diferencia avance y retorno. Acordar semántica y número de salidas antes de elegir válvula o asignar canal. |
| `DO_VisionTrigger` | Solicitud de captura a la cámara. | BOOL: 1 durante `INSPECT`; no dispara equipo físico. | Trigger discreto o comando de red, polaridad y confirmación. |

Para los dos finales del cilindro pueden evaluarse sensores magnéticos si el actuador seleccionado admite imán en el émbolo. Las detecciones de pieza pueden requerir fotocélulas, pero se deben validar con muestras y geometría reales. Las DI del modelo representan fases, no sensores montados. La lista física deberá convertir cada función en dispositivo, ubicación, señal eléctrica, canal, borne, filtro/diagnóstico y prueba de aceptación.

## 3. Estados lógicos de inspección y Safety

Estos BOOL del Watch no están incluidos en las 7 DI/4 DO y no deben sumarse a módulos como si ya fueran bornes.

| Tag | Comportamiento exacto del modelo | Tratamiento en una integración futura |
| --- | --- | --- |
| `VisionReady` | Constante `true`. | Estado de cámara real por definir; no es una confirmación física actual. |
| `InspectionDone` | `true` desde la fase posterior a `INSPECT`. | Estado de protocolo futuro; definir pulso/nivel, reset y asociación a pieza. |
| `InspectionValid` | `true` desde la fase posterior a `INSPECT`. | Calidad/validez del resultado por definir con el handshake seleccionado. |
| `VisionOK` | Resultado del lote fijo, asignado por la simulación al completar la inspección. | Resultado de visión que el PLC deberá validar y asociar a la pieza. No representa todos los defectos ni una Cognex conectada. |
| `SafetyReady` | Constante `true` y señalada como virtual en el Watch. | No se cablea ni se usa como función Safety. La arquitectura Safety se mantiene separada y requiere su evaluación propia. |

En el HTML, `InspectionDone` e `InspectionValid` permanecen a 1 desde la fase 3 hasta el final de la pieza; no existe handshake externo, confirmación `ACK` ni código de error Cognex. El comportamiento de resultado inválido o cámara sin respuesta queda pendiente de definición en el proyecto de PLC.

## 4. Valores numéricos del Watch

Son monitorización derivada del estado gráfico, no canales de E/S. El prefijo `DB_` conserva el nombre didáctico, pero aún no define el bloque ni el tipo de dato de un DB de TIA.

| Tag | Tipo Watch | Valor/fórmula actual | Unidad visible y límite |
| --- | --- | --- | --- |
| `DB_SequenceStep` | INT | `0` detenido o entre piezas; durante fase activa: índice de fase × 10 + 10. | Código didáctico, no enum de PLC. |
| `DB_PieceIndex` | INT | Índice del lote + 1 mientras `running`; 0 detenido antes de iniciar. | En un intervalo puede identificar el siguiente índice lógico. |
| `DB_CountOK` | DINT | Contador acumulado de rutas OK completadas. | Piezas del lote virtual. |
| `DB_CountNOK` | DINT | Contador acumulado de rutas NOK completadas. | Piezas del lote virtual. |
| `DB_CountTotal` | DINT | `DB_CountOK + DB_CountNOK`. | Total contabilizado en la simulación. |
| `DB_BeltSpeed` | REAL | `0.10` si `DO_ConveyorRun` vale 1; en otro caso `0`. | m/s mostrado; valor fijo didáctico, no medido. |
| `DB_PieceX` | REAL | Si la pieza es visible: limitar `(piece.x + 3) × 800 / 7.15` a 0…800; si no, 0. | mm mostrados; conversión de coordenada gráfica no calibrada. |
| `DB_PusherPos` | REAL | Limitar `abs(arm.z) / 1.48 × 200` a 0…200. | mm mostrados; escala normalizada, no carrera física calibrada. |
| `DB_StageElapsed` | TIME | 0 sin fase activa; durante una fase, `elapsed × 1000`. | Watch presenta ms; reloj del navegador, no tiempo de PLC medido. |

Conservar nombres, tipos y unidades visibles existentes. Antes de mapear a TIA, decidir resolución, rangos, precisión, escalado, retención y tratamiento de desbordamiento; en particular, no interpretar `DB_PieceX` ni `DB_PusherPos` como cotas reales.

## 5. Arquitectura propuesta de Cognex y datos externos

La siguiente separación es una arquitectura didáctica futura, no una conexión existente:

| Datos | Propietario | Función | Estado |
| --- | --- | --- | --- |
| Job/receta y parámetros de inspección | Cámara | Configuración de visión del dispositivo. | Modelo, contenido y gestión de versiones pendientes. |
| DB de intercambio PLC-cámara | PLC | Trigger, identificación de pieza, estados, resultado, diagnóstico y confirmación según protocolo. | Estructura y transporte pendientes. |
| Registro electrónico externo | Gateway/servicio de datos | Trazabilidad de pieza, resultado y eventos aceptados. | Tecnología, contrato, red, retención y responsable pendientes. |
| Presentación al operador | HMI | Estado, resultado, alarmas y acciones autorizadas. | Solo panel HTML simulado; plataforma y usuarios pendientes. |

Flujo objetivo a definir: el PLC solicita captura de la pieza detenida; la cámara procesa y publica estado/resultado; el PLC acepta una respuesta válida una sola vez y la asocia al índice o identificador de pieza; el gateway registra el resultado confirmado y la HMI presenta el estado. No elegir todavía nombres de campos, protocolo, DB Cognex o tecnología de base de datos.

No asumir conexión SQL directa del PLC. `DO_VisionTrigger`, `VisionReady`, `InspectionDone`, `InspectionValid` y `VisionOK` del prototipo son señales lógicas simplificadas; `Busy`, `ACK`, errores, número de pieza y datos de trazabilidad aún no existen en el HTML. El contrato y la recuperación ante pérdida de comunicación se cerrarán al seleccionar equipo y desarrollar el documento 06.

## 6. Conteo didáctico de E/S y BOM

Conteo confirmado del registro del HTML: **7 DI y 4 DO**. Las señales de cámara y Safety descritas arriba son lógicas, no bornes confirmados.

Como ejercicio de reserva, si se pide mantener al menos 20 % de los canales instalados libres, el tamaño mínimo teórico sería `ceil(7 / 0.8) = 9 DI` y `ceil(4 / 0.8) = 5 DO`. Redondear al tamaño real de los módulos y volver a contar señales adicionales de cámara, drive, mantenimiento y expansión. El 20 % es un criterio del ejercicio, no una norma ni un requisito del caso.

| Partida | Qué determina la selección | Estado del caso |
| --- | --- | --- |
| CPU PLC y versión TIA | Ciclo, memoria, comunicaciones, diagnóstico, ciclo de vida y estándares de planta. | S7-1200 solo candidato didáctico del esquema; modelo y versión sin seleccionar. |
| E/S estándar | 7 DI, 4 DO base, nivel eléctrico, tipo de salida, aislamiento y reserva. | Conteo lógico confirmado; módulos, direcciones y reserva final pendientes. |
| E/S/CPU Safety | Resultados de evaluación de riesgos y requisitos de Safety. | Sin dimensionar; no inferir desde `SafetyReady`. |
| Fuente y armario | Tensiones de planta, corrientes de carga, ambiente, IP, temperatura y disipación. | 24 VDC es supuesto didáctico; red y cargas no calculadas. |
| Motor, cinta y drive | Carga, velocidad, ciclo, frenado, régimen y estrategia de mando. | Sin dispositivo físico ni placa de cargas. |
| Cilindros, válvulas y sensores | Fuerza, carrera, ciclo, presión, caudal, puertos y confirmación requerida. | Geometría de pantalla solamente; el mando de retorno del expulsor sigue abierto. |
| Cámara, lente e iluminación | Defectos, piezas límite, campo de visión, exposición, interfaz y soporte. | Cognex es candidata de marca; no hay modelo, job ni conexión. |
| HMI y red | Pantallas, roles, idiomas, alarmas, mantenimiento, protocolos y ciberseguridad. | HMI web simulada; equipo y red industriales pendientes. |
| Gateway y base de datos | Propietario, contrato, identificador de pieza, retención, disponibilidad y red IT/OT. | Bloque conceptual; no hay servicio conectado. |

Esta tabla es una BOM de trabajo, no una lista de compra. No se asigna SKU sin datos del producto, proceso, instalación y requisitos de planta.

## 7. Ejemplo didáctico de direccionamiento

Las direcciones siguientes solo muestran notación Siemens y **no están asignadas al proyecto**. Las direcciones reales proceden de la configuración de dispositivo de TIA después de elegir CPU, módulos y topología; se deben comprobar rangos, solapamientos y reservas.

| Tag | Ejemplo no vinculante | Función |
| --- | --- | --- |
| `DI_MagazinePart` | `%I0.0` | Entrada discreta de disponibilidad en cargador. |
| `DI_InspectionPresent` | `%I0.1` | Entrada discreta de presencia en visión. |
| `DI_RejectPosition` | `%I0.2` | Entrada discreta de posición de clasificación. |
| `DI_PusherRetracted` | `%I0.3` | Confirmación retraído. |
| `DI_PusherExtended` | `%I0.4` | Confirmación extendido. |
| `DI_ExitA` | `%I0.5` | Confirmación de salida A. |
| `DI_ExitB` | `%I0.6` | Confirmación de salida B. |
| `DO_ConveyorRun` | `%Q0.0` | Petición a interfaz del drive. |
| `DO_FeederValve` | `%Q0.1` | Interfaz de válvula del alimentador. |
| `DO_PusherValve` | `%Q0.2` | Interfaz aún por definir para el expulsor. |
| `DO_VisionTrigger` | `%Q0.3` | Trigger discreto solo si se selecciona esa interfaz. |

El ejemplo no determina asignación, módulo, tensión, corriente ni función de seguridad. No mapear `SafetyReady` a una salida estándar ni usarla para representar un circuito Safety.

## 8. Datos requeridos antes de seleccionar modelos

1. Congelar pieza, material, masa, variación y criterios de aceptación de visión.
2. Confirmar ritmo, ciclo, tareas de operación, reposición, rechazo y mantenimiento.
3. Obtener tensión/fases de planta, corrientes disponibles, ambiente, IP, temperatura y longitudes de cable.
4. Cerrar la evaluación de riesgos y los requisitos de Safety antes de seleccionar controladores o E/S Safety.
5. Resolver sentidos de avance/retorno del expulsor y el interfaz del drive.
6. Elegir interfaz Cognex y definir propietario de job, handshake, resultado, diagnóstico y asociación a pieza.
7. Definir red IT/OT, gateway, esquema de datos, retención y disponibilidad de la base externa.
8. Seleccionar CPU y módulos; luego emitir lista de canales/direcciones TIA y BOM controlada.

## 9. Revisión y siguiente puerta

**Artefacto de esta etapa:** inventario de 7 DI, 4 DO, 5 estados lógicos, 9 valores numéricos del Watch y BOM de selección con pendientes identificados.
**Cotejo ejecutado:** lectura del `registry`, `processRegistry`, `refreshIO()` y `processValues()` del HTML; conteo de tags y fórmulas comparados con este documento. No se ejecutó PLC, TIA Portal, cámara, gateway ni base de datos.
**Pendiente de D2R:** validar que este mapa describe correctamente el caso didáctico.
**Siguiente documento:** 04 · Safety Engineering, antes de cerrar cualquier hardware o dirección Safety.
