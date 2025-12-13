---
sidebar_position: 2
title: "2. Top-Level Definitions"
description: "Defining the chip identity and defaults"
---

The first section of any ChipLib file establishes the identity of the chip and sets default behaviors for the code
generator. This saves you from repeating the same settings for every single register.

## The Metadata Block

Create a new file named `TMP1075N.yaml` and add the following metadata headers. These are used by documentation
generators and for naming the output C++ class.

```yaml title="TMP1075N.yaml"
chip: TMP1075N
manufacturer: Texas Instruments
description: "Register descriptions for the TMP1075N Temperature Sensor With I2C and Alert"
interface: [ I2C, SMBus ]
```

| YAML Key       | Datasheet Source                 | Rationale & Notes                               |
|:---------------|:---------------------------------|:------------------------------------------------|
| `chip`         | "TMP1075N"                       | The part number being defined in the yaml file. |
| `manufacturer` | "Texas Instruments"              | The company that makes the chip.                |
| `interface`    | "I2C and SMBus Interface"        | A list of communication protocols.              |
| `description`  | "Temperature Sensor With I2C..." | A brief summary for documentation.              |

## The Defaults Block

The `defaults` section is a powerful feature that reduces clutter. Since every register on
this chip is 16-bit and almost all are Read/Write, we set those as the defaults here.

```yaml
defaults:
  register_width: 16
  byte_order: big
  access: [ r, w ]
```

:::tip Why use defaults?

Without this block, you would have to add `register_width: 16` to **every single register definition** below. If a
specific register differs (e.g., an 8-bit ID register), you can override these defaults at the register level.

:::

### Field Breakdown

| Field            | Description                     | Rationale for TMP1075N                                                |
|------------------|---------------------------------|-----------------------------------------------------------------------|
| `register_width` | Default bit-width of registers. | The datasheet defines all registers as 16-bit.                        |
| `byte_order`     | `big` or `little`.              | I2C devices typically transmit the MSB (Most Significant Byte) first. |
| `access`         | Default permissions.            | Most configuration registers are Read/Write (`[ r, w ]`).             |
