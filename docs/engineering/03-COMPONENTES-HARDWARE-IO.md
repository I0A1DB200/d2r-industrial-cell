# 03 · Componentes, hardware y mapa de E/S

**Estado:** borrador didáctico v0.2 · selección pendiente
**Objetivo:** convertir las interfaces funcionales en una lista trazable de equipos y señales antes de asignar modelos o direcciones.

## Criterios para seleccionar hardware

| Elemento | Datos necesarios antes de elegir | Estado actual |
| --- | --- | --- |
| PLC y E/S | Cantidad/tipo de puntos, reserva, ciclo, red, diagnósticos y requisitos de Safety. | CPU, módulos y direcciones no seleccionados. |
| HMI | Roles, pantallas, idiomas, recetas, alarmas, acceso y conexión. | Solo existe un panel simulado. |
| Accionamiento de cinta | Velocidad, carga, ciclo, frenado, alimentación y diagnóstico. | No se modela un motor o variador real. |
| Válvulas y sensores | Presión, cargas, carreras, entorno, cableado y detección requerida. | Señales conceptuales; modelos no elegidos. |
| Visión Cognex | Pieza, defectos, campo de visión, óptica, luz, tiempo de exposición, red y formato de resultado. | Marca mencionada como posibilidad; no hay modelo ni conexión. |

La selección debe considerar compatibilidad eléctrica y de red, disponibilidad, repuestos, normas de planta, soporte y coste total. No se asignan números de parte sin datos de producto y entorno.

## Tags que existen en el prototipo

Estos nombres pertenecen al Watch del HTML. Son etiquetas conceptuales sin direcciones físicas.

| Grupo | Tags actuales |
| --- | --- |
| DI | `DI_MagazinePart`, `DI_InspectionPresent`, `DI_RejectPosition`, `DI_PusherRetracted`, `DI_PusherExtended`, `DI_ExitA`, `DI_ExitB` |
| DO | `DO_ConveyorRun`, `DO_FeederValve`, `DO_PusherValve`, `DO_VisionTrigger` |
| Lógicos de inspección / permiso | `VisionReady`, `InspectionDone`, `InspectionValid`, `VisionOK`, `SafetyReady` |
| INT | `DB_SequenceStep`, `DB_PieceIndex` |
| DINT | `DB_CountOK`, `DB_CountNOK`, `DB_CountTotal` |
| REAL | `DB_BeltSpeed` (m/s), `DB_PieceX` (mm), `DB_PusherPos` (mm) |
| TIME | `DB_StageElapsed` (ms en la presentación del Watch) |

No cambiar nombres, tipos o unidades del Watch normal al llevar esta interfaz a un PLC. Confirmar el significado y escala de cada variable antes de mapearla; `DB_PieceX` y `DB_PusherPos` son valores derivados de la visualización, no mediciones físicas calibradas.

## Mapa futuro y equipo externo

Preparar una tabla de asignación con: tag, descripción, tipo eléctrico, dirección PLC, equipo/borne, estado seguro, filtro/diagnóstico y caso de prueba. Mantener la dirección en `TBD` hasta elegir CPU y módulos.

Para la cámara, acordar propietario y ciclo de datos antes de crear el DB: `DO_VisionTrigger` podría activar la entrada física de trigger de la cámara o ser un comando de red, según la interfaz seleccionada. La Cognex devuelve `Ready`, `Busy/Done`, `Valid`, resultado y diagnóstico; el PLC mapea los datos aceptados en su DB de intercambio y los asocia a la pieza correcta. Distinguir el job/almacenamiento propio de la Cognex del DB de intercambio en el PLC; su contenido y protocolo dependen del modelo. El simulador solo expone señales lógicas básicas; no tiene handshake externo ni base de datos electrónica activa.

**Artefacto de salida:** lista de equipos aprobada, cálculo de E/S con reserva y tabla de direcciones.  
**Pendiente:** URS, layout, evaluación de Safety, red de planta, modelos seleccionados y asignación de direcciones.

## Dimensionamiento didáctico de E/S y BOM

Conteo base del modelo: 7 entradas discretas y 4 salidas discretas. `VisionReady`, `InspectionDone`, `InspectionValid` y `VisionOK` son estados lógicos simulados, no bornes adicionales confirmados. Si la cámara intercambia datos por Ethernet, sus campos no consumen un canal DI/DO, aunque sí exigen interfaz, memoria, actualización y diagnóstico. Si el protocolo final usa handshake discreto, volver a sumar esos canales.

Ejemplo aritmético para aprender reserva: suponiendo como **criterio de ejercicio**, no requisito universal, un 20 % de canales libres, 7 DI requieren `ceil(7 × 1,2)=9` y 4 DO requieren `ceil(4 × 1,2)=5`. Redondear al tamaño de módulo disponible y recontar canales de cámara, accionamiento, mantenimiento y expansión antes de seleccionar la estación.

