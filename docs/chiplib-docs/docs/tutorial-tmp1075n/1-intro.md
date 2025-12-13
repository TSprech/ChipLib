---
sidebar_position: 1
title: "1. Introduction: The TMP1075N"
description: "Overview of the example project"
---

In this tutorial, we will walk through the creation of a complete **ChipLib** specification for the **Texas Instruments
TMP1075N** Digital Temperature Sensor.

The TMP1075N is a simple device with a good mix of enums, access types, reset values, and bit masks to give a short, but
rich, tutorial.

By the end of this guide, you will understand how to translate a PDF datasheet into a clean, machine-readable YAML file
that generates your driver code.

## Device Overview

The **TMP1075N** is a digital temperature sensor with an I2C interface. It is often used as a low-power, high-accuracy
replacement for the industry-standard LM75.

:::info Datasheet Reference
Throughout this tutorial, we will reference the official datasheet:

* **Part Number:** TMP1075N
* **Document:** [SBOS854F](https://www.ti.com/lit/ds/symlink/tmp1075.pdf)

:::

### Key Specs to Model

Before writing YAML, we identify the key characteristics we need to capture:

* **Interface:** I2C and SMBus compatible.
* **Resolution:** 12-bit data resolution.
* **Register Width:** 16-bit (all registers are 2 bytes).
* **Endianness:** Big Endian (MSB first).

In the next step, we will start our YAML file by defining these global properties.