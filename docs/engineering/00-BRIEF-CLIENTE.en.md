# 00 · Client brief and initial requirements

**Status:** teaching draft · review pending  
**Date:** 2026-11-11  
**Case:** D2R Inspection Cell  
**Current behavior source:** [functional prototype](../../D2R-3D-001_Prototipo_Funcional_v11.html)

> No brief signed by a real client has been provided. This document reconstructs a learning scenario from the simulator and separates observable facts from decisions that still need to be made.

## 1. Proposed scenario

An inspection cell presents individual parts on a conveyor, performs a visual inspection, and directs each part to an output according to the result. The operator must be able to start an automatic batch or request one part at a time, observe machine status, and review signals and counters.

This text is a **teaching proposal**, not a requirement attributed to an identified company. The actual product, inspection tolerances, production rate, and line interfaces must be defined before selecting hardware.

## 2. Learning objective

Teach how to develop an inspection-cell project in stages: turn requirements into functional, mechanical, and electrical designs; select hardware; structure and program the PLC; define Safety Engineering; and prepare commissioning and acceptance.

The simulator is a study and demonstration tool. It is not a PLC running a real machine program and does not validate an industrial design.

## 3. Behavior currently represented

These points describe the prototype; they are not yet client-approved requirements:

- A magazine displays a stack of parts and animates extraction of the bottom part onto the conveyor.
- The conveyor carries the part to a simulated visual-inspection station and stops during the logical capture.
- The inspection result comes from the teaching batch, not from an algorithm that analyzes the part geometry.
- The demonstration batch contains seven results: `OK, NOK, OK, NOK, OK, OK, NOK`.
- Classification routes are `OK → A` via the side pusher and `NOK → B` at the end of the conveyor.
- `AUTO` runs the batch continuously; `PIEZA` processes one part per START command.
- STOP requests completion of the current part before stopping the cycle.
- The HMI shows status, mode, and counters; PLC Watch displays simulated signals and conceptual values.
- HMI RESET is restricted to a stopped machine. SIM RESET and pause control the simulation environment and must not be described as equivalent PLC commands.

The sequence has phases and durations defined in the HTML. These are simulated model times; they are not takt time, production capacity, or real equipment response times.

## 4. Preliminary requirements for the exercise

All requirements in this table are **proposals derived from the prototype** and need validation before they can be treated as client requirements.

| ID | Proposed requirement | Observable simulator criterion | Status |
| --- | --- | --- | --- |
| REQ-001 | The cell shall present one part per cycle on the conveyor. | One active part is visibly fed from the stack without duplication during the cycle. | Teaching proposal |
| REQ-002 | Each part shall pass through a visual-inspection station. | The INSPECT phase and its simulated signals are visible. | Teaching proposal; real inspection pending |
| REQ-003 | An OK result shall go to A and a NOK result to B. | In the example batch: four parts leave through A and three through B. | Route confirmed in simulator; inspection criteria pending |
| REQ-004 | AUTO and PIEZA modes shall be available. | AUTO runs the batch; PIEZA advances one part per START command. | Behavior present; operator approval pending |
| REQ-005 | STOP shall finish the current part and then stop the sequence. | The cycle does not stop immediately when FIN DE PIEZA is requested. | Behavior present; client approval pending |
| REQ-006 | The operator shall be able to see mode, status, and accumulated production. | The HMI shows READY/RUN, mode, OK, NOK, and total. | Behavior present; final HMI content pending |
| REQ-007 | Signal diagnostics shall be available during engineering and commissioning. | PLC Watch exposes simulated I/O and values. | Teaching tool present; it does not define a real PLC Watch Table |
| REQ-008 | The camera shall exchange trigger, ready, result, and acknowledgement signals. | Only a simulated logical exchange exists in the prototype. | Proposal; vendor, model, protocol, and data map pending |
| REQ-009 | The machine shall have a documented and verifiable safety concept. | The simulator displays a conceptual permission signal. | Risk assessment pending; no Safety function or certification evidence |

## 5. Demonstration data and limitations

The fixed 4 OK/3 NOK batch checks routes and counters. It **does not mean** the real process should produce that ratio. The 3D part and its visible details are graphics; they do not define the dimensions, material, tolerances, or acceptable defects of a real product.

Signals named `DI`, `DQ`, and `DB`, and types BOOL, INT, DINT, REAL, or TIME, are a conceptual representation in Watch. No physical addresses, CPU, TIA project, connected camera, or active external electronic exchange exist.

The Cognex camera is a possible component to study, not a selection. No model, lens, lighting, Ethernet interface, protocol, DB structure, or real handshake has been selected.

`SafetyReady` does not implement or validate a safety circuit. This brief does not define PLr/SIL, certified guards, emergency stop, or a risk assessment.

## 6. Out of scope for this brief

- Building or sizing a real machine from the HTML geometry.
- Promising throughput, inspection accuracy, OEE, or physical timings.
- Selecting or purchasing hardware before product, production, interfaces, and safety requirements are agreed.
- Assigning TIA addresses as if a real PLC project already existed.
- Claiming that the simulator's Safety system is suitable for industrial use.

## 7. Open questions to turn this draft into a URS

1. What real part will be inspected? Provide drawings, variants, material, dimensions, and tolerances.
2. Which defects must vision detect, and what defines OK/NOK? What error rate is acceptable?
3. What are the target output (parts/minute), availability, and shift pattern?
4. How is the part presented, and what are the requirements for magazine replenishment, jams, and accumulation at A/B?
5. Which signal confirms that a part arrived at inspection, was evaluated, and left each output?
6. Which PLC, HMI, drives, and industrial network are standardized at the plant? Are there vendor or protocol restrictions?
7. Which Cognex camera, optics, lighting, controller, and data link are required? Will the result be a bit, code, measurement, or set of values?
8. What hazards, access modes, stopping times, and risk-reduction level will the Safety assessment require?
9. Which acceptance conditions must pass FAT and SAT, and who signs each test?
10. Which electrical and pneumatic documents, languages, maintenance information, spares, and training must be delivered?

## 8. Acceptance of the teaching package

This first package is ready for review when:

- readers can distinguish simulator facts, proposals, and open questions;
- the teaching case covers feeding, simulated inspection, and classification `OK → A` / `NOK → B`;
- the 4/3 batch is described as demonstration data, not a production target;
- unimplemented items (physical PLC, Cognex, addresses, and Safety) are clearly identified.

**Real-client approval:** not applicable; no client has been identified.  
**D2R teaching review:** pending.  
**Next document:** [01 · Functional specification](01-FUNCTIONAL-SPECIFICATION.en.md), a teaching draft available for review against the open questions in this brief.
