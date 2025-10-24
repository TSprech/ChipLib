import sys

from systemrdl import RDLCompiler, RDLCompileError, RDLWalker, RegNode, AddrmapNode
from systemrdl import RDLListener

from function_gen import FunctionGenerator
import re
from rich.logging import RichHandler
import logging

# Set up logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rdl_compiler")

from rich import print

def process_template(template_path: str, output_path: str, public_registers_string: str, public_enum_string: str, private_registers_string: str) -> None:
    """Processes a template file by replacing placeholders with generated code, maintaining indentation."""
    try:
        with open(template_path, "r") as template_file:
            template_content = template_file.read()

        # Find indentation of placeholders
        public_indent = find_indentation(template_content, "/**{PUBLIC_REG}**/")
        enum_indent = find_indentation(template_content, "/**{PUBLIC_ENUM}**/")
        private_indent = find_indentation(template_content, "/**{PRIVATE_REG}**/")

        # Apply indentation to generated strings
        indented_public_registers = apply_indentation(public_registers_string, public_indent)
        indented_public_enum = apply_indentation(public_enum_string, enum_indent)
        indented_private_registers = apply_indentation(private_registers_string, private_indent)

        # Replace placeholders
        modified_content = template_content.replace("/**{PUBLIC_REG}**/", indented_public_registers).replace("/**{PUBLIC_ENUM}**/", indented_public_enum).replace("/**{PRIVATE_REG}**/", indented_private_registers)

        with open(output_path, "w") as output_file:
            output_file.write(modified_content)
        print(f"Template processed and saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
    except Exception as e:
        log.exception(f"An error occurred: {e}", exc_info=e)

def find_indentation(content: str, placeholder: str) -> str:
    """Finds the indentation of a placeholder on the same line in the template content, considering the last preceding newline."""
    escaped_placeholder = re.escape(placeholder)
    pattern = rf"(?P<preceding>(?:\n|^).*?(?P<indent>\s*){escaped_placeholder})"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)  # Added flags

    if match:
        preceding = match.group("preceding")
        last_newline_pos = preceding.rfind('\n')  # Find the last newline
        if last_newline_pos != -1:
            indent_start = last_newline_pos + 1
        else:
            indent_start = 0  # Start of string

        indent_match = re.search(r"^\s*", preceding[indent_start:])
        if indent_match:
            return indent_match.group(0)
        else:
            return ""
    else:
        return ""

def apply_indentation(content: str, indent: str) -> str:
    """Applies indentation to each line of the generated content."""
    lines = content.splitlines()
    indented_lines = [f"{indent}{line}" if line.strip() else "" for line in lines]
    if len(indented_lines) > 0:
        indented_lines[0] = indented_lines[0][len(indent):] # Remove the indent that is present due to the location of the comment in the template
    return "\n".join(indented_lines)

class MyModelPrintingListener(RDLListener):
    """Listener for RDLWalker to generate C++ code."""

    def __init__(self):
        self.address_shift_count = 1
        self.width = 8
        self.reg_name = ""
        self.reg_address = 0
        self.reg_default = 0
        self.public_registers_string = ""
        self.public_enum_string = ""
        self.private_registers_string = ""
        self.function_generator = FunctionGenerator()

    def enter_Component(self, node):
        if isinstance(node, AddrmapNode):
            self.address_shift_count = node.get_property('shift_count')
        elif isinstance(node, RegNode):
            self.width = node.get_property('regwidth')
            self.reg_default = node.get_property('reset_default')
            self.reg_name = node.get_path_segment()
            if not self.reg_default:
                print(f"No default value set for {self.reg_name}")
            self.reg_address = node.address_offset
            self.private_registers_string += f'  uint{self.width}_t {self.reg_name.lower() + "_"} = 0x{self.reg_default:0{self.width//4}X};\n'

    def enter_Field(self, node):
        public_registers_string, public_enums_string = self.function_generator.generate_function_string(node, self.width, self.reg_name, self.reg_address >> self.address_shift_count)
        self.public_registers_string += public_registers_string
        self.public_enum_string += public_enums_string

    def exit_Component(self, node):
        if isinstance(node, AddrmapNode):
            template_file_path = f"{node.get_path_segment()}.template.cppm"
            output_file_path = f"{node.get_path_segment()}.cppm"
            process_template(template_file_path, output_file_path, self.public_registers_string, self.public_enum_string, self.private_registers_string)
            self.public_registers_string = ""
            self.private_registers_string = ""

if __name__ == '__main__':
    input_files = sys.argv[1:]
    rdlc = RDLCompiler()
    try:
        for input_file in input_files:
            rdlc.compile_file(input_file)
        root = rdlc.elaborate()
        walker = RDLWalker(unroll=True)
        listener = MyModelPrintingListener()
        walker.walk(root, listener)
    except RDLCompileError:
        sys.exit(1)
    except Exception as e:
        log.exception(f"An unexpected error occurred: ", exc_info=e)
        sys.exit(1)
