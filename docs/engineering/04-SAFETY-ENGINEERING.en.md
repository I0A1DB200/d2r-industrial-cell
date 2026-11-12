# 04 · Safety Engineering

**Status:** working framework · no approved risk assessment  
**Objective:** define the work required to specify, implement, and validate safety functions for a real machine.

> The simulator's `SafetyReady` signal is a constant logical indication. It is not an input from a safety relay or safety PLC, it does not demonstrate a safety function, and it must not be used to size or validate a system.

## Design principle

Safety starts with intended use, machine limits, and hazard identification—not by copying a simulator bit. A competent person must assess risk using the regulations and standards applicable to the country, machine, and project date. The need for PLr/SIL, architecture, components, and tests follows from that assessment.

## Required work

1. Define operating modes, access, cleaning/jam-clearing tasks, maintenance, and foreseeable fault conditions.
2. Identify mechanical, electrical, pneumatic, and process hazards; estimate and reduce risk using the applicable method.
3. Specify each safety function: initiating event, zone, required response, stopping time/distance, reset, and diagnostics.
4. Select guards, interlocks, emergency stops, and control elements only after establishing requirements.
5. Separate standard control from safety functions and define their interfaces.
6. Verify the design and validate each function with a traceable protocol; record measurements, faults, changes, and responsible approval.

ISO 12100, ISO 13849-1, IEC 62061, and applicable type-C standards are references for review with the Safety team. Citing a standard does not establish compliance or certify this simulator.

## Topics to assess for this case

Access to the magazine and pinch zones; access to the belt, rollers, pusher, and ramps; jam-clearing intervention; residual energy and air loss; camera/lighting protection; and recovery after a stop. These are assessment topics, not a complete hazard list or a selected solution.

| Deliverable | Required evidence | Status |
| --- | --- | --- |
| Risk assessment | Limits, hazards, estimation, measures, and residual risk. | Pending |
| Function specification | Requirements, zones, safe state, reset, and measured times. | Pending |
| Safety design | Architecture, components, calculations, and electrical documentation. | Pending |
| Validation | Protocol, measured results, deviations, and approval. | Pending |

**Traceability:** `REQ-009` and operating decisions in documents 01–03.  
**Teaching limit:** the HTML retains its existing conceptual model; this document does not modify or extend its Safety behavior.
