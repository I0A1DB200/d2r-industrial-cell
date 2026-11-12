# 05 · Arquitectura PLC: OB, FC, FB, DB, UDT y tags

**Estado:** propuesta didáctica v0.2 · TIA Portal por confirmar
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

## Árbol de proyecto propuesto

```text
PLC
├── PLC tags
│   ├── DI_Raw / DQ_Command       (mapeo I/Q del hardware seleccionado)
│   └── DB_HMI_Interface          (tags públicos de operador/diagnóstico)
├── PLC data types
│   ├── UDT_CellCommand
│   ├── UDT_CellStatus
│   ├── UDT_VisionExchange
│   └── UDT_AlarmEntry
└── Program blocks
    ├── OB1_Main
    ├── FB10_CellSequence         + DB_CellSequence
    ├── FB20_Feeder               + DB_Feeder
    ├── FB30_Conveyor              + DB_Conveyor
    ├── FB40_VisionInterface       + DB_VisionInterface
    ├── FB50_Sorter                + DB_Sorter
    └── FC10_ValidateCommands
```

Es un árbol didáctico que se ajustará a versión TIA, norma del proyecto, diagnóstico requerido y tamaño real. No se ha creado ningún bloque en TIA Portal.

## Qué resuelve cada elemento TIA

| Elemento | Qué contiene/ejecuta | Cuándo encaja aquí | Decisión de diseño |
| --- | --- | --- | --- |
| OB | Punto de entrada por ciclo o evento de CPU. | `OB1_Main` coordina el ciclo cíclico. OB de arranque/diagnóstico solo si requisitos/hardware lo necesitan. | Evitar meter toda la secuencia en OB1. |
| FC | Lógica invocable sin DB de instancia propio. | Validar un rango, convertir unidades, preparar una estructura. | Preferir entradas/salidas explícitas y no depender de variables globales ocultas. |
| FB | Lógica con memoria estática por instancia. | Secuencia de célula, alimentador, cinta, visión y expulsor. | Cada instancia conserva su estado, tiempos y diagnóstico. |
| DB de instancia | Datos privados asociados a una instancia de FB. | `DB_Feeder`, `DB_Conveyor`, `DB_Sorter`, etc. | No exponer todos los datos privados a HMI sin necesidad. |
| DB global | Datos globales con interfaz acordada. | HMI, intercambio de cámara, configuración autorizada. | Definir propietario y permisos de escritura por campo. |
| UDT | Tipo compuesto reutilizable. | Estructuras de comandos, estados, alarmas y datos de visión. | Versionar cambios de interfaz y revisar compatibilidad. |

Un bloque de organización de diagnóstico (por ejemplo, evento de fallo de módulo) depende de CPU, módulos y configuración. No se prescribe un OB concreto sin el inventario de hardware.

## Esquemas de datos candidatos

Los campos siguientes son una propuesta para discutir. Hay que validarlos con software, HMI, visión, mantenimiento y red antes de fijarlos.

| Estructura/campo | Tipo candidato | Propietario | Regla propuesta |
| --- | --- | --- | --- |
| `UDT_CellCommand.StartReq` | BOOL | HMI | Solicitud momentánea; PLC detecta flanco y valida. |
| `UDT_CellCommand.StopAfterPartReq` | BOOL | HMI | Solicita terminar la unidad activa. |
| `UDT_CellCommand.ResetReq` | BOOL | HMI | Se acepta solo con precondiciones acordadas; no rearma Safety. |
| `UDT_CellCommand.ModeRequest` | USINT/ENUM | HMI | Valor validado; cambio de modo sujeto a estado de máquina. |
| `UDT_CellStatus.State` | UINT/ENUM | PLC | Estado único, con tabla de valores versionada. |
| `UDT_CellStatus.PieceIndex` | INT | PLC | Índice de pieza según regla de lote acordada. |
| `UDT_CellStatus.CountOK/CountNOK` | DINT | PLC | Actualizar solo al confirmar finalización según especificación. |
| `UDT_VisionExchange.TriggerReq` | BOOL | PLC | Trigger asociado a una pieza/ciclo identificable. |
| `UDT_VisionExchange.JobId` | UINT/STRING | PLC/cámara | Campo de receta/job acordado con el modelo. |
| `UDT_VisionExchange.Ready/Busy/Done/Valid` | BOOL | Cámara | Calidad/validez revisadas antes de aceptar resultado. |
| `UDT_VisionExchange.Result` | UINT/ENUM | Cámara → PLC | Tabla de resultados documentada; OK/NOK no basta si hay clases adicionales. |
| `UDT_VisionExchange.SequenceId` | DINT | PLC | Evita asociar respuesta atrasada a otra pieza, si protocolo lo soporta. |
| `UDT_AlarmEntry.Code/Active/Ack` | UINT/BOOL/BOOL | PLC | Causa y reconocimiento separados; retención según estándar. |

La interfaz de cámara puede estar en un DB global o en estructura accesible por protocolo. El job interno de Cognex es independiente; no duplicar la propiedad del resultado.

## Flujo de ejecución cíclica

Un orden posible para `OB1_Main`, pendiente de revisión con tiempo de ciclo y módulos:

1. Leer imagen de proceso y diagnósticos de canal.
2. Convertir bits de hardware a estructuras tipadas de entrada y conservar calidad/error.
3. Validar comandos HMI y datos externos; rechazar valores inválidos con diagnóstico.
4. Ejecutar la secuencia que consume feedback y produce órdenes de equipo.
5. Ejecutar bloques de equipo que calculan salidas y temporizaciones a partir de esas órdenes.
6. Aplicar enclavamientos estándar y límites de proceso antes de escribir salidas estándar.
7. Publicar estado, contadores, valores y alarmas a HMI/diagnóstico.

Documentar si los bloques de equipo consumen órdenes de este ciclo o del anterior y medir el ciclo real. La función Safety sigue una ruta de diseño y validación separada.

## Reglas de interfaz

- Una sola fuente de verdad por valor: entrada bruta, lógica derivada, comando aceptado o estado calculado.
- Comandos HMI son solicitudes; el PLC publica si fueron aceptados y cuál es el estado real.
- El PLC retiene el resultado de visión aceptado hasta terminar la ruta o invalidarlo en recuperación definida.
- Las variables analógicas llevan unidad, resolución, rango válido, valor de sustitución y calidad.
- Las alarmas registran causa, timestamp si el hardware lo permite, activo, reconocido y condición de retorno.
- HMI no escribe salidas físicas directamente y ningún DB estándar representa las funciones Safety.

## Ejercicio de revisión en TIA

En una futura sesión, crear primero tipos y PLC tags sin asignar hardware; revisar interfaces; después añadir la CPU/módulos seleccionados, enlazar tags I/Q y compilar. Importar Watch solo cuando la tabla de tags y direcciones esté aprobada. Este documento no afirma que esa sesión ya se haya realizado.
