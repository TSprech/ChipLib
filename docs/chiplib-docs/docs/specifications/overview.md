---
sidebar_position: 1
---

# Overview

A ChipLib YAML file represents a single integrated circuit (IC) or IP block. The file is structured into four primary sections:

1.  **Metadata:** Top-level information identifying the chip.
2.  **Defaults:** Global settings applied to registers unless overridden.
3.  **Enums:** Shared enumeration definitions for bit-fields.
4.  **Registers:** The complete memory map definition.

### Example Skeleton

```yaml
chip: <String>
manufacturer: <String>
description: <String>
interface: <List[String]>

defaults:
  register_width: <Integer>
  byte_order: <"big" | "little">
  access: <List[AccessCode]>

enums:
  - symbol: <String>
    values: [...]

registers:
  - address: <Integer>
    symbol: <String>
    fields: [...]
````
