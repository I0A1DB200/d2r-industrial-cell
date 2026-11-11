# 00 · Brief del cliente y requisitos iniciales

**Estado:** borrador didáctico · pendiente de revisión  
**Fecha:** 2026-11-11  
**Caso base:** D2R Inspection Cell  
**Fuente del comportamiento actual:** [prototipo funcional](../../D2R-3D-001_Prototipo_Funcional_v11.html)

> No se ha proporcionado un brief firmado por un cliente real. Este documento reconstruye un escenario de aprendizaje a partir del simulador y separa los hechos observables de las decisiones que aún deben tomarse.

## 1. Escenario propuesto

Una célula de inspección debe presentar piezas individuales en una cinta, realizar una inspección visual y dirigir cada pieza a una salida según el resultado. El operador debe poder iniciar un lote automático o pedir el procesamiento de una pieza, observar el estado de la máquina y consultar señales y contadores.

Este texto es una **propuesta didáctica**, no una necesidad atribuida a una empresa identificada. El producto real, las tolerancias de inspección, el ritmo de producción y las interfaces con la línea deben definirse antes de seleccionar hardware.

## 2. Objetivo del caso didáctico

Enseñar a desarrollar, por etapas, el proyecto de una célula de inspección: convertir requisitos en diseño funcional, mecánico y eléctrico; seleccionar hardware; estructurar y programar el PLC; definir Safety Engineering; y preparar la puesta en marcha y aceptación.

El simulador sirve como objeto de estudio y demostración. No es un PLC ejecutando el programa de una máquina real ni una validación de diseño industrial.

## 3. Funcionamiento representado actualmente

Estos puntos describen el prototipo; no son todavía requisitos aprobados por un cliente:

- Un cargador muestra una pila de piezas y anima la extracción de la pieza inferior hacia la cinta.
- La cinta transporta la pieza a una estación de inspección visual simulada y se detiene durante la captura lógica.
- El resultado de inspección lo determina el lote didáctico, no un algoritmo que analice la geometría de la pieza.
- El lote de demostración contiene siete resultados: `OK, NOK, OK, NOK, OK, OK, NOK`.
- La ruta de clasificación es `OK → A` mediante expulsión lateral y `NOK → B` al final de la cinta.
- `AUTO` ejecuta el lote de forma continua; `PIEZA` procesa una pieza por orden de START.
- STOP solicita terminar la pieza actual antes de detener el ciclo.
- El HMI presenta estado, modo y contadores; PLC Watch muestra señales simuladas y valores conceptuales.
- RESET HMI está restringido a máquina detenida. RESET SIM y la pausa controlan el entorno de simulación y no deben describirse como mandos PLC equivalentes.

La secuencia contiene fases y duraciones definidas en el HTML. Son tiempos del modelo simulado; no constituyen takt time, capacidad de producción ni tiempos de respuesta de equipos reales.

## 4. Requisitos preliminares para el ejercicio

Todos los requisitos de esta tabla son **propuestas derivadas del prototipo** y necesitan validación antes de considerarse requisitos de cliente.

| ID | Requisito propuesto | Criterio observable en el simulador | Estado |
| --- | --- | --- | --- |
| REQ-001 | La célula debe presentar una pieza por ciclo en la cinta. | Se observa una pieza activa alimentada desde la pila, sin duplicarla en el ciclo. | Propuesta didáctica |
| REQ-002 | Cada pieza debe pasar por una estación de inspección visual. | Se observa la fase INSPECT y sus señales simuladas. | Propuesta didáctica; inspección real pendiente |
| REQ-003 | El resultado OK debe ir a A y el resultado NOK a B. | En el lote de ejemplo: cuatro salidas A y tres salidas B. | Ruta confirmada en el simulador; criterio de inspección pendiente |
| REQ-004 | Se deben ofrecer AUTO y PIEZA. | AUTO recorre el lote; PIEZA avanza una pieza por orden START. | Comportamiento presente; aprobación de operador pendiente |
| REQ-005 | STOP debe finalizar la pieza actual y luego detener la secuencia. | El ciclo no se detiene inmediatamente al solicitar FIN DE PIEZA. | Comportamiento presente; aprobación de cliente pendiente |
| REQ-006 | El operador debe conocer modo, estado y producción acumulada. | HMI muestra READY/RUN, modo, OK, NOK y total. | Comportamiento presente; contenido final de HMI pendiente |
| REQ-007 | Debe existir diagnóstico de señales durante ingeniería y puesta en marcha. | PLC Watch permite observar E/S y valores simulados. | Herramienta didáctica presente; no define una Watch Table de PLC real |
| REQ-008 | La cámara debe intercambiar disparo, disponibilidad, resultado y confirmación. | Solo existe un intercambio lógico simulado en el prototipo. | Propuesta; fabricante, modelo, protocolo y mapa de datos pendientes |
| REQ-009 | La máquina debe tener un concepto de seguridad documentado y validable. | El simulador muestra un permiso lógico conceptual. | Pendiente de evaluación; no es función Safety ni evidencia de certificación |

