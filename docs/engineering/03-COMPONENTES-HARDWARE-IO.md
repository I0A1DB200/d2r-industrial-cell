# 03 · Componentes, hardware y mapa de E/S

**Estado:** borrador didáctico v0.1 · selección pendiente  
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
