---
sidebar_position: 5
---

# Registers

The `registers` list defines the memory map.

### Register Object Structure

| Field     | Required | Type             | Description                                                |
|:----------|:--------:|:-----------------|:-----------------------------------------------------------|
| `address` | **Yes**  | `Integer`        | The offset address of the register.                        |
| `symbol`  | **Yes**  | `String`         | The programmatic name (e.g., `CTRL_REG`).                  |
| `name`    |    No    | `String`         | The full human-readable name (e.g., `Control Register 1`). |
| `reset`   | **Yes**  | `Integer`        | The value of the register after a power-on reset (POR).    |
| `fields`  | **Yes**  | `List[FieldObj]` | A list of bit-fields within this register.                 |

**Example:**

```yaml
registers:
  - address: 0x01
    symbol: CFGR
    name: Configuration Register
    reset: 0x0000
    fields: [...]
```

