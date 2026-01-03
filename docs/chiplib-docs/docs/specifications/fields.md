---
sidebar_position: 6
---

# Fields

Fields define the bit-packing layout within a register.

## Field Object Structure

| Field         |  Required   | Type               | Description                                                                         |
|:--------------|:-----------:|:-------------------|:------------------------------------------------------------------------------------|
| `symbol`      |   **Yes**   | `String`           | The programmatic name for the field (e.g., `EN`).                                   |
| `bits`        |   **Yes**   | `List[Integer]`    | The bit range as `[high, low]` (e.g., `[7, 7]` or `[15, 12]`).                      |
| `name`        | Recommended | `String`           | Full name of the field.                                                             |
| `description` | Recommended | `String`           | Documentation for the field.                                                        |
| `access`      |     No      | `List[AccessCode]` | Overrides the default register access.                                              |
| `enum`        |     No      | `String`           | The `symbol` of a global Enum to link to this field.                                |
| `reset`       | Recommended | `String` or `Int`  | The reset value for *this specific field*. Can be a number or an Enum Value `name`. |
| `format`      |     No      | `FormatObj`        | Defines data representation (signed/unsigned) and units.                            |

### Access Codes

| Code    | Meaning                            | Explanation                                                                        |
|:--------|:-----------------------------------|------------------------------------------------------------------------------------|
| `na`    | No access                          | Generally should not be used, registers that have no access should not be included |
| `r`     | Readable                           |                                                                                    |
| `rclr`  | Read to Clear                      |                                                                                    |
| `rset`  | Read to Set                        |                                                                                    |
| `w`     | Writable                           |                                                                                    |
| `woset` | Write 1 to Set (Self resetting)    | Denotes self resetting as typically writing a 1 performs a set                     |
| `woclr` | Write 1 to Clear                   |                                                                                    |
| `wotog` | Write 1 to Toggle                  |                                                                                    |
| `wzset` | Write 0 to Set                     |                                                                                    |
| `wzclr` | Write 0 to Clear  (Self resetting) | Denotes self resetting as typically writing a 0 performs a clear                   |
| `wztog` | Write 0 to Toggle                  |                                                                                    |
| `wclr`  | Write to Clear                     | Denotes writing any value causes a clear                                           |
| `wset`  | Write to Set                       | Denotes writing any value causes a set                                             |

### Format Object Structure

The `format` block is used to describe the **raw data representation** and provide **documentation units**. It does
*not* generate scaling logic.

| Field            | Required | Type     | Description                                                                                                                                                                                                                                                                                                 |
|:-----------------|:--------:|:---------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `representation` | **Yes**  | `String` | Can be one of the following options:<br></br>1. `us`: Unsigned e.g. uint8_t or uint32_t<br></br>2. `tc`: Two's Compliment e.g. int8_t or int32_t, sign extended<br></br>3. `sm`: Sign Magnitude e.g. MSB is the sign bit<br></br>4. `bd`: Binary Coded Decimal e.g. Each 4 bits represent a digit from 0-9. |
| `unit`           |    No    | `String` | The real-world unit of measurement (e.g., `"Celsius"`, `"Volts"`).                                                                                                                                                                                                                                          |
| `scale`          |    No    | `Float`  | The magnitude scalar applied to the units. For example, `0.001` would be used in conjunction with `unit: "Celsius"` to denote **millicelsius**.                                                                                                                                                             |

**Example (Field with Format):**

```yaml
- symbol: TEMP
  bits: [ 15, 4 ]
  access: [ r ]
  description: "Temperature result."
  format:
    representation: tc
    unit: "Celsius"
    scale: 1.0
```