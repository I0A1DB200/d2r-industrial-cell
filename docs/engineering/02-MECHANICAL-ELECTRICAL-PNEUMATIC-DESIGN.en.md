# 02 · Mechanical, electrical, and pneumatic design

**Status:** teaching draft v0.2 · review pending
**Objective:** translate the functional sequence into coordinated stations, actuators, sensors, and design documents.

> The HTML geometry is a visual representation. It is not released CAD, a manufacturing drawing, or a structural calculation.

## Proposed functional layout

| Station | Function | Items to define during engineering |
| --- | --- | --- |
| Feeder | Present one part at a time from the magazine. | Magazine, guides, retention, pusher, cylinder, replenishment, and level/part detection. |
| Transport | Move the part to inspection and sorting. | Belt, drive, rollers, guides, structure, and motion confirmation. |
| Inspection | Illuminate, capture, and evaluate the stopped part. | Camera support, optics, lighting, ambient-light protection, and part reference. |
| Output A | Divert OK parts using the side pusher and ramp. | Useful stroke, guidance, stops, bin, and exit confirmation. |
| Output B | Deliver NOK parts at the end of the conveyor. | Transfer, bin, retention, and exit confirmation. |

The cabinet shown next to the feeder is only a visual reference; its final location depends on access, wiring, environment, and maintenance requirements.

## Electrical and control interfaces

As an initial concept, discrete inputs represent presence, retracted/extended position, and output confirmation. Outputs represent conveyor, valve, and vision-trigger commands. Power, signal type, protection, connectors, grounding, power/control segregation, and network design remain open.

The Cognex camera connection is treated as an external device: a trigger from the control system and returned ready, capture, and result data. No camera, data link, or external DB is currently connected.

## Pneumatic concept

The visual model represents a feeder mechanism and a pusher with a cylinder. Real selection requires load, stroke, speed, cycle rate, available pressure, guidance, cushioning, end-position detection, and consumption assessment. The schematic must show air preparation, valves, ports, actuators, sensors, and the state on loss of energy or air as determined by the risk assessment.

## Design package to produce

- 2D/3D layout with dimensions, interfaces, maintenance, and part replenishment.
- Assembly and detail drawings, bill of materials, and manufacturing tolerances.
- Electrical drawings, 24 VDC distribution, protection, terminals, wiring, and cable list.
- Pneumatic diagram, valve/actuator list, and state table.
- Interface table across mechanical, electrical, PLC, camera, and Safety disciplines.

## Design verification

Review collisions, operator reach, bin removal, camera visibility, sensor/actuator access, maintenance, and cable/hose protection. Confirm that each sensor can be adjusted and replaced without unplanned dismantling. Simulator captures help explain layout and sequence; they do not prove safety distances, strength, ergonomics, or real performance.

**Traceability:** `REQ-001`…`REQ-003`, `REQ-008`, and `REQ-009`.  
**Pending:** drawings, product dimensions, loads, available utilities, environment, and risk review.

## Mechanical assembly breakdown shown in the model

| Assembly | Process function | Confirmed in HTML | Real engineering still required |
| --- | --- | --- | --- |
| Gravity feeder | Hold parts and present the bottom part. | Four open guides; one active part and up to six above it; visual stack drop after extraction. | Part tolerances, capacity, replenishment, retention, jams, and empty-magazine detection. |
| Feed pusher | Extract the bottom part and transfer it to the belt. | Carriage, pusher, support tongue, and visual cylinder facing +X. | Load, buckling, guidance, force, stroke, cushioning, and pinch-point protection. |
| Conveyor | Transport and hold the part during inspection. | Bed and belt share a top surface; rollers and side guides are shown. | Product size, required speed, motor/gearbox, belt tension, and motion detection. |
| Vision gantry | Position camera and lighting over the stopped part. | Graphical overhead camera, bracket, light, and visual illumination cone. | Field of view, depth of field, optics, real lighting, mount, and inspection-capability validation. |
| Side pusher | Move OK parts by contact toward output A. | Plate on a moving carriage, connected rod, horizontal bridge, and inclined ramp. | Force, guidance, permitted contact, edge design, wear, part exit, and guarding. |
| Output B | Receive NOK parts at the end of transport. | Final section and collection box are illustrated. | Drop height, accumulation, removal, presence, and bin capacity. |

### Visual geometry references

These coordinates and dimensions help read the model; they are not manufacturing dimensions. The HTML uses graphical units without validated CAD scale or tolerances.

