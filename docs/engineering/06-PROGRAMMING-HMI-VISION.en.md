# 06 · Programming, HMI, and vision interface

**Status:** teaching guide v0.1 · no executable project  
**Objective:** explain how to turn the PLC architecture into verifiable logic and a clear operator/diagnostic interface.

## Language choice

- **LAD/KOP:** permissive and discrete-condition networks that maintenance staff can review online.
- **SCL:** structure transformations, recipe/data handling, and calculations that read better as structured text.
- A sequence can combine both languages. Team standards and maintainability matter more than rewriting everything in one style.

Programming should start from approved interfaces and block-level tests. Each sequence transition needs an entry condition, action, exit condition, maximum time where applicable, and fault response. Do not use accelerated simulator timings as machine values.

## Camera interface

The following table is a conceptual exchange, not an implemented handshake. Order, edges, retention, timeout, and recovery must be agreed with the selected camera model.

| Stage | PLC | Camera | Expected evidence |
| --- | --- | --- | --- |
| Preparation | Validates part present, recipe, and process permission. | Reports ready and recipe loaded. | Values coherent for the same part. |
| Trigger | Sends `Trigger` and a cycle ID if the protocol supports it. | Accepts trigger and starts capture. | Observable acknowledgement or transition. |
| Result | Waits for capture complete and a valid result. | Returns OK/NOK, validity, and agreed diagnostics. | Result linked to the correct part ID. |
| Close | Stores/consumes the result once and releases the exchange. | Returns to `Ready` according to its interface. | No stale or duplicated result. |

The simulation presents `DO_VisionTrigger`, `VisionReady`, `InspectionDone`, `InspectionValid`, and `VisionOK`; the result comes from the internal batch. No electronic camera communication exists.

## HMI and Watch

The machine HMI should prioritize mode, state, START, FIN DE PIEZA, permitted RESET, alarm, and production. Confirmations, user permissions, navigation, and alarm detail belong in the specification. Simulator pause freezes the graphics clock; a real machine requires a specifically defined operational stop and risk analysis.

PLC Watch is an observation/commissioning tool, not the production HMI. Keep the prototype's existing names and types as a reference: BOOL, INT, DINT, REAL, and TIME. Before exporting a real table, validate address, unit, range, quality, and retention.

## Software verification

Plan cases for each block, transition, reject path, lost handshake, missing signal, timeout, restart, and recovery. Record preconditions, stimulus, expected result, observed value, and evidence. Faults must come from a verifiable logical condition; injected faults do not prove an alarm.

**Output artifact:** versioned PLC source, HMI/vision tag list, and approved test matrix.  
**Traceability:** `REQ-002`…`REQ-008`; proposed blocks in document 05.
