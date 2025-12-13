---
title: Markdown page example
---

# ChipLib YAML Specification

**Version:** 1.0.0
**Status:** Draft

This document defines the schema and structural requirements for ChipLib YAML specification files. These files serve as the "single source of truth" for generating hardware abstraction layers (HALs) and driver libraries.

---

## 1. File Structure Overview

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

-----

## 2\. Top-Level Metadata

These fields identify the device and provide context for documentation generators.

| Field | Required | Type | Description | Example |
| :--- | :---: | :--- | :--- | :--- |
| `chip` | **Yes** | `String` | The canonical part number or model name. Used for class naming. | `TMP1075N` |
| `manufacturer` | No | `String` | The name of the silicon vendor. | `Texas Instruments` |
| `description` | No | `String` | A brief summary of the device's function. | `Digital Temperature Sensor` |
| `interface` | No | `List[String]` | Supported communication protocols. | `[I2C, SMBus]` |

-----

## 3\. Defaults Section

The `defaults` block defines properties that apply to *all* registers unless explicitly overridden at the register or field level. This reduces repetition.

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `register_width` | **Yes** | `Integer` | The standard width of a register in bits. |
| `byte_order` | **Yes** | `Enum` | `big` (MSB first) or `little` (LSB first). |
| `access` | No | `List[AccessCode]` | Default read/write permissions (e.g., `[r, w]`). |

**Example:**

```yaml
defaults:
  register_width: 16
  byte_order: big
  access: [r, w]
```

-----

## 4\. Enums Section

Enumerations (`enums`) define named states for bit-fields. They are defined globally to allow reuse across multiple registers.

### Enum Object Structure

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `symbol` | **Yes** | `String` | The programmatic name for the Enum type. Must be PascalCase or UPPER\_CASE. |
| `values` | **Yes** | `List[ValueObj]` | A list of named values belonging to this enum. |

### Enum Value Object

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `name` | **Yes** | `String` | The human-readable name of the state. Used to generate the enum member name. |
| `value` | **Yes** | `Integer` | The raw integer value of the state. Supports `0x`, `0b`, or decimal. |
| `description` | No | `String` | Documentation for this specific state. |

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

-----

## 5\. Registers Section

The `registers` list defines the memory map.

### Register Object Structure

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `address` | **Yes** | `Integer` | The offset address of the register. |
| `symbol` | **Yes** | `String` | The programmatic name (e.g., `CTRL_REG`). |
| `name` | No | `String` | The full human-readable name (e.g., `Control Register 1`). |
| `reset` | **Yes** | `Integer` | The value of the register after a power-on reset (POR). |
| `fields` | **Yes** | `List[FieldObj]` | A list of bit-fields within this register. |

**Example:**

```yaml
registers:
  - address: 0x01
    symbol: CFGR
    name: Configuration Register
    reset: 0x0000
    fields: [...]
```

-----

## 6\. Fields Section

Fields define the bit-packing layout within a register.

### Field Object Structure

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `symbol` | **Yes** | `String` | The programmatic name for the field (e.g., `EN`). |
| `bits` | **Yes** | `List[Integer]` | The bit range as `[high, low]` (e.g., `[7, 7]` or `[15, 12]`). |
| `name` | No | `String` | Full name of the field. |
| `description` | No | `String` | Documentation for the field. |
| `access` | No | `List[AccessCode]` | Overrides the default register access. |
| `enum` | No | `String` | The `symbol` of a global Enum to link to this field. |
| `reset` | No | `String` | `Int` | The reset value for *this specific field*. Can be a number or an Enum Value `name`. |
| `format` | No | `FormatObj` | Defines data representation (signed/unsigned) and units. |

### Access Codes

| Code | Meaning |
| :--- | :--- |
| `r` | Readable. |
| `w` | Writable. |
| `woset` | Write-One-to-Set (Self-clearing). |
| `w1c` | Write-1-to-Clear. |
| `rc` | Read-to-Clear. |

### Format Object Structure

The `format` block is used to describe the **raw data representation** and provide **documentation units**. It does *not* generate scaling logic.

| Field | Required | Type | Description |
| :--- | :---: | :--- | :--- |
| `representation` | **Yes** | `String` | `unsigned`, `twos_complement`, `sign_magnitude`, or `bcd`. |
| `unit` | No | `String` | The real-world unit of measurement (e.g., `"Celsius"`, `"Volts"`). |
| `lsb_weight` | No | `Float` | The value of 1 LSB in the specified units. Defaults to `1`. |

**Example (Field with Format):**

```yaml
- symbol: TEMP
  bits: [15, 4]
  access: [r]
  description: "Temperature result."
  format:
    representation: twos_complement
    unit: "Celsius"
    lsb_weight: 0.0625
```

-----

## 7\. Best Practices

1.  **Naming:** Use **Title Case** for `name` fields (e.g., "Conversion Rate"). Use **UPPER\_CASE** for `symbol` fields representing registers or enums.
2.  **Binary Literals:** Use binary (`0b...`) for enum values and bitmasks to make the specific bit settings obvious.
3.  **Documentation:** Use the `description` fields liberally. This text is propagated to the generated code (e.g., Doxygen comments) and is vital for the end-user.
4.  **Resets:** Always verify that the `reset` value of a register matches the sum of its fields' defaults in the datasheet.
