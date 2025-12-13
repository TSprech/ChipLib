---
sidebar_position: 2
---

# Metadata

These top level fields identify the device and provide context for documentation generators.

| Field          |  Required   | Type           | Description                                                                | Example                      |
|:---------------|:-----------:|:---------------|:---------------------------------------------------------------------------|:-----------------------------|
| `chip`         |   **Yes**   | `String`       | The canonical part number or model name. Used for class naming.            | `TMP1075N`                   |
| `manufacturer` |   **Yes**   | `String`       | The name of the silicon vendor.                                            | `Texas Instruments`          |
| `description`  | Recommended | `String`       | A brief summary of the device's function.                                  | `Digital Temperature Sensor` |
| `interface`    |   **Yes**   | `List[String]` | Supported communication protocols.                                         | `[I2C, SMBus]`               |
| `revision`     |     No      | `String`       | If there are multiple silicon revisions that have different register maps. | `A`                          |

## Chip Notes

The chip name should not include the footprint portion of the device's part number. For example:

**TMP1075DR** - SOIC 8 package

**TMP1075DSGR** - WSON 9 package

Would both fall under the TMP1075.yaml file as there is no register difference. However,

**TMP1075NDRLR** - SOT-563 package

Would get its own TMP1075N.yaml as it has a slightly different register map than the TMP1075 no N. The register map
difference is what requires the different file, not the packaging difference.

:::note Package Suffixes

The package portion of part numbers should be left off, such as both the TMP1075**DR** and TMP1075**DSGR** parts
drop their suffix to be combined into just TMP1075.yaml.

:::

## Interface Notes

The interface can be a variety of standard interface options such as:

* `I2C`
* `SPI`
* `UART`
* `One Wire`
* `SMBus`
* `Quad SPI`
* etc.

The interface name should be the widely used, condensed (`I2C` instead of `Inter-Integrated Circuit`) name for the bus.
If a device has multiple communication protocols, all should be listed.

## Revision Notes

The `revision` field should **not** be included unless silicon revisions affect the register map for simplicity.
