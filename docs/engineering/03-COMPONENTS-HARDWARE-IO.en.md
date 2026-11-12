# 03 · Components, hardware, and I/O map

**Status:** teaching draft v0.2 · selection pending
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

## Teaching I/O sizing and BOM

Model baseline: 7 discrete inputs and 4 discrete outputs. `VisionReady`, `InspectionDone`, `InspectionValid`, and `VisionOK` are simulated logical states, not confirmed extra terminals. If the camera exchanges data over Ethernet, its fields do not consume DI/DO channels, but require interface, memory, update, and diagnostic design. If the final protocol uses discrete handshake, add those channels again.

Arithmetic example for teaching spare capacity: assuming a **classroom exercise criterion**, not a universal requirement, of 20% free channels, 7 DI require `ceil(7 × 1.2)=9` and 4 DO require `ceil(4 × 1.2)=5`. Round up to the available module size and recount camera, drive, maintenance, and expansion channels before selecting the station.

| BOM item | Specification to close | Selection method | Case status |
| --- | --- | --- | --- |
| PLC CPU | cycle, memory, communication, diagnostics, lifecycle, F-Safety if risk assessment requires it. | Compare requirements to candidate CPU and plant support; validate TIA version. | Family/model pending. |
| Standard I/O | quantity, 24 VDC or other level, output type, isolation, and diagnostics. | Tag-by-tag count plus documented spare capacity. | Baseline example 7 DI/4 DO; topology pending. |
| Safety I/O | count/type of devices/channels resulting from assessment. | Derive from Safety specification and calculate/validate architecture. | Not sized. |
| 24 VDC supply | simultaneous demand of sensors, valves, PLC/HMI, and thermal margin. | Sum nameplate currents, startup conditions, and project margin. | Currents unavailable. |
| Conveyor motor/drive | load, speed, duty, starting torque, braking, and network. | Mechanical sizing plus duty and control strategy. | No real device modeled. |
| Valves/cylinders | force, stroke, speed, duty, pressure, and sensors. | Size actuator and valve; review consumption, maintenance, and risk. | Geometry is visual only. |
| Cognex camera | defects, vision, lens, lighting, time, interface, mount, and service. | Trial with labeled parts and Quality evaluation of results. | Model/optics/job pending. |
| HMI and cabinet | size, readability, users, environment, location, and access. | Review screens/roles and plant constraints. | Panel/cabinet only represented in HTML. |

This is a working BOM, not a purchase recommendation. No SKU is given because missing variables directly affect selection.

## Detailed simulator tag inventory

Names and behavior below refer to the HTML. `DI` and `DO` are conceptual families; no TIA address table or connected hardware exists.

| Tag | Logical type | Description | Value in current model |
| --- | --- | --- | --- |
| `DI_MagazinePart` | BOOL | Part available at magazine outlet. | 1 during `FEED`; generated by phase, not physical sensor. |
| `DI_InspectionPresent` | BOOL | Part at inspection station. | 1 during `INSPECT`. |
| `DI_RejectPosition` | BOOL | Part at sorting position. | 1 during `SORT_STOP` and OK push. |
| `DI_PusherRetracted` | BOOL | Rod/carriage at retracted home. | 0 while pushing or returning; calculated from phase. |
| `DI_PusherExtended` | BOOL | Pusher extended confirmation. | 1 at end of OK extension and during the first part of return; calculated by phase. |
| `DI_ExitA` | BOOL | Graphical confirmation of output A. | 1 in final OK phase. |
| `DI_ExitB` | BOOL | Graphical confirmation of output B. | 1 in final NOK phase. |
| `DO_ConveyorRun` | BOOL | Virtual conveyor-movement command. | 1 during transport and NOK travel to output B. |
| `DO_FeederValve` | BOOL | Virtual feeder-actuator command. | Partial `FEED` window. |
| `DO_PusherValve` | BOOL | Virtual pusher-valve command. | 1 during OK push and OK return. |
| `DO_VisionTrigger` | BOOL | Logical capture trigger. | 1 during `INSPECT`; does not operate a physical camera. |
| `VisionReady` | BOOL | Camera ready for inspection. | Constant 1 in simulation. |
| `InspectionDone` | BOOL | Logical capture complete. | 1 after `INSPECT`. |
| `InspectionValid` | BOOL | Result usable by sequence. | 1 after `INSPECT`. |
| `VisionOK` | BOOL | Simulated inspection result. | Derived from fixed batch after capture. |
| `SafetyReady` | BOOL | Conceptual permission shown in Watch. | Constant 1; not a Safety function. |

