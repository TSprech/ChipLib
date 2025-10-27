import yaml
import sys
import os
from jinja2 import Environment, FileSystemLoader

# --- Helper Function for Jinja ---
def bits_to_mask(bit_range):
    """
    Converts a SystemRDL-like bit range string (e.g., '15:4') into a C++ hex mask.
    This function will be registered as a Jinja filter.
    """
    if not isinstance(bit_range, list):
        print(f"Not a list: {bit_range}") # TODO: Error
    # Handle the YAML list format: [ 15, 4 ]
    print(bit_range)
    high, low = bit_range[0], bit_range[1]
    print(high, low)

    width = high - low + 1
    # Create the mask (e.g., for 15:4, mask is 0xFFF0)
    mask = ((1 << width) - 1) << low
    return f"0x{mask:0{mask.bit_length() // 4}X}"


def generate_cpp_header(yaml_data, template_path, output_path):
    """
    Loads data, configures Jinja, and generates the C++ header file.
    """
    try:
        # Setup Jinja Environment
        # FileSystemLoader looks for templates in the current directory
        file_loader = FileSystemLoader('.')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)

        # Register the custom filter
        env.filters['bits_to_mask'] = bits_to_mask

        # Load the template
        template = env.get_template(template_path)

        # Execute the template against the entire YAML data structure
        cpp_output = template.render(spec=yaml_data)

        # Write the output file
        with open(output_path, 'w') as f:
            f.write(cpp_output)

        print(f"Successfully generated C++ header: {output_path}")

    except Exception as e:
        print(f"Error during code generation: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Define file paths
    yaml_file = 'TMP1075N.yaml'
    template_file = 'chip_cpp.jinja'
    output_file = 'TMP1075N_Regs.hpp'

    # Check for input files
    if not os.path.exists(yaml_file):
        print(f"Error: Input YAML file not found at {yaml_file}")
        sys.exit(1)
    if not os.path.exists(template_file):
        print(f"Error: Jinja template file not found at {template_file}")
        sys.exit(1)

    # Load YAML data
    try:
        with open(yaml_file, 'r') as f:
            spec_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML data: {e}")
        sys.exit(1)

    # Start generation
    generate_cpp_header(spec_data, template_file, output_file)

