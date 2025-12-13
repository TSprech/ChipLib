---
sidebar_position: 4
title: "4. Defining Registers"
description: "Mapping the memory and fields"
---

The `registers` block is the core of your specification. It maps the memory addresses to the fields we defined earlier.

## Example 1: A Read-Only Data Register (TEMP)

The Temperature register (Address `0x00`) contains the sensor data.

**Datasheet Page 21:**

> **Table 7-5. TMP1075 Register Map**
>
> | ADDRESS | TYPE | RESET | ACRONYM | REGISTER NAME               |
> |:--------|:-----|:------|:--------|-----------------------------|
> | 00h     | R    | 0000h | TEMP    | Temperature result register |

> > **Table 7-7. Temperature Register Field Description**
>
> | BIT  | FIELD   | TYPE | RESET | DESCRIPTION                                                                            |
> |:-----|:--------|:-----|:------|:---------------------------------------------------------------------------------------|
> | 15:4 | T[11:0] | R    | 000h  | 12-bit, read-only register that stores the most recent temperature conversion results. |

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
        description: "12-bit, read-only register..."
        format:
          representation: tc
          unit: "Celsius"
```

:::warning Overriding Defaults

Notice we included `access: [ r ]`. This overrides the global default of `[ r, w ]` because this specific register is
Read-Only.

:::

#### Understanding `format`

* **`representation: tc`**: Tells the generator this is a **Two's Complement** signed integer.
* **`unit: "Celsius"`**: Purely for documentation, letting the user know what the value represents.

### Key Concepts from this Example:

* `address`, `name`, `symbol`, and `reset` are copied directly from the register map table.
* `fields`: Contains a list of all bit-fields within this register.
* `bits: [ 15, 4 ]`: The `[high, low]` bit range for this field.
* `access: [ r ]`: This field is **Read-Only**, so we override the register's default `[r, w]` access.
* `format:`: The `format` section specifies the `representation`, which is two's-complement or `tc`. It also specifies
  the `unit` which is a text representation of the units that the field corresponds to.

---

## Example 2: A Complex Configuration Register (CFGR)

The Configuration register (Address `0x01`) mixes basic bits with Enums.

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

```yaml
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

    # ... other fields ...
    
    - name: Alert Polarity
      symbol: POL
      bits: [ 10, 10 ]
      # access: is set to the default [ r, w ]
      description: "Polarity of the output pin"
      enum: POL # Links to the global 'POL' enum
      reset: Low # Maps to the 'name' in the 'POL' enum
    # ... other fields ...
```

### Linking Enums

* **`enum: R`**: This links the field to the global `R` enum we defined in Step 3. The generated code will force you to
  use a valid `R` enum value when writing to this field.
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
  the datasheet for register level operations.

---

## Summary

You have now defined:

1. **Metadata:** The chip identity.
2. **Enums:** Reusable states like `Shutdown` and `Conversion Rate`.
3. **Registers:** The memory map linking addresses to bit-fields and enums.

This YAML file is now ready to be fed into **ChipLib** to generate your C++, Python, or any other library!