## 5. Datos de demostración y límites

El lote 4 OK/3 NOK es fijo para comprobar las rutas y los contadores. **No significa** que el proceso real deba producir esa proporción. La pieza 3D y sus detalles visibles son elementos gráficos; no fijan dimensiones, material, tolerancias o defectos aceptables de un producto real.

Las señales con nombres `DI`, `DQ`, `DB` y tipos BOOL, INT, DINT, REAL o TIME son una representación conceptual del Watch. No hay direcciones físicas asignadas, CPU seleccionada, proyecto TIA, cámara conectada ni intercambio electrónico externo activo.

La cámara Cognex citada como posible componente es una intención para estudiar. En este punto no se ha seleccionado modelo, lente, iluminación, interfaz Ethernet, protocolo, estructura DB ni handshake real.

El permiso `SafetyReady` no implementa ni valida un circuito de seguridad. Este brief no define PLr/SIL, resguardos certificados, parada de emergencia ni evaluación de riesgos.

## 6. Fuera de alcance de este brief

- Fabricar o dimensionar una máquina real a partir de la geometría del HTML.
- Prometer capacidad, precisión de inspección, OEE o tiempos físicos.
- Elegir o comprar hardware antes de acordar producto, producción, interfaces y requisitos de seguridad.
- Asignar direcciones TIA como si ya existiera un proyecto PLC real.
- Afirmar que el sistema Safety del simulador es apto para uso industrial.

## 7. Preguntas abiertas para convertir el borrador en un URS

1. ¿Qué pieza real se inspecciona? Facilitar planos, variantes, material, dimensiones y tolerancias.
2. ¿Qué defectos debe detectar la visión y qué condiciones definen OK/NOK? ¿Cuál es la tasa de error aceptable?
3. ¿Cuál es la producción objetivo (piezas/minuto), disponibilidad y patrón de operación por turno?
4. ¿Cómo se presenta la pieza y qué requisitos hay para reposición del cargador, atascos y acumulación en A/B?
5. ¿Qué señal confirma que la pieza llegó a inspección, fue evaluada y abandonó cada salida?
6. ¿Qué PLC, HMI, accionamientos y red industrial están normalizados en la planta? ¿Hay restricciones de marca o protocolo?
7. ¿Qué cámara Cognex, óptica, iluminación, controlador y enlace de datos se requieren? ¿El resultado será un bit, código, medida o conjunto de valores?
8. ¿Qué peligros, modos de acceso, tiempos de parada y nivel de reducción de riesgo exige la evaluación de Safety?
9. ¿Qué condiciones de aceptación deben superar FAT y SAT? ¿Quién firma cada prueba?
10. ¿Qué documentación eléctrica, neumática, idioma, mantenimiento, repuestos y formación debe entregarse?

## 8. Aceptación del paquete didáctico

Este primer paquete se considerará listo para revisión cuando:

- el lector pueda distinguir hechos del simulador, propuestas y preguntas pendientes;
- el caso de enseñanza cubra alimentación, inspección simulada y clasificación `OK → A` / `NOK → B`;
- el lote 4/3 se describa como dato de demostración y no como objetivo de producción;
- los elementos no implementados (PLC físico, Cognex, direcciones y Safety) estén señalados sin ambigüedad.

**Aprobación de cliente real:** no aplica; no hay cliente identificado.  
**Revisión didáctica D2R:** pendiente.  
**Siguiente documento:** especificación funcional, con secuencia, modos, estados, transiciones y criterios de prueba trazados a `REQ-001`…`REQ-009`.
