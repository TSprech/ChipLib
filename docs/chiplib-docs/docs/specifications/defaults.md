---
sidebar_position: 3
---

# Defaults

The `defaults` block defines properties that apply to *all* registers unless explicitly overridden at the register or
field level. This reduces repetition.

| Field            |  Required   | Type               | Description                                      |
|:-----------------|:-----------:|:-------------------|:-------------------------------------------------|
| `register_width` |   **Yes**   | `Integer`          | The standard width of a register in bits.        |
| `byte_order`     |   **Yes**   | `Enum`             | `big` (MSB first) or `little` (LSB first).       |
| `access`         | Recommended | `List[AccessCode]` | Default read/write permissions (e.g., `[r, w]`). |

**Example:**

```yaml
defaults:
  register_width: 16
  byte_order: big
  access: [ r, w ]
```

:::tip Other Fields

Any other field that would typically go in the `fields:` section can be included. For example, if a device's registers
all reset to the same value, the `reset:` field could be included in the `defaults:`.

:::
