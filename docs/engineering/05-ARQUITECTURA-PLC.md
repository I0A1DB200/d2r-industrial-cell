# 05 · Arquitectura PLC: OB, FC, FB, DB, UDT y tags

**Estado:** propuesta didáctica v0.1 · TIA Portal por confirmar  
**Objetivo:** organizar responsabilidades y propiedad de datos para que el programa sea legible, comprobable y ampliable.

## Capas de datos

1. **E/S de hardware:** imagen de proceso y diagnósticos de canal, vinculados a la configuración física aprobada.
2. **Datos brutos:** lectura de sensores, estados de variadores, válvulas y cámara, conservando la calidad de origen.
3. **Comandos:** solicitudes de operador e interfaces externas, validadas antes de entrar en la secuencia.
4. **Estados y alarmas:** propietario PLC, con causas, estado activo/confirmado y recuperación definida.
5. **Interfaz HMI/visión:** DB estable, con tipos, unidades, permisos y versión acordados.

El PLC debe ser dueño del estado de ciclo y de los contadores de producción. La cámara es dueña del resultado de captura hasta que el PLC lo valida y lo asocia a una pieza. HMI y Watch observan/escriben solo los campos autorizados. Esta arquitectura es una propuesta; no existe un proyecto PLC para esta célula.

## Distribución propuesta de bloques

| Bloque propuesto | Responsabilidad | Datos asociados |
| --- | --- | --- |
| `OB1_Main` | Llamar los bloques de equipo y coordinar el ciclo cíclico. | Sin lógica de estación extensa. |
| `FB10_CellSequence` | Modos, transiciones, órdenes y estado global. | `DB_CellSequence` como DB de instancia. |
| `FB20_Feeder` | Alimentación y confirmación de pieza. | `DB_Feeder` de instancia. |
| `FB30_Conveyor` | Mando y diagnóstico del transporte. | `DB_Conveyor` de instancia. |
| `FB40_VisionInterface` | Disparo, handshake, resultado y diagnóstico de cámara. | `DB_VisionInterface` de instancia y DB de intercambio acordado. |
| `FB50_Sorter` | Clasificación, expulsor y salidas. | `DB_Sorter` de instancia. |
| `FC10_ValidateCommands` | Validaciones sin memoria de instancia, cuando convenga. | Parámetros de entrada/salida explícitos. |
| `DB_HMI_Interface` | Interfaz estable para mando, estado, contadores y alarmas visibles. | Tipos de interfaz compartidos. |

Los nombres son IDs didácticos, no bloques ya creados. En TIA Portal, un FB conserva datos estáticos en su DB de instancia; un FC no tiene DB de instancia propio. Un DB global contiene datos compartidos. Un UDT define una estructura reutilizable; no ejecuta lógica.

## UDT y trazabilidad

Como candidatos, revisar `UDT_CellCommand`, `UDT_CellStatus`, `UDT_AlarmEntry` y `UDT_VisionExchange`. Separar comandos, estado, configuración, datos brutos y alarmas cuando existan consumidores distintos. Cada campo debe tener propietario, tipo, unidad, rango, ciclo de actualización y regla de validez. La base/job interna de la cámara y el DB de intercambio PLC son objetos distintos; confirmar si el modelo Cognex requiere una receta, un número de job o almacenamiento de resultados.

Safety se diseña y valida en su arquitectura correspondiente; no se sustituye por un FB estándar ni por un campo `SafetyReady` del simulador.

**Verificación:** revisión de llamadas, DB de instancia, interfaces, acceso HMI y ausencia de escrituras duplicadas al mismo dato.  
**Pendiente:** CPU/firmware, estándares de nombres, requisitos de comunicación, número de instancias y límites del equipo de software.
