# 07 · Project management and commissioning

**Status:** teaching work plan v0.1 · no physical tests executed  
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
