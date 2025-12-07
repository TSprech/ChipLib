# ChipLib: The Chip Library Generator

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=Python&logoColor=white&style=flat)
![Python](https://img.shields.io/badge/Jinja-3-FF5545?logo=Jinja&logoColor=white&style=flat)
[![Test Status](https://img.shields.io/github/actions/workflow/status/TSprech/ChipLib/python-ci.yml?label=Test&logo=githubactions&logoColor=white)](https://github.com/TSprech/ChipLib/actions)
[![Coverage](https://img.shields.io/coveralls/github/TSprech/ChipLib?label=Coverage&logo=coveralls&logoColor=white)](https://coveralls.io/github/TSprech/ChipLib)
![GitHub](https://img.shields.io/github/license/TSprech/Pull-Based-Pipeline?color=%23D22128&logo=apache)

**ChipLib** is a development tool that converts human-readable YAML register specifications into language-agnostic,
production-ready embedded driver libraries.

## 1. The Problem ChipLib Solves

In embedded systems development, the journey from a 100-page PDF datasheet to a functional, bug-free driver is laborious
and repetitive:

* **Manual & Slow:** Developers manually translate register addresses, bitmasks, and field positions into code, a
  process that can take days.
* **Error-Prone:** A single mistake in a bitmask (e..g, `0xFF` vs `0xFE`) can lead to silent, hard-to-debug hardware
  failures.
* **Language-Specific:** A `C++` driver is useless to the `Python` test team. A `Rust` implementation can't be reused in
  a legacy `C` project.
* **Outdated Libraries:** Updating working code from one programming language version to another or changing library
  standards can be risky with manual refactoring, keeping libraries in the past.

Of course, you could use a library you find online, but there's no easy way to verify it is correct, nor does not match
your particular coding / HAL format.

**ChipLib** fixes this by abstracting the hardware definition into a *single source of truth* (a YAML file). It uses
this specification along with your own template to generate drivers for any target language, ensuring correctness and
saving hundreds of development hours. On top of that, you can update your entire collection of chip interface libraries
to new coding standards in less time than it would take to refactor a single library.

*Note: ChipLib is not designed to be a tool which does 100% of the work required to create an embedded library. It is
designed to be a flexible tool that generates ~95% of the code required, particularly the tedious and error-prone
portions, and then the remaining 5% filled in by the end developer. As such, it leaves implementing the library template
file and hardware interaction implementation up to the developer. However, creating and sharing templates for common
languages like Arduino C++, Circuit/MicroPython, and others is encouraged!*

## 2. Project History: From SystemRDL to YAML

This project began by using **SystemRDL**, a language purpose-built for defining ASIC/FPGA register maps. I created more
than a dozen RDL-based libraries over the course of several months with fantastic success.

However, several challenges arose as I continued to use RDL more. It became obvious that as good of a tool as RDL is, it
has its own challenges when applying it to embedded sensor libraries:

1. **Addressing Conflicts:** SystemRDL does not allow *address overlap* such as a 16 bit register at addresses 0x00 and
   another at 0x01.
2. **Limited Tooling:** As a niche language, SystemRDL has limited support in editors, formatters, and tooling.
3. **Flexibility:** The schema was too rigid, requiring workarounds to describe real-world chip behavior which varies
   between manufacturers.

The project pivoted to **YAML** to solve these issues. YAML is universally supported, human-readable, allows for
comments, and gives us the flexibility to build a schema that *perfectly* matches the needs of embedded sensor
development, not ASIC design.

## 3. Core Technologies

* **Python:** The core application is written in Python, providing a cross-platform CLI.
* **YAML:** The format for chip specifications. Chosen for its readability, native commenting, and universal support.
* **Jinja:** A powerful templating engine that separates the generation logic from the output code's structure, allowing
  ChipLib to be language-agnostic.

## 4. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TSprech/ChipLib.git
   cd ChipLib
   ```

2. Install the required Python packages. It is recommended to use a Python virtual environment.
   ```bash
   # Create and activate a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate
   
   # Install required packages
   pip install -r requirements.txt
   ```

## 5. Usage & Command-Line Interface

ChipLib is a command-line tool. The basic command requires a specification file, a template, and an output path.

### Example

```bash
python chiplib.py TMP1075N.yaml -t cpp_module.jinja -o TMP1075N.cppm
```

This command:

1. Reads the spec from `TMP1075N.yaml`.
2. Uses the template `cpp_module.jinja`.
3. Writes the generated C++ header to `TMP1075N.cppm`.

### CLI Arguments

The CLI is built with `rich-argparse` for a clear help menu. Running `python chiplib.py --help` will display a help
summary:

| Argument     | Short        | Description                          | Required |
|:-------------|:-------------|:-------------------------------------|:---------|
| `spec_file`  | (Positional) | Path to the YAML specification file. | **Yes**  |
| `--template` | `-t`         | Path to the Jinja template file.     | **Yes**  |
| `--output`   | `-o`         | Path for the generated output file.  | **Yes**  |
| `--verbose`  | `-v`         | Set the logging level.               | No       |

## 6. The YAML Specification Format

The YAML file is the heart of the project. It is designed to be a human-readable translation of the datasheet.

### Top-Level Structure

| Key              | Required | Type   | Description                                                            |
|:-----------------|:---------|:-------|:-----------------------------------------------------------------------|
| `chip`           | **Yes**  | String | The model name (e.g. "TMP1075N"). Used for file names and class names. |
| `manufacturer`   | No       | String | The company name.                                                      |
| `interface`      | No       | List   | List of supported bus types (e.g. `[I2C, SPI]`).                       |
| `description`    | No       | String | A brief description of the chip for documentation.                     |
| `register_width` | **Yes**  | Int    | The default register width in bits (e.g. `16`).                        |
| `access`         | No       | List   | Default access for all registers (e.g. `[r, w]`). Can be overridden.   |
| `enums`          | **Yes**  | List   | A list of all global enum definitions.                                 |
| `registers`      | **Yes**  | List   | A list of all register definitions.                                    |

### `enums` Structure

Defined globally so they can be referenced by multiple fields. Each item in the `enums` list is a map:

| Key      | Required | Type   | Description                                   |
|:---------|:---------|:-------|:----------------------------------------------|
| `symbol` | **Yes**  | String | The C++-safe enum class name (e.g. "SD").     |
| `values` | **Yes**  | List   | List of key-value pairs for each enum member. |

Each item in `values` contains:

| Key           | Required | Type   | Description                                         |
|:--------------|:---------|:-------|:----------------------------------------------------|
| `name`        | **Yes**  | String | Human-readable name (e.g. "Continuous Conversion"). |
| `value`       | **Yes**  | Int    | The numerical value (supports `0b0`, `0x1`, `123`). |
| `description` | No       | String | Doxygen/doc-comment for the enum member.            |

**Example:**

```yaml
enums:
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
```

### `registers` Structure

A list containing all registers on the chip.

| Key       | Required | Type   | Description                                                |
|:----------|:---------|:-------|:-----------------------------------------------------------|
| `address` | **Yes**  | Int    | The bus address (e.g. `0x00`).                             |
| `symbol`  | **Yes**  | String | The name of the register from the datasheet (e.g. `TEMP`). |
| `name`    | No       | String | Human-readable extended name (e.g. `Temperature`).         |
| `reset`   | **Yes**  | Int    | The reset default value (e.g. `0x60A0`).                   |
| `fields`  | **Yes**  | List   | List of all bit fields in this register.                   |

### `fields` Structure

A list containing all fields for a parent register.

| Key | Re quired | Type | Description |
| :--:------------------ | :--- |:-----------------------------------------------------------------------------------|
| `sy mbol` | **      Yes** | String | The name of the register from the datasheet (e.g. `OS`). |
| `bi ts` | **        Yes** | List `[hi, lo]` | The bit range, high bit first (e.g. `[15, 4]`). |
| `na me` | No | String | Human-readable extended name (e.g. `One Shot`). |
| `ac cess` | No | List | *Overrides* register access. e.g. `[r]` (Read-Only), `[woset]` (Write One to Set). |
| `de scription` | No | String | Doxygen/doc-comment for the field. |
| `en um` | No | String | The `symbol` of a global enum to link to this field. |
| `re set` | No | String or Int | *Overrides* register reset. Can be an Int or a String reference to an enum `name`. |

**Example:**

```yaml
registers:
  - address: 0x01
    name: Configuration
    symbol: CFGR
    reset: 0x60A0
    fields:
      - name: Conversion Rate
        symbol: R
        bits: [ 14, 13 ]
        access: [ r ]
        description: "Conversion rate setting"
        enum: R # Links to the global 'R' enum
        reset: Conversion Rate 250 # Overrides 'reset', referencing 'R' enum's 'Conversion Rate 250'
```  

## 7. How Jinja Templates Work

ChipLib uses Jinja to separate the **data** (YAML) from the **presentation** (the generated code). The template file
defines the *shape* of the output.

This design is powerful because it makes ChipLib **language-agnostic**. To generate Python instead of C++, you don't
change the YAML; you just point the generator at a different template.

### Key Jinja Syntax

* `{{ spec.chip }}`: Prints a variable from the YAML data.
* `{%- for reg in spec.registers %}`: Loops over a list (e.g. all registers).
* `{%- if field.enum %}`: Conditional logic (e.g. only add enum logic if `field.enum` exists).
* `{{ bits | bits_to_mask }}`: Uses a custom Python filter (defined in `chiplib.py`) to transform data.

Please refer to the Jinja documentation for more details about Jinja syntax and how to create templates that fit your
requirements.

## 8. Running Tests

This project uses `pytest` for unit and integration testing.

1. Install test dependencies:

   ```bash
   pip install pytest pytest-mock pytest-cov
   ```

2. Run tests from the root directory:

   ```bash
   pytest
   ```

3. Run tests with a coverage report:

   ```bash
   pytest --cov=chiplib
   ```

## 9\. Contributing

Contributions are welcome\! If you'd like to fix a bug in the generator, add a new language template, or contribute
documentation, please feel free to open an issue or submit a pull request.

## 10\. License

This project is licensed under the **Apache 2.0**. See the `LICENSE` file for details.