| Partida de BOM | Especificación que debe cerrarse | Método de selección | Estado del caso |
| --- | --- | --- | --- |
| CPU PLC | ciclo, memoria, comunicaciones, diagnóstico, ciclo de vida, F-Safety si el análisis lo exige. | Comparar requisitos con CPU candidata y soporte de planta; validar versión TIA. | Familia/modelo pendiente. |
| E/S estándar | cantidad, 24 VDC u otro nivel, tipo de salida, aislamiento y diagnóstico. | Conteo tag a tag + reserva documentada. | Ejemplo base 7 DI/4 DO; topología pendiente. |
| E/S Safety | cantidad y tipo de dispositivos/canales resultantes del análisis. | Derivar desde especificación Safety y calcular/validar arquitectura. | No dimensionado. |
| Fuente 24 VDC | demanda simultánea de sensores, válvulas, PLC/HMI y margen térmico. | Sumar corrientes de placa, condiciones de arranque y margen del proyecto. | Corrientes no disponibles. |
| Motor/drive cinta | carga, velocidad, ciclo, par de arranque, frenado y red. | Cálculo mecánico + régimen y estrategia de control. | No se modela equipo real. |
| Válvulas/cilindros | fuerza, carrera, velocidad, ciclo, presión y sensores. | Dimensionar actuador y válvula; revisar consumo, mantenimiento y riesgo. | Geometría solo visual. |
| Cámara Cognex | defectos, visión, lente, luz, tiempo, interfaz, soporte y servicio. | Prueba con piezas etiquetadas y evaluación de resultados con Calidad. | Modelo/óptica/job pendientes. |
| HMI y armario | tamaño, legibilidad, usuarios, ambiente, ubicación y acceso. | Revisar pantallas/roles y restricciones de planta. | Panel/cabina solo representados en HTML. |

La tabla es una BOM de trabajo, no una recomendación de compra. No se da un SKU porque faltan variables que cambian directamente la selección.

## Inventario detallado de tags del simulador

El nombre y el comportamiento descrito en la última columna corresponden al HTML. `DI` y `DO` nombran familias conceptuales; no hay tabla de direcciones TIA ni hardware conectado.

| Tag | Tipo lógico | Descripción | Valor en el modelo actual |
| --- | --- | --- | --- |
| `DI_MagazinePart` | BOOL | Pieza disponible en la salida del cargador. | 1 durante `FEED`; se genera por fase, no por sensor físico. |
| `DI_InspectionPresent` | BOOL | Pieza en estación de inspección. | 1 durante `INSPECT`. |
| `DI_RejectPosition` | BOOL | Pieza en posición de clasificación. | 1 en `SORT_STOP` y durante empuje OK. |
| `DI_PusherRetracted` | BOOL | Vástago/carro en reposo retraído. | 0 mientras empuja o retorna; estado calculado desde fase. |
| `DI_PusherExtended` | BOOL | Confirmación de expulsor extendido. | 1 en el extremo de extensión OK y durante el primer tramo del retorno; calculado por fase. |
| `DI_ExitA` | BOOL | Confirmación gráfica de salida A. | 1 en la fase de finalización OK. |
| `DI_ExitB` | BOOL | Confirmación gráfica de salida B. | 1 en la fase de finalización NOK. |
| `DO_ConveyorRun` | BOOL | Orden virtual de movimiento de cinta. | 1 en transporte y avance NOK a salida B. |
| `DO_FeederValve` | BOOL | Orden virtual del actuador alimentador. | Ventana parcial de `FEED`. |
| `DO_PusherValve` | BOOL | Orden virtual de válvula del expulsor. | 1 en empuje OK y retorno OK. |
| `DO_VisionTrigger` | BOOL | Disparo lógico de la captura. | 1 durante `INSPECT`; no acciona una cámara física. |
| `VisionReady` | BOOL | Cámara disponible para inspeccionar. | Constante 1 en la simulación. |
| `InspectionDone` | BOOL | Captura lógica finalizada. | 1 desde la fase posterior a `INSPECT`. |
| `InspectionValid` | BOOL | Resultado utilizable por la secuencia. | 1 desde la fase posterior a `INSPECT`. |
| `VisionOK` | BOOL | Resultado OK de la inspección simulada. | Derivado del lote fijo después de captura. |
| `SafetyReady` | BOOL | Permiso conceptual visible en Watch. | Constante 1; no es una función Safety. |

Los estados de sensores son proxies de animación: por ejemplo, las salidas A/B se representan al final de la fase, no mediante fotocélulas físicas. Una ingeniería real debe definir posición de montaje, distancia de detección, tipo de sensor, temporización, cable y diagnóstico.

## Variables numéricas visibles en Watch