| Model reference | Represented value | Note |
| --- | --- | --- |
| Feeder group origin | `x = -2.98`; local axis `x = -1.02` (world `x ≈ -4`) | Visual location relative to the belt. |
| 3D part | `0.52 × 0.135 × 0.38` | Visual box with five simulated holes. |
| Stack pitch | `0.135` | One active bottom part plus up to six above it. |
| Conveyor top surface | `y = 1.2925` | Visually aligns with the underside of the part. |
| Pusher cylinder body | Length `1.80`, radius `0.13`, local center `(0, 1.385, 2.20)` | Body and end caps are fixed in the sort group. |
| Pusher plate | `(0, 1.385, 0.80)`, `0.59 × 0.16 × 0.075` | At rest its face stays outside the belt edge. |
| Graphical pusher stroke | `1.48` | The rod follows the carriage; this is not a selected machine stroke. |
| Visual plate/belt clearance | Rest contact face `z=0.7625`; belt edge `z=0.55`; plate underside `y=1.305`. | Plate is outside the path and above the top surface; tolerances are not included. |

| Conveyor item | Visual reference | Note |
| --- | --- | --- |
| Main bed | Center `y=1.13`, height `0.215`. | Top face aligns with belt underside. |
| Belt | Center `y=1.265`, thickness `0.055`; top face `y=1.2925`. | Material and texture are graphical only. |
| End rollers | Center `y=1.13`, radius `0.16`. | No real shaft, drive, or transmission is modeled. |
| Part guides | Approximately `y=1.31`. | Not a product-containment calculation. |
| Output-A bridge | Top surface `y=1.2925`; from belt edge to local sort `z≈-0.7175`. | Visual transfer alignment. |
| Ramp A | Graphical width `0.88`, end near `z=-2.25`, drop `0.54`. | Visual slope; drop, friction, and accumulation calculations are missing. |

### Feeder visual path

Within `FEED` (0.8 s in the model): `0–0.45` advances the pusher (visual stroke `1.0`) and moves the bottom part from `x=-4` to `x=-3`; `0.45–0.75` returns the carriage while the part stays at `x=-3`; `0.75–0.78` waits; `0.78–1.00` animates the stack down quadratically by one `0.135` step. A rear tongue visually supports the stack during advance and withdraws before the drop. This is graphical kinematics, not a gravity calculation or validated real actuator.

### OK-pusher visual path

The sort group is at `x=1.25`. During `SORT_STOP` the part is held; during `DISCHARGE` the plate approaches and pushes by contact, with part travel clamped at zero until its face reaches the plate. During `PUSH_RETRACT`, the OK part tips at the start of its path then follows the ramp while the cylinder retracts. NOK parts travel on the belt to B and do not actuate the pusher. These are model rules for explaining interfaces and movement; they do not simulate force, friction, or gravity.

The ramp and OK-part path are tuned for visual continuity. Their angle, height, and path are not calculated results for drop, friction, or sizing.

## Candidate electrical architecture

The following diagram shows possible functional boundaries; it is not an approved connection and does not define signal types:

```text
Presence/position sensors ──────> PLC inputs
Operator HMI ───────────────────> commands / status in PLC
PLC ──> conveyor drive
PLC ──> feeder valve and pusher valve
PLC ──> camera Trigger input (I/O or network, TBD)
Camera ──> Ready / Done / Valid / Result to PLC exchange DB
Safety devices ──> independent Safety system, to be designed and validated
```

These lines do not mean the equipment is installed. Confirm network architecture, supplies, isolation, common references, protection, and diagnostics before producing electrical drawings.

## Cross-discipline interface schedule

| Interface | Defined by | Handoff to next discipline | Joint review |
| --- | --- | --- | --- |
| Part ↔ feeder | Envelope, mass, orientation, and tolerances. | Part drawing and variation range. | Mechanical + process. |
| Belt ↔ vision | Speed, stop, repeatable position, and allowable vibration. | Capture window and part-present signal. | Mechanical + controls + vision. |
| PLC ↔ Cognex | Trigger, job/recipe, result, validity, diagnostics, and timeout. | Versioned data table and configuration tool. | Controls + vision + customer. |
| Pusher ↔ part/ramp | Contact face, force, stroke, orientation, and complete exit. | Motion envelope and A confirmation. | Mechanical + controls + maintenance. |
| Electrical ↔ pneumatic | Valve, voltage, pressure, end sensors, and return. | Terminal/tag list and pneumatic schematic. | Electrical + mechanical + controls. |

## Review before design freeze

First establish part dimensions and mass, product stability on the belt, required output, feeder variation, camera exposure time, available utilities, bin space, and maintenance access. Then perform interference, ergonomics, and wiring reviews. None of these values can be inferred from the 3D view.
