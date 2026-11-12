# 02 · Mechanical, electrical, and pneumatic design

**Status:** teaching draft v0.1 · review pending  
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
