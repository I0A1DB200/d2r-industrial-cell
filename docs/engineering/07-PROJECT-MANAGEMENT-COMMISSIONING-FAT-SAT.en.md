# 07 · Project management and commissioning

**Status:** teaching work plan v0.2 · no physical tests executed
**Objective:** organize deliverables, reviews, and tests from the brief through acceptance of a real installation.

## Milestones and review gates

| Gate | Output package | Entry criterion for next gate |
| --- | --- | --- |
| G0 · Kickoff | Scope, owners, risks, and customer questions. | Owner identified for each decision. |
| G1 · Requirements | URS/brief and traceable functional specification. | Verifiable requirements and agreed exceptions. |
| G2 · Design | Layout, mechanical design, electrical/pneumatic schematics, and interfaces. | Interdisciplinary reviews closed. |
| G3 · Hardware and Safety | BOM, addresses, risk assessment, and Safety design. | Selection and validation planned by competent owners. |
| G4 · Software | PLC, HMI, camera, alarms, and version documentation. | Compilation, simulation, and integration tests recorded. |
| G5 · FAT | Factory acceptance protocol and results. | Deviations resolved or formally accepted. |
| G6 · SAT | Installation, plant interfaces, safety, and process tests. | Site tests accepted by the customer/team. |
| G7 · Handover | As-built, backups, manuals, training, and spares. | Final package and operating owners accepted. |

The actual order may vary by contract and risk assessment. No simulator capture replaces FAT, SAT, or Safety validation.

## Commissioning preparation

Before energizing, review mechanical release, drawings, connections, cable identification, grounding, air, network, software versions, backups, and work permits. Then check I/O with equipment isolated and under an approved procedure; test actuators individually; verify camera and recipe; integrate the sequence; and measure acceptance criteria with suitable instruments.

Define criteria in advance for: one-part feeding, inspection stop, result-to-part association, route A/B, counting, FIN DE PIEZA, RESET, communication recovery, alarms, recipe changes, and safe behavior. For each test, state initial condition, steps, expected, measured, owner, and evidence.

## Initial proposed FAT/SAT matrix

| Case | Test | Evidence type |
| --- | --- | --- |
| `TC-101` | Full AUTO run and reconciliation of parts/counters. | PLC/HMI record and product observation. |
| `TC-102` | PIEZA, FIN DE PIEZA, RESET, and recovery after an operational stop. | Approved protocol and state record. |
| `TC-103` | Camera communication loss and recovery. | Logs, diagnostic, and part association. |
| `TC-104` | OK/NOK result and physical check of A/B. | Challenge samples and signed acceptance. |
| `TC-105` | Validation of each Safety function. | Safety protocol, measurements, and competent-person report. |

These cases are a template. Limits, vision samples, safe procedures, and results must be defined for the real equipment; none have been executed yet.

## Issue tracking and closeout

Record each deviation with ID, version, symptom, reproduction condition, impact, owner, correction, retest, and status. Maintain an identifiable approved configuration and backups. Handover includes as-built drawings, software/hardware list, manuals, training, spares, and change log.

**Traceability:** `REQ` → `TC` → evidence → deviation/closure matrix.  
**Pending:** schedule, owners, contractual criteria, versions, samples, instruments, and acceptance format.

## Team responsibilities

| Role | Responsible for | Delivery evidence |
| --- | --- | --- |
| Customer / process owner | URS, product, rate, OK/NOK criteria, interfaces, and acceptance. | Approved requirements and review minutes. |
| Project Manager | Scope, gates, risks, changes, cost, dependencies, and open decisions. | Plan, RAID log, decision register, and minutes. |
| Mechanical engineering | Layout, CAD, loads, access, fabrication, and as-built records. | Released drawings, mechanical BOM, and reviews. |
| Electrical engineering | Cabinet, power, schematics, protection, wiring, and network. | Approved drawings, cable list, and inspection records. |
| PLC/HMI | Architecture, tags, program, alarms, versions, and tests. | Versioned project/backup, tag list, and FAT protocol. |
| Vision integration | Optics/light, job, samples, interface, limits, and result traces. | Agreed capability report, backed-up job, and data map. |
| Safety owner | Assessment, specification, architecture, calculation, and validation. | Safety file signed by competent owner. |
| Quality / commissioning | Samples, inspection, traceability, deviations, and acceptance. | Signed protocols and nonconformance log. |

One person may cover multiple roles on a small project; Safety and customer approvals still require appropriate competence and authority.

## Commissioning activity phases

### 1. Document review and pre-commissioning

- Confirm serial number, software/firmware version, drawings, and “as designed” configuration.
- Review assembly, fasteners, guards, labels, grounding, continuity, protection, pressure, and air quality.
- Identify open tests, permits, calibrations, and measurement equipment.
- Create an initial backup of PLC, HMI, camera, and drive before changing parameters.

### 2. Electrical I/O check

With the area controlled and approved procedures followed, check tag ↔ terminal ↔ device, voltage/polarity, normal state, transition, lost-channel diagnostic, and program response. Operate outputs only when the area is ready and movement is authorized. Record every channel; do not infer status from an HMI LED alone.

### 3. Individual motion and integration

Test drive, feeder, and pusher individually under agreed risk limits; check direction, speed, stroke, pressure, cushioning, and feedback. Then integrate feed → vision → sorting; test real parts, part variation, and bin; confirm each camera response belongs to the correct part ID.

### 4. FAT

1. Agree build, backups, sample, instruments, protocol, and owners.
2. Run nominal and boundary tests against each traced requirement.
3. Check alarms, communication loss, recovery, reset, piece mode, and operational stop.
4. Retest corrected faults and attach evidence identified by version.
5. Record deviations; accept, reject, or defer each with owner and date.

### 5. SAT and handover

Check site utilities and connections; repeat relevant tests after transport/installation; validate plant interfaces, product formats, environmental conditions, and Safety functions on site. Close the punch list before signing acceptance. Deliver as-built documentation, tested backups, spares lists, training, and support contacts.

## Traceable test record

| Field | Example of what to document |
| --- | --- |
| ID / requirement | `TC-104` / `REQ-003`; document version. |
| Equipment / configuration | Serial number, CPU/firmware, program, Cognex recipe/job. |
| Preconditions | Part/revision, mode, speed, pressure, bin, and initial state. |
| Steps | Exact command sequence, induced inputs, and relevant environmental conditions. |
| Expected | Criterion with unit and tolerance approved before testing. |
| Observed | Measured value, instrument/calibration, tag/log, and behavior. |
| Result | PASS/FAIL/BLOCKED; deviation and impact assessment. |
| Approvals | Executor, witness, customer, and date. |

Do not substitute the virtual batch “4 OK / 3 NOK” for production-quality criteria. Vision validation needs representative labeled samples, ground truth, and an agreed false-accept/false-reject rate.
