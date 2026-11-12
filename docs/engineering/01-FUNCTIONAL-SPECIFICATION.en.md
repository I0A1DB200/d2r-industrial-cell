# 01 · Functional specification

**Status:** teaching draft v0.1 · review pending  
**Objective:** turn document 00 into behaviors and reviewable criteria before design or programming begins.

> The simulator shows a proposed sequence. The statements here are not signed requirements or evidence from a physical machine.

## Inputs and scope

- Main input: document 00 · Client brief and its open questions about product, production, inspection, interfaces, and Safety.
- Includes: single-part feeding, transport, inspection capture, OK/NOK decision, discharge, and HMI operation.
- Excludes: real vision algorithm, sensor selection, capacity calculation, selected hardware, and implemented Safety functions.
- The HTML sequence is a teaching reference; its durations are not production setpoints.

## Observable reference behavior

| Prototype phase | Model duration | Represented behavior |
| --- | ---: | --- |
| `FEED` | 0.8 s | Releases one part from the feeder. |
| `TRAVEL_VISION` | 2.2 s | Transports the part to inspection. |
| `INSPECT` | 1.5 s | Stops the conveyor and presents the logical trigger/capture. |
| `TRAVEL_SORT` | 1.9 s | Transports the part toward sorting. |
| `SORT_STOP` | 0.5 s | Stops the part at the sorting position. |
| `DISCHARGE` | 2.2 s | Represents OK ejection or travel toward output B. |
| `PUSH_RETRACT` | 1.1 s | Represents return and output confirmation. |

The fixed batch `OK, NOK, OK, NOK, OK, OK, NOK` only exercises the two routes: `OK → A` and `NOK → B`. It does not define a real quality ratio.

## Modes and commands

- `AUTO`: processes the demonstration batch continuously.
- `PIEZA`: one START command requests one part; another START requests the next.
- `FIN DE PIEZA`: STOP requests completion of the active part before the machine becomes stopped.
- `RESET HMI`: available while stopped; resets the model's operating state.
- Simulator `PAUSA`: freezes the animation and simulation clock. It is not equivalent to a safe pause on a real machine.
- `RESET SIM`: restarts the demonstration environment; it is not a PLC command.

## Proposed criteria

| ID | Reviewable criterion | Traceability | Status |
| --- | --- | --- | --- |
| `TC-001` | One part is presented per cycle without visual duplication. | `REQ-001` | Proposed; observable in simulation |
| `TC-002` | The part reaches inspection and the conveyor stops during `INSPECT`. | `REQ-002` | Proposed; real capture pending |
| `TC-003` | The accepted result follows route A or B according to the batch. | `REQ-003` | Routes present in prototype |
| `TC-004` | AUTO and PIEZA respect the requested number of commands. | `REQ-004` | Proposed for client review |
| `TC-005` | FIN DE PIEZA completes the active cycle, then prevents new cycles. | `REQ-005` | Present as simulated behavior |
| `TC-006` | The HMI presents understandable mode, status, and counters. | `REQ-006` | Draft; final content pending |
| `TC-007` | The vision exchange is confirmed before a result is used. | `REQ-008` | Proposed requirement; no real interface exists |

## Open decisions

Define the product and its variants, defects and OK/NOK limits; target production; behavior on missing parts or jams; physical confirmation of each output; and the required response to communication loss. The customer and process, maintenance, and Safety owners should review these points before freezing the specification.

**Output artifact:** approved functional specification and traceability matrix.  
**Next stage:** mechanical, electrical, and pneumatic design. The displayed timings do not transfer automatically to the real design.
