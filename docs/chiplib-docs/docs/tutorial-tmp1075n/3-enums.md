---
sidebar_position: 3
title: "3. Defining Enums"
description: "Creating reusable named states"
---

Digital sensors often use specific bit patterns to represent states (e.g., `0b1` = "Shutdown Mode"). Instead of using "
magic numbers" in your code, ChipLib allows you to define **Global Enums**.

These enums are defined once and can be linked to any register field.

## Creating the 'Shutdown' Enum

> **Table 7-8. Configuration Register Field Description**
>
> | BIT | FIELD | RESET | DESCRIPTION                                                                                                                            |
> |:----|:------|:------|:---------------------------------------------------------------------------------------------------------------------------------------|
> | 8   | SD    | 0     | Sets the device in shutdown mode to conserve power<br></br>0: Device is in continuous conversion<br></br>1: Device is in shutdown mode |

Here is how we model that in YAML:

```yaml
enums:
  - symbol: SD
    values:
      - name: Continuous Conversion
        value: 0b0
        description: "Device is in continuous conversion"
      - name: Shutdown
        value: 0b1
        description: "Device is in shutdown mode"
```

### Field Breakdown

| YAML Key      | Datasheet Source                 | Rationale & Notes                              |
|:--------------|:---------------------------------|:-----------------------------------------------|
| `symbol`      | "SD"                             | The short name for the bit(s) in the register. |
| `name`        | "Shutdown"                       | A human understandable name, **Title Case**.   |
| `value`       | "0: ... 1: ..."                  | The value that each enum corresponds to.       |
| `description` | "Sets the device in shutdown..." | A brief summary for documentation.             |

:::note Naming Convention

ChipLib uses **Title Case** for names (e.g., `Continuous Conversion`). This allows the generator to easily convert them
to `PascalCase`, `camelCase`, or `SNAKE_CASE` depending on your output language template.

:::

## Creating the 'Conversion Rate' Enum

Some enums have multi-bit values. An example is the **Consecutive Fault (F)** field which control how many faults are
required to trigger an alert.

```yaml
  - symbol: F
    values:
      - name: Fault 1
        value: 0b00
        description: "1 fault"
      - name: Fault 2
        value: 0b01
        description: "2 faults"
      - name: Fault 4
        value: 0b10
        description: "4 faults"
      - name: Fault 6
        value: 0b11
        description: "6 faults"
```

As shown above, multi-bit follows the same pattern as single bit enums.

:::tip Enum Reuse

Common enums that are used between multiple fields, such as an `Enable` / `Disable` enum, can be defined once and
referenced multiple times. No need to make one for each field!

:::
