# 05 · PLC architecture: OB, FC, FB, DB, UDT, and tags

**Status:** teaching proposal v0.1 · TIA Portal to be confirmed  
**Objective:** organize responsibilities and data ownership so the program is readable, testable, and extensible.

## Data layers

1. **Hardware I/O:** process image and channel diagnostics tied to the approved physical configuration.
2. **Raw data:** sensor readings, drive/valve states, and camera data, preserving source quality.
3. **Commands:** operator and external-interface requests, validated before entering the sequence.
4. **States and alarms:** PLC-owned, with causes, active/acknowledged state, and defined recovery.
5. **HMI/vision interface:** stable DB with agreed types, units, permissions, and version.

The PLC should own cycle state and production counters. The camera owns a capture result until the PLC validates it and associates it with a part. HMI and Watch observe/write only authorized fields. This architecture is a proposal; no PLC project exists for this cell.

## Proposed block allocation

| Proposed block | Responsibility | Associated data |
| --- | --- | --- |
| `OB1_Main` | Call equipment blocks and coordinate the cyclic sequence. | No long station logic. |
| `FB10_CellSequence` | Modes, transitions, commands, and global status. | `DB_CellSequence` as instance DB. |
| `FB20_Feeder` | Feeding and part confirmation. | `DB_Feeder` instance. |
| `FB30_Conveyor` | Transport command and diagnostics. | `DB_Conveyor` instance. |
| `FB40_VisionInterface` | Camera trigger, handshake, result, and diagnostics. | `DB_VisionInterface` instance and agreed exchange DB. |
| `FB50_Sorter` | Classification, pusher, and outputs. | `DB_Sorter` instance. |
| `FC10_ValidateCommands` | Stateless validations where useful. | Explicit input/output parameters. |
| `DB_HMI_Interface` | Stable interface for commands, status, counters, and visible alarms. | Shared interface types. |

These names are teaching IDs, not blocks that already exist. In TIA Portal, an FB retains static data in its instance DB; an FC has no instance DB of its own. A global DB contains shared data. A UDT defines a reusable structure; it does not execute logic.

## UDTs and traceability

Review `UDT_CellCommand`, `UDT_CellStatus`, `UDT_AlarmEntry`, and `UDT_VisionExchange` as candidates. Separate commands, status, configuration, raw data, and alarms when they have different consumers. Every field needs an owner, type, unit, range, update cycle, and validity rule. The camera's internal job/database and the PLC exchange DB are separate objects; confirm whether the Cognex model needs a recipe, job number, or result storage.

Safety must be designed and validated in its appropriate architecture; it is not replaced by a standard FB or the simulator's `SafetyReady` field.

**Verification:** review calls, instance DBs, interfaces, HMI access, and absence of duplicate writes to the same data.  
**Pending:** CPU/firmware, naming standards, communication requirements, number of instances, and software-team boundaries.
