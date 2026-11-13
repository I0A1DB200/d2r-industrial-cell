# Registro de láminas conceptuales · Concept sheet register

Este paquete convierte el concepto del documento 02 en tres diagramas vectoriales legibles desde el lector del simulador o en un navegador. Las láminas son bilingües (ES/EN), esquemáticas y no están dibujadas a escala.

> **ESTADO: CONCEPTUAL · NO APTO PARA FABRICACIÓN / CONCEPTUAL · NOT FOR CONSTRUCTION.** No utilizar para comprar, fabricar, cablear, instalar, dimensionar o validar una máquina. No representan equipo físico conectado ni certificación.

| Nº de plano | Título | Qué enseña | Limitación principal |
| --- | --- | --- | --- |
| [M-02-001](M-02-001-layout-conceptual.svg) | Layout funcional / Functional layout | Alimentador, cinta, cámara, transferencia OK→A, ruta NOK→B y armario de referencia. | Croquis funcional sin escala, envolventes, cotas de montaje ni revisión de accesos. |
| [E-02-001](E-02-001-arquitectura-electrica-conceptual.svg) | Arquitectura eléctrica / Electrical architecture | Fronteras entre alimentación, control estándar, campo, visión, gateway y disciplina Safety. | No es esquema de potencia/control; no hay referencias de equipos, direcciones, bornes ni protecciones. |
| [P-02-001](P-02-001-circuito-neumatico-conceptual.svg) | Concepto neumático / Pneumatic concept | Suministro supuesto, preparación/islamiento por definir y dos funciones actuadas. | No es un esquema ISO 1219 liberado; circuito, válvulas, actuadores, caudales y estado por pérdida de energía pendientes. |

## Base usada

- Brief didáctico 00 y especificación funcional 01; diseño conceptual 02; inventario de tags en 03; límites de Safety en 04.
- Posiciones gráficas del HTML para identificar zonas. Las coordenadas y dimensiones visuales no se tratan como cotas CAD ni se convierten en tolerancias.
- Señales del Watch documentadas en 03: siete DI y cuatro DO como inventario del prototipo; son tags lógicos sin asignación eléctrica ni dirección TIA.
- S7-1200, Cognex, control 24 VDC y aire nominal 6 bar son hipótesis del ejercicio con selección/verificación pendiente. 6 bar no está medido.

## Pendientes antes de planos de ingeniería

1. Confirmar requisitos, producto real, tolerancias, masa, rendimiento, layout, tareas de mantenimiento y entorno.
2. Elegir motor/drive, sensores, actuadores, válvulas, CPU/módulos, cámara/óptica/luz, gateway y equipos de operador; obtener sus hojas de datos.
3. Cerrar el inventario y la asignación real de E/S, protocolo de cámara, red/DB, cargas, alimentación AC, protecciones, cableado y bornes.
4. Medir y calcular fuerzas, carreras físicas, ciclo/caudal de aire, estabilidad, rigidez, accesos y transferencias.
5. Realizar evaluación de riesgos competente y definir/validar Safety antes de decidir aislamiento, descargas o estados de actuadores.
6. Emitir planos de fabricación, potencia, control, red, bornes/cables y neumática con revisión formal, criterios aplicables y responsables.

## Evidencia y revisión

Los SVG se inspeccionaron por lectura de etiquetas y coherencia con documentos 02–04. No se ejecutó CAD, análisis dimensional, cálculo eléctrico/neumático, revisión normativa, prueba física ni validación Safety. La revisión D2R de las láminas está pendiente.

## English summary

This first package contains three bilingual, schematic, not-to-scale vector sheets. M-02-001 shows the functional cell layout; E-02-001 separates conceptual power, standard PLC control, field devices, vision, external data and the unresolved Safety boundary; P-02-001 shows the assumed air supply and two actuator functions without selecting valve states or actuator circuits.

All sheets are **CONCEPTUAL · NOT FOR CONSTRUCTION**. No physical equipment is confirmed or connected. S7-1200, Cognex, 24 VDC and nominal 6 bar are educational assumptions pending confirmation; the pressure has not been measured. The Watch tags have no physical addresses. Before detailed engineering, confirm the product, layout, loads, selected equipment, wiring/network interfaces, pneumatic demand, maintenance tasks and risk assessment. Then issue reviewed mechanical, power/control, network, terminal/cable and pneumatic drawings.

The SVG labels and this register were checked against documents 02–04. No CAD, dimensional or sizing calculation, standards review, physical test or Safety validation was performed. D2R review is pending.