| Tag | Tipo | Unidad de pantalla | Regla usada por el modelo | Uso didáctico / limitación |
| --- | --- | --- | --- | --- |
| `DB_SequenceStep` | INT | número de etapa | 0 detenido; en marcha, índice de fase × 10 + 10. | Código de etapa simulado; no enumera estados TIA reales. |
| `DB_PieceIndex` | INT | piezas | índice de lote más 1 mientras ejecuta pieza. | Puede mostrar la pieza en curso. |
| `DB_CountOK` | DINT | piezas | contador de rutas OK completadas. | Contador del modelo. |
| `DB_CountNOK` | DINT | piezas | contador de rutas NOK completadas. | Contador del modelo. |
| `DB_CountTotal` | DINT | piezas | `DB_CountOK + DB_CountNOK`. | Total de piezas ya contadas. |
| `DB_BeltSpeed` | REAL | m/s | 0 o 0,10 según el BOOL de cinta. | Valor discreto didáctico, no velocidad medida. |
| `DB_PieceX` | REAL | mm | posición X visual escalada y limitada a 0…800. | Conversión ilustrativa desde coordenadas 3D; no calibrada. |
| `DB_PusherPos` | REAL | mm | extensión relativa × 200/1,48, limitada a 0…200. | Escala normalizada de Watch, no carrera real en mm. |
| `DB_StageElapsed` | TIME | ms | tiempo de fase × 1000. | Reloj virtual, no tiempo de PLC ni medición instrumental. |

La descripción anterior registra el Watch actual para conservar trazabilidad. No debe copiarse como especificación de hardware sin revisar resolución, precisión, overflow, retención y unidades requeridas.

## Ejemplo de asignación de direcciones (solo ejercicio)

El siguiente bloque enseña la forma de una tabla Siemens de ejemplo. **No son direcciones asignadas a este proyecto.** Se deben reemplazar tras seleccionar CPU, módulos y topología de estación; verificar solapamientos con la configuración TIA.

| Tag de ejemplo | Dirección ilustrativa | Tipo de señal a confirmar |
| --- | --- | --- |
| `DI_MagazinePart` | `%I0.0` | Entrada discreta, sensor de pieza. |
| `DI_InspectionPresent` | `%I0.1` | Entrada discreta, sensor en estación. |
| `DI_RejectPosition` | `%I0.2` | Entrada discreta, presencia en clasificación. |
| `DI_PusherRetracted` | `%I0.3` | Entrada discreta, sensor de cilindro. |
| `DI_PusherExtended` | `%I0.4` | Entrada discreta, sensor de cilindro. |
| `DI_ExitA` / `DI_ExitB` | `%I0.5` / `%I0.6` | Entradas discretas, sensores de salida a definir. |
| `DO_ConveyorRun` | `%Q0.0` | Salida a interfaz de accionamiento, no necesariamente potencia directa. |
| `DO_FeederValve` | `%Q0.1` | Salida a bobina/interfaz de válvula según selección. |
| `DO_PusherValve` | `%Q0.2` | Salida a bobina/interfaz de válvula según selección. |
| `DO_VisionTrigger` | `%Q0.3` | Salida discreta o comando de red, por decidir. |

No mapear `SafetyReady` a una salida estándar para imitar un circuito Safety. Los dispositivos y señales Safety requieren canales, evaluación y arquitectura propios.

## Ficha de selección: Cognex y datos electrónicos

Antes de seleccionar cámara, completar: pieza/variantes, defecto, tolerancia, falso rechazo/falsa aceptación permitidos, campo de visión, resolución, óptica, iluminación, tiempo disponible con cinta parada, distancia de trabajo, ambiente, montaje, job/receta, comunicación, licencia/herramientas, resultado requerido, diagnóstico, almacenamiento y soporte.

| Dato de interfaz propuesto | Dirección lógica | Tipo candidato | Propietario | Estado |
| --- | --- | --- | --- | --- |
| Trigger | PLC → cámara | BOOL discreto o comando Ethernet | PLC genera; cámara acepta | Interfaz por seleccionar |
| Job/Recipe ID | PLC → cámara | UINT/STRING según interfaz | PLC solicita; cámara valida | Pendiente |
| Ready / Busy | Cámara → PLC | BOOL | Cámara publica | Pendiente |
| Done / Valid | Cámara → PLC | BOOL | Cámara publica | Pendiente |
| Result / Score | Cámara → PLC | BOOL/ENUM/REAL según criterio | Cámara calcula; PLC valida y retiene | Criterio pendiente |
| ErrorCode / JobActive | Cámara → PLC | UINT/ENUM | Cámara publica | Modelo pendiente |
| Ack / ResetExchange | PLC ↔ cámara | BOOL o comando de protocolo | Propiedad acordada por handshake | Pendiente |

Esto es una propuesta de estructura, no un formato de Cognex concreto. Confirmar la documentación del modelo, el protocolo y el firmware; no asumir que `VisionOK` representa todos los defectos o resultados del equipo.