Sensor states are animation proxies: for example, A/B outputs are represented at the end of a phase, not by physical photoeyes. Real engineering must specify mounting, sensing distance, sensor type, timing, cable, and diagnostics.

## Numeric variables shown in Watch

| Tag | Type | Display unit | Model rule | Teaching use / limitation |
| --- | --- | --- | --- | --- |
| `DB_SequenceStep` | INT | step number | 0 stopped; while running, phase index × 10 + 10. | Simulated step code; not a real TIA state enumeration. |
| `DB_PieceIndex` | INT | parts | batch index plus 1 while a part is running. | Can show current part. |
| `DB_CountOK` | DINT | parts | Counter for completed OK routes. | Model counter. |
| `DB_CountNOK` | DINT | parts | Counter for completed NOK routes. | Model counter. |
| `DB_CountTotal` | DINT | parts | `DB_CountOK + DB_CountNOK`. | Total parts already counted. |
| `DB_BeltSpeed` | REAL | m/s | 0 or 0.10 according to conveyor BOOL. | Discrete teaching value, not measured speed. |
| `DB_PieceX` | REAL | mm | Visual X coordinate scaled and limited to 0…800. | Illustrative 3D conversion; not calibrated. |
| `DB_PusherPos` | REAL | mm | Relative stroke × 200/1.48, limited to 0…200. | Normalized Watch scale, not real stroke in mm. |
| `DB_StageElapsed` | TIME | ms | Phase time × 1000. | Virtual clock, not PLC time or instrument reading. |

This records the existing Watch for traceability. Do not copy it as a hardware specification without reviewing resolution, precision, overflow, retention, and required units.

## Address assignment example (exercise only)

The table below demonstrates a Siemens-style example format. **These addresses are not assigned to this project.** Replace them after selecting CPU, modules, and station topology; check for overlaps in the TIA configuration.

| Example tag | Illustrative address | Signal type to confirm |
| --- | --- | --- |
| `DI_MagazinePart` | `%I0.0` | Digital input, part sensor. |
| `DI_InspectionPresent` | `%I0.1` | Digital input, station sensor. |
| `DI_RejectPosition` | `%I0.2` | Digital input, sorting presence. |
| `DI_PusherRetracted` | `%I0.3` | Digital input, cylinder sensor. |
| `DI_PusherExtended` | `%I0.4` | Digital input, cylinder sensor. |
| `DI_ExitA` / `DI_ExitB` | `%I0.5` / `%I0.6` | Digital inputs, output sensors to define. |
| `DO_ConveyorRun` | `%Q0.0` | Output to drive interface, not necessarily direct power. |
| `DO_FeederValve` | `%Q0.1` | Output to valve coil/interface as selected. |
| `DO_PusherValve` | `%Q0.2` | Output to valve coil/interface as selected. |
| `DO_VisionTrigger` | `%Q0.3` | Digital output or network command, TBD. |

Do not map `SafetyReady` to a standard output to imitate a Safety circuit. Safety devices and signals require their own channels, assessment, and architecture.

## Cognex and electronic data selection record

Before selecting a camera, document: part/variants, defect, tolerance, allowable false accept/reject rates, field of view, resolution, optics, lighting, time available while the belt is stopped, working distance, environment, mounting, job/recipe, communication, license/tools, required result, diagnostics, storage, and support.

| Proposed interface data | Logical direction | Candidate type | Owner | Status |
| --- | --- | --- | --- | --- |
| Trigger | PLC → camera | BOOL discrete or Ethernet command | PLC generates; camera accepts | Interface to select |
| Job/Recipe ID | PLC → camera | UINT/STRING per interface | PLC requests; camera validates | Pending |
| Ready / Busy | Camera → PLC | BOOL | Camera publishes | Pending |
| Done / Valid | Camera → PLC | BOOL | Camera publishes | Pending |
| Result / Score | Camera → PLC | BOOL/ENUM/REAL per criteria | Camera calculates; PLC validates and retains | Criteria pending |
| ErrorCode / JobActive | Camera → PLC | UINT/ENUM | Camera publishes | Model pending |
| Ack / ResetExchange | PLC ↔ camera | BOOL or protocol command | Ownership agreed in handshake | Pending |

This is a proposed structure, not a specific Cognex format. Confirm the selected model's documentation, protocol, and firmware; do not assume `VisionOK` represents every possible defect or device result.
