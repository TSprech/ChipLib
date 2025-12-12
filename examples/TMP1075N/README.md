# Example: Texas Instruments TMP1075N

[![Manufacturer](https://img.shields.io/badge/Manufacturer-Texas%20Instruments-CC0000)](https://www.ti.com/)
[![Datasheet](https://img.shields.io/badge/Datasheet-SBOS854F-111111)](https://www.ti.com/lit/ds/symlink/tmp1075.pdf)
![Datasheet Revision](https://img.shields.io/badge/Datasheet%20Revision-F-EEEEEE)

This document provides a complete example of a **ChipLib** specification file. It details how
the [TMP1075N temperature sensor datasheet (SBOS854F)](https://www.google.com/search?q=https://www.ti.com/lit/gpn/tmp1075)
is translated into the `TMP1075N.yaml` format.

## 0. Notes Regarding Naming

ChipLib uses Title Case with spaces extensively for names. This is because it is the easiest case that I have found to
convert into any other case that fits your programming style. Please follow this standard to ensure uniform conversion
into libraries.

## 1. Device Overview

The **TMP1075N** is a digital temperature sensor with an I2C interface. It is a low-power, high-accuracy replacement for
the industry-standard LM75.

* **Interface:** I2C, SMBus
* **Resolution:** 12-bit
* **Default Register Width:** 16 bits

## 2. Top-Level Specification (`TMP1075N.yaml`)

The top-level object defines the device itself. This information is gathered from the datasheet's front page and
register map summary.

```yaml
---
chip: TMP1075N
manufacturer: Texas Instruments
description: "Register descriptions for the TMP1075N Temperature Sensor With I2C and Alert"
interface: [ I2C, SMBus ]

defaults:
  register_width: 16
  byte_order: big
  access: [ r, w ]
```

### Top-Level Field Correlation

| YAML Key         | Datasheet Source                 | Rationale & Notes                                                                        |
|:-----------------|:---------------------------------|:-----------------------------------------------------------------------------------------|
| `chip`           | "TMP1075N"                       | The part number being defined in the yaml file.                                          |
| `manufacturer`   | "Texas Instruments"              | The company that makes the chip.                                                         |
| `interface`      | "I2C and SMBus Interface"        | A list of communication protocols.                                                       |
| `description`    | "Temperature Sensor With I2C..." | A brief summary for documentation.                                                       |
| `register_width` | "16-bit read/write register"     | The default width of a register transaction. For the TMP1075N, all registers are 16-bit. |
| `access`         | "R", "W"                         | The default access for most registers. This can be overridden per-field.                 |

The defaults section sets up variables that are consistent, or mostly consistent throughout the file. For example, most
registers are read/write access, so setting access to default to `[ r, w ]` allows that entry to be omitted from any
fields that match that access. To override it, you simply add the `access` entry to the field that requires a different
access specifier and the default will be overridden. Another example is the `register_width`, which is 16 bit for all
registers, so the `defaults:` section is the only place it needs to be defined.

-----

## 3. Global Enum Definitions (`enums`)

The `enums` block defines all named bit-field enumerations. This is critical for generating human-readable
`enum` types and improves code safety. While technically not strictly required, they are extremely useful in making
libraries more usable.

### Example: `SD` (Shutdown Mode) Enum

This enum defines the `SD` bit (Bit 8) in the Configuration Register.

**Datasheet Reference (Page 22):**

> **Table 7-8. Configuration Register Field Description**
>
> | BIT | FIELD | RESET | DESCRIPTION                                                                                                                   |
> |:----|:------|:------|:------------------------------------------------------------------------------------------------------------------------------|
> | 8   | SD    | 0     | Sets the device in shutdown mode to conserve power<br>0: Device is in continuous conversion<br>1: Device is in shutdown mode  |

**YAML Definition:**

```yaml
enums:
  - symbol: SD
    values:
      - name: Shutdown
        value: 0b0
        description: "Device is in continuous conversion"
      - name: Shutdown
        value: 0b1
        description: "Device is in shutdown mode"
```

| YAML Key      | Datasheet Source                 | Rationale & Notes                              |
|:--------------|:---------------------------------|:-----------------------------------------------|
| `symbol`      | "SD"                             | The short name for the bit(s) in the register. |
| `name`        | "Shutdown"                       | A human understandable name, **Title Case**.   |
| `value`       | "0: ... 1: ..."                  | The value that each enum corresponds to.       |
| `description` | "Temperature Sensor With I2C..." | A brief summary for documentation.             |

-----

## 4. Register Definitions (`registers`)

This is the main list of all registers on the device, taken directly from the **Register Map** (Table 7-5 on page 21 of
the datasheet).

### Example 1: `TEMP` (Read-Only Register)

**Datasheet Reference (Page 21):**

> **Table 7-5. TMP1075 Register Map**
>
> | ADDRESS | TYPE | RESET | ACRONYM | REGISTER NAME               |
> |:--------|:-----|:------|:--------|-----------------------------|
> | 00h     | R    | 0000h | TEMP    | Temperature result register |

> **Table 7-7. Temperature Register Field Description**
>
> | BIT  | FIELD   | TYPE | RESET | DESCRIPTION                                                                            |
> |:-----|:--------|:-----|:------|:---------------------------------------------------------------------------------------|
> | 15:4 | T[11:0] | R    | 000h  | 12-bit, read-only register that stores the most recent temperature conversion results. |

**YAML Definition:**

```yaml
registers:
  - address: 0x00
    name: Temperature
    symbol: TEMP
    reset: 0x0000
    fields:
      - name: Temperature
        symbol: T
        bits: [ 15, 4 ]
        access: [ r ]
        description: "12-bit, read-only register that stores the most recent temperature conversion results"
        format:
          representation: tc
          unit: "Celsius"
```

#### Key Concepts from this Example:

* `address`, `name`, `symbol`, and `reset` are copied directly from the register map table.
* `fields`: Contains a list of all bit-fields within this register.
* `bits: [ 15, 4 ]`: The `[high, low]` bit range for this field.
* `access: [ r ]`: This field is **Read-Only**, so we override the register's default `[r, w]` access.
* `format:`: The `format` section specifies the `representation`, which is two's-complement or `tc`. It also specifies
  the `unit` which is a text representation of the units that the field corresponds to.

-----

### Example 2: `CFGR` (R/W Register with Enums)

This is a complex register demonstrating field overrides, enums, and default value mapping.

**Datasheet Reference (Page 22):**

> **Table 7-5. TMP1075 Register Map**
>
> | ADDRESS | TYPE | RESET | ACRONYM | REGISTER NAME          |
> |:--------|:-----|:------|:--------|------------------------|
> | 01h     | R/W  | 60A0h | CFGR    | Configuration register |

> **Table 7-8. Configuration Register Field Description**
>
> | BIT   | FIELD  | TYPE         | RESET | DESCRIPTION                                                          |
> |:------|:-------|:-------------|:------|:---------------------------------------------------------------------|
> | 14:13 | R[1:0] | R (TMP1075N) | 11    | Conversion rate setting when device is in continuous conversion mode |
> | 10    | POL    | R/W          | 0     | Polarity of the output pin                                           |

**YAML Definition:**

```yaml
enums:
  # ... other enums ...
  - symbol: R
    values:
      - name: Conversion Rate 27 5
        value: 0b00
        description: "27.5 ms conversion rate"
      - name: Conversion Rate 55
        value: 0b01
        description: "55 ms conversion rate"
      - name: Conversion Rate 110
        value: 0b10
        description: "110 ms conversion rate"
      - name: Conversion Rate 250
        value: 0b11
        description: "250 ms conversion rate"

  - symbol: POL
    values:
      - name: Low
        value: 0b0
        description: "Active low ALERT pin"
      - name: High
        value: 0b1
        description: "Active high ALERT pin"

registers:
  # ... other registers ...
  - address: 0x01
    name: Configuration
    symbol: CFGR
    reset: 0x60A0
    fields:
      # ... other fields ...
      - name: Conversion Rate
        symbol: R
        bits: [ 14, 13 ]
        access: [ r ] # This field is Read-Only on TMP1075N
        description: "Conversion rate setting when device is in continuous conversion mode"
        enum: R # Links to the global 'R' enum
        reset: Conversion Rate 250 # Maps to the 'name' in the 'R' enum

      - name: Alert Polarity
        symbol: POL
        bits: [ 10, 10 ]
        # access: is set to the default [ r, w ]
        description: "Polarity of the output pin"
        enum: POL # Links to the global 'POL' enum
        reset: Low # Maps to the 'name' in the 'POL' enum
      # ... other fields ...
```

#### Key Concepts from this Example:

* **`enum: R`**: This field explicitly links this field to the global `R` enum defined in the `enums:` block. The code
  generator will use this to create type-safe functions (e.g., `Set_R(R::Conversion_Rate_250)`).
* **`access: [ r ]`**: The `CFGR` register is R/W, but the `R` (Conversion Rate) field is **Read-Only** on the TMP1075N
  variant. This `access` key overrides the parent register's access setting.
* **`reset: Conversion Rate 250`**: The datasheet states the reset for `R[1:0]` is `11`, which corresponds to the "250
  ms conversion rate" enum. By using the `name` from the enum, we make the reset value self-documenting. The generator
  will resolve this string to `0b11` or the programming language equivalent.
* **`enums` and `registers`**: The enums and registers are in two separate sections, and are linked together using the
  enum name as mentioned above. All names are **Title Case**.
* **`reset: 0x60A0`**: For each field, `reset: <Name>` is defined to set the *field* specific reset value. This is
  useful for generators that need to
  initialize and reset fields individually, while the register-level `reset: 0x60A0` documents the full reset value from
  the
  datasheet for register level operations.

-----
