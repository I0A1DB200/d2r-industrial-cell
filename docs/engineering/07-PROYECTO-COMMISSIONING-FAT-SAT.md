# 07 · Gestión del proyecto y commissioning

**Estado:** plan de trabajo didáctico v0.1 · sin pruebas físicas ejecutadas  
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
