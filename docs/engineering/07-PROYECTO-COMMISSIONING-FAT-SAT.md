# 07 · Gestión del proyecto y commissioning

**Estado:** plan de trabajo didáctico v0.2 · sin pruebas físicas ejecutadas
**Objetivo:** ordenar entregables, revisiones y pruebas desde el brief hasta la aceptación de una instalación real.

## Hitos y puertas de revisión

| Hito | Paquete de salida | Criterio para avanzar |
| --- | --- | --- |
| G0 · Inicio | Alcance, responsables, riesgos y preguntas de cliente. | Propietario de cada decisión identificado. |
| G1 · Requisitos | URS/brief y especificación funcional trazada. | Requisitos verificables y excepciones acordadas. |
| G2 · Diseño | Layout, mecánica, esquemas eléctricos/neumáticos e interfaces. | Revisiones interdisciplinarias cerradas. |
| G3 · Hardware y Safety | Lista de materiales, direcciones, evaluación de riesgos y diseño Safety. | Selección y validación planificadas por responsables competentes. |
| G4 · Software | PLC, HMI, cámara, alarmas y documentación de versiones. | Compilación, simulación y pruebas de integración registradas. |
| G5 · FAT | Protocolo y resultados de aceptación en fábrica. | Desviaciones resueltas o aceptadas formalmente. |
| G6 · SAT | Instalación, interfaces de planta, pruebas de seguridad y proceso. | Pruebas en emplazamiento aprobadas por cliente/equipo. |
| G7 · Entrega | As-built, copias de seguridad, manuales, formación y repuestos. | Paquete final y responsables de operación aceptados. |

El orden real puede variar por contrato y análisis de riesgos. Ninguna captura del simulador sustituye FAT, SAT ni validación de Safety.

## Preparación de commissioning

Antes de energizar, revisar liberación mecánica, planos, conexiones, identificación de cables, tierra, aire, red, versiones de software, copias de seguridad y permisos de trabajo. Después comprobar E/S con el equipo aislado y según procedimiento autorizado; probar actuadores por separado; verificar cámara y receta; integrar la secuencia; y medir los criterios de aceptación con instrumentos adecuados.

Definir de antemano criterios para: alimentación de una pieza, detención en inspección, asociación de resultado a pieza, ruta A/B, conteo, FIN DE PIEZA, RESET, recuperación de comunicación, alarmas, cambios de receta y comportamiento seguro. Para cada prueba, indicar condición inicial, pasos, esperado, medido, responsable y evidencia.

## Matriz inicial de FAT/SAT propuesta

| Caso | Prueba | Tipo de evidencia |
| --- | --- | --- |
| `TC-101` | AUTO completo y conciliación de piezas/contadores. | Registro PLC/HMI y observación del producto. |
| `TC-102` | PIEZA, FIN DE PIEZA, RESET y recuperación tras parada operacional. | Protocolo aprobado y registro de estados. |
| `TC-103` | Pérdida y recuperación de comunicación con cámara. | Logs, diagnóstico y asociación de pieza. |
| `TC-104` | Resultado OK/NOK y comprobación física de A/B. | Muestras de desafío y firma de aceptación. |
| `TC-105` | Validación de cada función Safety. | Protocolo Safety, medidas e informe competente. |

Estos casos son una plantilla. Los valores límite, muestras de visión, procedimientos seguros y resultados deben definirse para el equipo real; aún no se han ejecutado.

## Registro de incidencias y cierre

Registrar cada desviación con ID, versión, síntoma, condición de reproducción, impacto, responsable, corrección, repetición de prueba y estado. Mantener configuración aprobada y copias de seguridad identificables. La entrega incluye planos as-built, lista de software/hardware, manual, formación, repuestos y registro de cambios.

**Trazabilidad:** matriz `REQ` → `TC` → evidencia → desviación/cierre.  
**Pendiente:** cronograma, responsables, criterios contractuales, versiones, muestras, instrumentos y formato de aceptación.

## Responsabilidades del equipo

