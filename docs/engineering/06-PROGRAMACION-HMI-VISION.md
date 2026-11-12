# 06 · Programación, HMI y enlace de visión

**Estado:** guía didáctica v0.1 · sin proyecto ejecutable  
**Objetivo:** explicar cómo pasar de la arquitectura PLC a lógica verificable y a una interfaz clara para operador y diagnóstico.

## Elección de lenguaje

- **LAD/KOP:** redes de permisos y condiciones discretas fáciles de revisar online con mantenimiento.
- **SCL:** transformaciones de estructuras, gestión de recetas/datos y cálculos que se lean mejor como texto estructurado.
- La secuencia puede combinar ambos lenguajes. La norma del equipo y la mantenibilidad pesan más que reescribir todo en un único estilo.

El trabajo de programación debe partir de interfaces aprobadas y pruebas unitarias de bloques. Cada transición de secuencia necesita condición de entrada, acción, condición de salida, tiempo máximo si aplica y respuesta ante fallo. No usar los tiempos acelerados del simulador como valores de máquina.

## Interfaz con la cámara

La tabla siguiente es una conversación conceptual, no un handshake implementado. El orden, flancos, retención, timeout y recuperación se acuerdan con el modelo de cámara elegido.

| Etapa | PLC | Cámara | Evidencia esperada |
| --- | --- | --- | --- |
| Preparación | Valida pieza presente, receta y permiso de proceso. | Informa lista y receta cargada. | Valores coherentes para una misma pieza. |
| Disparo | Emite `Trigger` y un ID de ciclo si el protocolo lo admite. | Acepta el disparo e inicia captura. | Acknowledgement o transición observable. |
| Resultado | Espera captura completa y resultado válido. | Devuelve OK/NOK, validez y diagnóstico acordado. | Resultado asociado al ID de pieza correcto. |
| Cierre | Registra/consume el resultado una sola vez y libera el intercambio. | Vuelve a `Ready` según su interfaz. | Sin resultado antiguo ni duplicado. |

La simulación presenta `DO_VisionTrigger`, `VisionReady`, `InspectionDone`, `InspectionValid` y `VisionOK`; el resultado proviene del lote interno. No hay comunicación electrónica con una cámara.

## HMI y Watch

El HMI de máquina debe priorizar modo, estado, START, FIN DE PIEZA, RESET permitido, alarma y producción. Confirmaciones, permisos de usuario, navegación y detalle de alarmas se acuerdan en la especificación. La pausa del simulador congela el reloj gráfico; una máquina real requiere una definición de parada operacional específica y análisis de riesgo.

PLC Watch es una herramienta de observación/puesta en marcha, no la HMI de producción. Mantener los nombres y tipos existentes del prototipo como referencia: BOOL, INT, DINT, REAL y TIME. Antes de exportar una tabla real se validan dirección, unidad, rango, calidad y retención.

## Verificación del software

Planificar casos para cada bloque, transición, rechazo, pérdida de handshake, señal ausente, timeout, reinicio y recuperación. Registrar precondiciones, estímulo, resultado esperado, valor observado y evidencia. Los fallos deben proceder de una condición lógica comprobable; no se deben inyectar averías para dar por válida una alarma.

**Artefacto de salida:** fuente PLC versionada, lista de tags HMI/visión y matriz de pruebas aprobada.  
**Trazabilidad:** `REQ-002`…`REQ-008`; bloques propuestos en el documento 05.
