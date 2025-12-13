---
sidebar_position: 4
---

# Enums

Enumerations (`enums`) define named states for bit-fields. They are defined globally to allow reuse across multiple
registers.

### Enum Object Structure

| Field    | Required | Type             | Description                                                                 |
|:---------|:--------:|:-----------------|:----------------------------------------------------------------------------|
| `symbol` | **Yes**  | `String`         | The programmatic name for the Enum type. Must be PascalCase or UPPER\_CASE. |
| `values` | **Yes**  | `List[ValueObj]` | A list of named values belonging to this enum.                              |

### Enum Value Object

| Field         |  Required   | Type      | Description                                                                                     |
|:--------------|:-----------:|:----------|:------------------------------------------------------------------------------------------------|
| `name`        |   **Yes**   | `String`  | The human-readable name of the state. Used to generate the enum member name.                    |
| `value`       |   **Yes**   | `Integer` | The raw integer value of the state. Supports `0x` for hexadecimal, `0b` for binary, or decimal. |
| `description` | Recommended | `String`  | Documentation for this specific state.                                                          |

**Example:**

```yaml
enums:
  - symbol: Gain
    values:
      - name: Gain 1x
        value: 0b00
        description: "Standard gain setting."
      - name: Gain 8x
        value: 0b11
        description: "High sensitivity mode."
```