| Rol | Responsable de | Evidencia de entrega |
| --- | --- | --- |
| Cliente / dueño de proceso | URS, producto, cadencia, criterios OK/NOK, interfaces y aceptación. | Requisitos aprobados y actas de revisión. |
| Project Manager | Alcance, hitos, riesgos, cambios, coste, dependencias y decisiones abiertas. | Plan, RAID log, registro de decisiones y minutas. |
| Ingeniería mecánica | Layout, CAD, cargas, accesos, fabricación y documentación as-built. | Planos liberados, BOM mecánico y revisiones. |
| Ingeniería eléctrica | Armario, alimentación, esquemas, protección, cableado y red. | Esquemas aprobados, lista de cables y registros de inspección. |
| PLC/HMI | Arquitectura, tags, programa, alarmas, versiones y pruebas. | Backup/proyecto versionado, lista de tags y protocolo FAT. |
| Integración de visión | Óptica/luz, job, muestras, interfaz, límites y trazas de resultados. | Informe de capacidad acordado, job respaldado y mapa de datos. |
| Responsable Safety | Evaluación, especificación, arquitectura, cálculo y validación. | Expediente de Safety firmado por responsable competente. |
| Calidad / puesta en marcha | Muestras, inspección, trazabilidad, desviaciones y aceptación. | Protocolos firmados y registro de no conformidades. |

Una misma persona puede asumir roles en un proyecto pequeño; las aprobaciones de Safety y cliente siguen requiriendo la competencia y autoridad correspondientes.

## Actividades por fase de commissioning

### 1. Revisión documental y precomisionado

- Confirmar número de serie, versión de software/firmware, planos y configuración “as designed”.
- Revisar montaje, fijaciones, guardas, etiquetado, tierra, continuidad, protecciones, presión y calidad de aire.
- Comprobar que las pruebas pendientes, permisos, calibraciones y equipos de medida están identificados.
- Preparar respaldo inicial de PLC, HMI, cámara y variador antes de cambiar parámetros.

### 2. Prueba eléctrica de E/S

Con el área controlada y siguiendo procedimientos aprobados, comprobar tag ↔ borne ↔ dispositivo, tensión/polaridad, estado normal, transición, diagnóstico de pérdida de canal y reacción de programa. Ejecutar salidas solo cuando la zona esté preparada y el movimiento esté autorizado. Registrar cada canal, no inferir un estado a partir del LED del HMI solamente.

### 3. Movimiento individual e integración

Probar drive, alimentador y expulsor por separado con límites de riesgo acordados; verificar sentido, velocidad, carrera, presión, amortiguación y feedback. Luego integrar alimentación → visión → clasificación; probar pieza real, variación de pieza y contenedor; confirmar que una respuesta de cámara pertenece al ID de pieza correcto.

### 4. FAT

1. Acordar build, backups, muestra, instrumentos, protocolo y responsables.
2. Ejecutar pruebas nominales y límite contra cada requisito trazado.
3. Verificar alarmas, pérdida de comunicación, recuperación, reset, modo pieza y parada operacional.
4. Repetir fallos corregidos y adjuntar evidencia identificada por versión.
5. Registrar desviaciones; aceptar, rechazar o aplazar cada una con responsable y fecha.

### 5. SAT y entrega

Verificar servicios y conexiones del emplazamiento; repetir pruebas relevantes después del transporte/instalación; validar interfaces de planta, formatos de producto, condiciones ambientales y funciones Safety en el emplazamiento. Cerrar punch-list antes de firmar aceptación. Entregar documentación as-built, backups probados, listas de repuestos, formación y contactos de soporte.

## Registro de prueba trazable

| Campo | Ejemplo de qué documentar |
| --- | --- |
| ID / requisito | `TC-104` / `REQ-003`; versión de documento. |
| Equipo / configuración | Número de serie, CPU/firmware, programa, receta/job Cognex. |
| Precondiciones | Pieza/revisión, modo, velocidad, presión, contenedor y estado inicial. |
| Pasos | Orden exacto, entradas provocadas y condiciones ambientales relevantes. |
| Esperado | Criterio con unidad y tolerancia aprobado antes de la prueba. |
| Observado | Valor medido, instrumento/calibración, tag/log y comportamiento. |
| Resultado | PASS/FAIL/BLOCKED; desviación y evaluación de impacto. |
| Aprobaciones | Ejecutor, testigo, cliente y fecha. |

No sustituir “4 OK / 3 NOK” del lote virtual por criterio de calidad de producción. Para validar visión se necesitan muestras representativas etiquetadas, verdad de referencia y acuerdo de falsos aceptados/rechazados.
