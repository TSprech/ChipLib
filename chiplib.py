import yaml
import sys
import os
import argparse
import logging
from jinja2 import Environment, FileSystemLoader
from rich_argparse import RichHelpFormatter
from rich.logging import RichHandler

# Setup logging configuration globally
log = logging.getLogger("chiplib-core")


def setup_logging(level: int):
    """Sets up rich-formatted logging based on verbosity level argument."""

    # Map CLI verbosity (0, 1, 2) to logging levels
    log_level = {
        0: logging.WARNING,  # Default: Only show WARNING, ERROR, CRITICAL
        1: logging.INFO,  # Show INFO messages
        2: logging.DEBUG  # Show detailed DEBUG messages
    }.get(level, logging.WARNING)

    log.setLevel(log_level)

    # Configure the RichHandler
    handler = RichHandler(
        level=log_level,
        show_time=True,
        show_level=True,
        show_path=False,
        rich_tracebacks=True,
        log_time_format="%H:%M:%S"
    )

    if not log.handlers:
        log.addHandler(handler)
        log.propagate = False

    return log


def parse_args():
    """Defines and parses command-line arguments using RichHelpFormatter."""
    parser = argparse.ArgumentParser(
        description="ChipLib-Core: YAML Register Specification to C++ Header Generator.",
        epilog="Use -v for INFO logs, -vv for DEBUG logs.",
        formatter_class=RichHelpFormatter
    )

    # --- Core Arguments ---
    parser.add_argument(
        "yaml_file",
        metavar="<YAML_SPEC>",
        type=str,
        help="Path to the mandatory input YAML register specification file.",
    )

    parser.add_argument(
        "-t", "--template",
        dest="template_file",
        type=str,
        help="Path to the Jinja2 template file.",
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        type=str,
        help="Path for the generated C++ header file.",
    )

    # --- Utility Arguments ---
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="Increase output verbosity. Use -vv for debug level.",
    )

    args = parser.parse_args()
    return args


# --- Helper Function for Jinja ---
def bits_to_mask(bit_range: list):
    """
    Converts a bit range list (e.g., [15, 4]) into a C++ hexadecimal mask string.
    """
    if not isinstance(bit_range, list) or len(bit_range) != 2:
        log.error(f"Bits filter received invalid range: {bit_range}. Expected [high, low].")
        return "0x0"  # Return a safe default mask

    high, low = bit_range[0], bit_range[1]

    width = high - low + 1
    mask = ((1 << width) - 1) << low

    # Use bit_length // 4 to get hex width, ensuring we handle zero properly
    hex_width = (mask.bit_length() + 3) // 4
    return f"0x{mask:0{hex_width}X}"


def generate_cpp_header(yaml_data, template_path, output_path):
    """
    Loads data, configures Jinja, and generates the C++ header file.
    """
    try:
        # Setup Jinja Environment
        file_loader = FileSystemLoader(os.path.dirname(template_path) or '.')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

        # Register the custom filter
        env.filters['bits_to_mask'] = bits_to_mask

        # Load the template (use just the filename if path was resolved by FileSystemLoader)
        template_filename = os.path.basename(template_path)
        template = env.get_template(template_filename)
        log.debug(f"Jinja template '{template_filename}' loaded successfully.")

        # Execute the template
        cpp_output = template.render(spec=yaml_data)

        # Write the output file
        with open(output_path, 'w') as f:
            f.write(cpp_output)

        # Success message handled in main
        return True

    except Exception as e:
        log.exception(f"Error executing template or writing output for '{template_path}': {e}")
        raise  # Re-raise exception to be caught in main


if __name__ == '__main__':
    args = parse_args()
    setup_logging(args.verbosity)

    log.info("Starting ChipLib-Core code generation.")
    log.debug(f"Parsed arguments: {vars(args)}")

    # --- 3. Validation on file existence ---
    if not os.path.exists(args.yaml_file):
        log.error(f"Input YAML file not found at: [bold red]{args.yaml_file}[/bold red]")
        sys.exit(1)

    if not os.path.exists(args.template_file):
        log.error(f"Jinja template file not found at: [bold red]{args.template_file}[/bold red]")
        sys.exit(2)

    # Load YAML data
    try:
        with open(args.yaml_file, 'r') as f:
            spec_data = yaml.safe_load(f)
        log.info(f"Successfully loaded and parsed specification from [cyan]{args.yaml_file}[/cyan].")

    except Exception:
        log.exception(f"Fatal error while loading or parsing YAML file: {args.yaml_file}")
        sys.exit(3)

    # Start generation
    try:
        generate_cpp_header(spec_data, args.template_file, args.output_file)
        log.info(f"Generation complete. Output written to [green]{args.output_file}[/green].")
    except Exception:
        # Exception already logged in generate_cpp_header
        log.error("Code generation failed due to a template or output error.")
        sys.exit(4)
