# 01 · Functional specification

**Status:** teaching draft v0.2 · review pending
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

## Functional sequence breakdown

| Step | Entry/advance condition | Represented actions | Confirmation or output |
| --- | --- | --- | --- |
| Ready | RESET complete and operating conditions available. | No movement; wait for START. | READY state; batch prepared. |
| `FEED` | START and a part available in the model. | Feed pulse/window; bottom part leaves the magazine. | Active part on conveyor. |
| `TRAVEL_VISION` | Feeding ends. | Conveyor runs toward inspection. | `DI_InspectionPresent` becomes 1 in the next phase. |
| `INSPECT` | Part is at the camera position. | Conveyor stopped; `DO_VisionTrigger` active; logical camera ready. | Simulated `InspectionDone`, `InspectionValid`, and result. |
| `TRAVEL_SORT` | Result is recorded in the model. | Conveyor transports the part again. | Arrival at sorting zone. |
| `SORT_STOP` | Part is at the sorting position. | Conveyor stopped; cycle result is known. | Simulated sorting position. |
| `DISCHARGE` | OK/NOK result available. | OK: pusher moves part through transfer A. NOK: conveyor moves it toward B. | Part leaves sorting position. |
| `PUSH_RETRACT` | End of OK discharge or B-exit confirmation. | OK: pusher retracts; NOK: conveyor discharge completes. | Counter updated and cycle complete. |
| Between parts | Part complete and batch has remaining units. | Wait `0.9 s` on the prototype clock. | Start next part or remain stopped after FIN DE PIEZA. |

The phase names and times above belong to the Three.js model. A real machine needs sensor-driven transitions and customer requirements; it should not be programmed with timer-only transitions.

### Simulated signal sequence

| Phase | Conveyor `DO_ConveyorRun` | `DO_FeederValve` | `DO_PusherValve` | Logical vision |
| --- | --- | --- | --- | --- |
| `FEED` | 0 | Active during part of phase | 0 | No capture |
| `TRAVEL_VISION` | 1 | 0 | 0 | No capture |
| `INSPECT` | 0 | 0 | 0 | Trigger active; presence 1; simulated ready 1 |
| `TRAVEL_SORT` | 1 | 0 | 0 | Result already recorded by the batch |
| `SORT_STOP` | 0 | 0 | 0 | No new trigger |
| `DISCHARGE` OK | 0 | 0 | 1 | OK result retained in cycle |
| `DISCHARGE` NOK | 1 | 0 | 0 | NOK result retained in cycle |
| `PUSH_RETRACT` OK | 0 | 0 | 1 | Output A represented |
| `PUSH_RETRACT` NOK | 0 | 0 | 0 | Output B represented |

`VisionReady`, `InspectionDone`, `InspectionValid`, `VisionOK`, and `SafetyReady` are virtual simulation signals. Camera ready and Safety permission do not represent feedback from real equipment.

## Command and priority matrix

| Command | Prototype state allowed | Observed effect | Real-machine definition still required |
| --- | --- | --- | --- |
| START | READY | Starts AUTO batch or one PIEZA part. | Debounce, acknowledgement, start permissives, and command reset. |
| FIN DE PIEZA / STOP | RUN | Requests a stop after the active part finishes. | Stop category, fault response, and drive stopping behavior. |
| AUTO / PIEZA | READY | Selects continuous run or one part per START. | Mode-change permissive and behavior during a process. |
| HMI RESET | READY | Resets the model's process state/counters. | Alarm acknowledgement, reset source, and restart prevention. |
| Simulator PAUSE | RUN | Freezes logical clock and animation. | Do not transfer directly; define operational pause and risk assessment. |
| RESET SIM | Any state | Restarts the entire demonstration scene. | No machine-command equivalent. |

Recommended real-program processing order: acquire inputs → validate communications and permissions → process commands → update equipment states → evaluate transitions → calculate outputs → publish diagnostics. This chain does not replace the Safety architecture.

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

### Test procedure per requirement

1. Record software version, mode, batch, part, and starting index.
2. Capture Watch values before START and during each relevant phase.
3. Confirm conveyor state during INSPECT, vision result, and discharge route.
4. Reconcile part, result, and counter; repeat with RESET to confirm the initial state.
5. Mark evidence as **SIM** for HTML, **PLC** for online observation, or **PHYSICAL** for measurement on real equipment.

Current evidence can only be **SIM**. The final protocol needs numeric criteria and customer-approved signatures.

## Open decisions

Define the product and its variants, defects and OK/NOK limits; target production; behavior on missing parts or jams; physical confirmation of each output; and the required response to communication loss. The customer and process, maintenance, and Safety owners should review these points before freezing the specification.

**Output artifact:** approved functional specification and traceability matrix.  
**Next stage:** mechanical, electrical, and pneumatic design. The displayed timings do not transfer automatically to the real design.
