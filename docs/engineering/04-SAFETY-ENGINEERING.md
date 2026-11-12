# 04 · Safety Engineering

**Estado:** marco de trabajo · sin evaluación de riesgos aprobada  
**Objetivo:** establecer el proceso necesario para definir, implementar y validar las funciones de seguridad de una máquina real.

> La señal `SafetyReady` del simulador es una indicación lógica constante. No es una entrada de un relé o PLC Safety, no demuestra una función de seguridad y no debe usarse para dimensionar ni validar el sistema.

## Principio de diseño

Safety empieza con el uso previsto, los límites de la máquina y la identificación de peligros; no con copiar un bit del simulador. Una persona competente debe evaluar riesgos con la normativa aplicable al país, la máquina y la fecha del proyecto. La necesidad de PLr/SIL, arquitectura, componentes y pruebas se deriva de ese análisis.

## Trabajo necesario

1. Definir modos de operación, accesos, tareas de limpieza/desatasco, mantenimiento y condiciones previsibles de fallo.
2. Identificar peligros mecánicos, eléctricos, neumáticos y de proceso; estimar y reducir el riesgo según el método aplicable.
3. Especificar cada función de seguridad: evento iniciador, zona, reacción requerida, tiempo/distancia de parada, rearme y diagnóstico.
4. Seleccionar resguardos, enclavamientos, paradas de emergencia y elementos de control solo después de establecer los requisitos.
5. Separar el control estándar de las funciones de seguridad y definir las interfaces entre ellos.
6. Verificar el diseño y validar cada función con un protocolo trazable; registrar medidas, fallos, cambios y aprobación responsable.

ISO 12100, ISO 13849-1, IEC 62061 y las normas de tipo C que correspondan son referencias para revisar con el equipo de Safety. Citar una norma no acredita conformidad ni certifica este simulador.

## Temas por evaluar para este caso

Acceso al cargador y a zonas de pellizco; acceso a cinta, rodillos, expulsor y rampas; intervención ante atasco; energías residuales y pérdida de aire; protección de cámara/iluminación; y recuperación tras parada. Son temas de evaluación, no una lista cerrada de peligros ni una solución seleccionada.

| Entregable | Evidencia requerida | Estado |
| --- | --- | --- |
| Evaluación de riesgos | Límites, peligros, estimación, medidas y riesgo residual. | Pendiente |
| Especificación de funciones | Requisitos, zonas, estado seguro, rearme y tiempos medidos. | Pendiente |
| Diseño Safety | Arquitectura, componentes, cálculos y documentación eléctrica. | Pendiente |
| Validación | Protocolo, resultados medidos, desviaciones y aprobación. | Pendiente |

**Trazabilidad:** `REQ-009` y decisiones de operación de los documentos 01–03.  
**Límite didáctico:** el HTML mantiene su modelo conceptual existente; esta ficha no modifica ni amplía su Safety.
