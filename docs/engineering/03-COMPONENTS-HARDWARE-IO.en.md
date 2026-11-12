# 03 · Components, hardware, and I/O map

**Status:** teaching draft v0.1 · selection pending  
**Objective:** convert functional interfaces into a traceable equipment and signal list before assigning models or addresses.

## Hardware-selection criteria

| Item | Information required before selection | Current status |
| --- | --- | --- |
| PLC and I/O | Point count/type, spare capacity, cycle, network, diagnostics, and Safety requirements. | CPU, modules, and addresses not selected. |
| HMI | User roles, screens, languages, recipes, alarms, access, and connection. | Only a simulated panel exists. |
| Conveyor drive | Speed, load, cycle rate, braking, supply, and diagnostics. | No real motor or drive is modeled. |
| Valves and sensors | Pressure, loads, strokes, environment, wiring, and required detection. | Conceptual signals; no models selected. |
| Cognex vision | Part, defects, field of view, optics, lighting, exposure time, network, and result format. | Brand mentioned as a possibility; no model or connection. |

Selection should consider electrical and network compatibility, availability, spares, plant standards, support, and total cost. Do not assign part numbers without product and environmental data.

## Tags present in the prototype

These names belong to the HTML Watch. They are conceptual tags without physical addresses.

| Group | Current tags |
| --- | --- |
| DI | `DI_MagazinePart`, `DI_InspectionPresent`, `DI_RejectPosition`, `DI_PusherRetracted`, `DI_PusherExtended`, `DI_ExitA`, `DI_ExitB` |
| DO | `DO_ConveyorRun`, `DO_FeederValve`, `DO_PusherValve`, `DO_VisionTrigger` |
| Inspection / permission logic | `VisionReady`, `InspectionDone`, `InspectionValid`, `VisionOK`, `SafetyReady` |
| INT | `DB_SequenceStep`, `DB_PieceIndex` |
| DINT | `DB_CountOK`, `DB_CountNOK`, `DB_CountTotal` |
| REAL | `DB_BeltSpeed` (m/s), `DB_PieceX` (mm), `DB_PusherPos` (mm) |
| TIME | `DB_StageElapsed` (ms in Watch presentation) |

Do not change the names, types, or units of normal Watch variables when implementing this interface in a PLC. Confirm each variable's meaning and scale before mapping it; `DB_PieceX` and `DB_PusherPos` are derived from the visualization, not calibrated physical measurements.

## Future map and external device

Prepare an assignment table with tag, description, electrical type, PLC address, device/terminal, safe state, filtering/diagnostics, and test case. Keep addresses `TBD` until the CPU and modules are selected.

For the camera, agree data ownership and update cycle before creating the DB: `DO_VisionTrigger` could drive the camera's physical trigger input or be a network command, depending on the selected interface. The Cognex returns `Ready`, `Busy/Done`, `Valid`, result, and diagnostics; the PLC maps accepted data into its exchange DB and associates it with the correct part. Distinguish the Cognex job/own storage from the exchange DB in the PLC; its content and protocol depend on the selected model. The simulator exposes only basic logical signals; it has no external handshake or active electronic database.

**Output artifact:** approved equipment list, I/O count with spare capacity, and address table.  
**Pending:** URS, layout, Safety assessment, plant network, selected models, and address assignment.
