# Expediente de ingeniería · D2R Inspection Cell

Este expediente convierte la célula del simulador en un caso didáctico trazable, desde el brief hasta la puesta en marcha. El punto de partida es el [prototipo actual](../../D2R-3D-001_Prototipo_Funcional_v11.html); no representa todavía un proyecto de cliente aprobado ni una instalación física.

## Ruta de documentos

| Etapa | Documento | Estado |
| --- | --- | --- |
| 00 | Brief del cliente y requisitos iniciales ([ES](00-BRIEF-CLIENTE.md) · [EN](00-BRIEF-CLIENTE.en.md)) | Base didáctica aprobada por D2R · cliente real no aplica |
| 01 | Especificación funcional y criterios de aceptación ([ES](01-ESPECIFICACION-FUNCIONAL.md) · [EN](01-FUNCTIONAL-SPECIFICATION.en.md)) | Especificación v0.3 basada en brief aprobado · revisión D2R pendiente |
| 02 | Diseño mecánico, eléctrico y neumático ([ES](02-DISENO-MECANICO-ELECTRICO-NEUMATICO.md) · [EN](02-MECHANICAL-ELECTRICAL-PNEUMATIC-DESIGN.en.md)) | Referencias del simulador y paquete de diseño; ingeniería física pendiente |
| 03 | Componentes, hardware y mapa de E/S ([ES](03-COMPONENTES-HARDWARE-IO.md) · [EN](03-COMPONENTS-HARDWARE-IO.en.md)) | Tags y ejemplo de asignación; hardware/direcciones reales pendientes |
| 04 | Safety Engineering ([ES](04-SAFETY-ENGINEERING.md) · [EN](04-SAFETY-ENGINEERING.en.md)) | Registro inicial y plantilla; evaluación aprobada pendiente |
| 05 | Arquitectura PLC: OB, FC, FB, DB, UDT y tags ([ES](05-ARQUITECTURA-PLC.md) · [EN](05-PLC-ARCHITECTURE.en.md)) | Árbol y estructuras propuestas; PLC no implementado |
| 06 | Programación LAD/KOP y SCL, HMI y visión ([ES](06-PROGRAMACION-HMI-VISION.md) · [EN](06-PROGRAMMING-HMI-VISION.en.md)) | Ejemplos didácticos no compilados; proyecto ejecutable pendiente |
| 07 | Gestión del proyecto, commissioning, FAT y SAT ([ES](07-PROYECTO-COMMISSIONING-FAT-SAT.md) · [EN](07-PROJECT-MANAGEMENT-COMMISSIONING-FAT-SAT.en.md)) | Roles, puertas y protocolos; pruebas físicas pendientes |

Safety se identifica desde el brief y se desarrolla antes de cerrar el diseño detallado y las pruebas de puesta en marcha. El orden del índice organiza el aprendizaje; no sustituye el orden profesional de evaluación de riesgos.

## Estado real del caso

- **Confirmado en el simulador:** secuencia didáctica, fases/tiempos del HTML, lote virtual 4 OK/3 NOK, rutas OK → A y NOK → B, nombres/tipos del Watch y mandos disponibles.
- **Desarrollado como propuesta educativa:** requisitos funcionales, desglose del conjunto, mapa lógico de E/S, ejemplos ilustrativos de direcciones, estructuras Cognex/PLC, árbol de bloques, flujo HMI y plan de aceptación.
- **Todavía no definido por un cliente ni implementado:** dimensiones y masa de pieza, tolerancias de inspección, producción objetivo, marcas/modelos de hardware, protocolo Cognex, asignación TIA real, evaluación/diseño Safety, planos liberados y criterios físicos FAT/SAT.

Por ello, el expediente ya sirve como guía de aprendizaje y revisión, pero todavía no es un paquete de fabricación, un proyecto TIA cargable ni una especificación contractual cerrada.

## Convenciones

- **Confirmado en el simulador:** comportamiento o dato comprobable en el HTML y las pruebas actuales.
- **Propuesta didáctica:** requisito reconstruido para enseñar el diseño; no equivale a una petición real firmada.
- **Pendiente de definición:** dato que requiere una decisión del cliente o una ingeniería posterior.
- **Fuera de alcance actual:** hardware, software o validación física que aún no existe.

Cada documento registrará su objetivo, entradas, decisiones, artefactos, verificación, estado y trazabilidad. La documentación tendrá lectura en español e inglés con selector dentro del lector; el Markdown español será el texto de trabajo y su traducción inglesa se mantendrá en paralelo. Usaremos identificadores `REQ-###` para requisitos, `TAG-###` para señales, `PLC-###` para bloques y `TC-###` para casos de prueba. Un requisito debe poder seguirse desde su origen hasta su prueba, sin duplicar nombres de señales entre documentos.

Los documentos 01–07 son borradores de ingeniería didácticos: no hay hardware seleccionado, DB/PLC reales, cámara Cognex conectada, evaluación de riesgos aprobada ni FAT/SAT ejecutados. `reader.html` representa los Markdown dentro del lector del simulador; sus fuentes ES/EN se mantienen en este directorio.

## Principios de trabajo

1. Empezar por lo que el simulador confirma y marcar las reconstrucciones como borrador.
2. No seleccionar una CPU, módulos, cámara Cognex, protocolo ni direcciones hasta tener requisitos suficientes.
3. Mantener la lógica, fases, temporizaciones, clasificación y modelo de Safety del simulador fuera de los cambios documentales.
4. Distinguir una simulación visual de una prueba con equipo real.
5. Revisar cada paquete antes de avanzar al siguiente.

El estado del simulador y sus comprobaciones actuales se resumen en el [informe ENGINE-001](../D2R-ENGINE-001-REPORT.md). Ese informe de QA no sustituye a los documentos de ingeniería de este expediente.
