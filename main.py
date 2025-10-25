import sys

import yaml

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

# def process_template(template_path: str, output_path: str, public_registers_string: str, public_enum_string: str, private_registers_string: str) -> None:
#     """Processes a template file by replacing placeholders with generated code, maintaining indentation."""
#     try:
#         with open(template_path, "r") as template_file:
#             template_content = template_file.read()
#
#         # Find indentation of placeholders
#         public_indent = find_indentation(template_content, "/**{PUBLIC_REG}**/")
#         enum_indent = find_indentation(template_content, "/**{PUBLIC_ENUM}**/")
#         private_indent = find_indentation(template_content, "/**{PRIVATE_REG}**/")
#
#         # Apply indentation to generated strings
#         indented_public_registers = apply_indentation(public_registers_string, public_indent)
#         indented_public_enum = apply_indentation(public_enum_string, enum_indent)
#         indented_private_registers = apply_indentation(private_registers_string, private_indent)
#
#         # Replace placeholders
#         modified_content = template_content.replace("/**{PUBLIC_REG}**/", indented_public_registers).replace("/**{PUBLIC_ENUM}**/", indented_public_enum).replace("/**{PRIVATE_REG}**/", indented_private_registers)
#
#         with open(output_path, "w") as output_file:
#             output_file.write(modified_content)
#         print(f"Template processed and saved to: {output_path}")
#
#     except FileNotFoundError:
#         print(f"Error: Template file not found at {template_path}")
#     except Exception as e:
#         log.exception(f"An error occurred: {e}", exc_info=e)
#
# def find_indentation(content: str, placeholder: str) -> str:
#     """Finds the indentation of a placeholder on the same line in the template content, considering the last preceding newline."""
#     escaped_placeholder = re.escape(placeholder)
#     pattern = rf"(?P<preceding>(?:\n|^).*?(?P<indent>\s*){escaped_placeholder})"
#     match = re.search(pattern, content, re.MULTILINE | re.DOTALL)  # Added flags
#
#     if match:
#         preceding = match.group("preceding")
#         last_newline_pos = preceding.rfind('\n')  # Find the last newline
#         if last_newline_pos != -1:
#             indent_start = last_newline_pos + 1
#         else:
#             indent_start = 0  # Start of string
#
#         indent_match = re.search(r"^\s*", preceding[indent_start:])
#         if indent_match:
#             return indent_match.group(0)
#         else:
#             return ""
#     else:
#         return ""
#
# def apply_indentation(content: str, indent: str) -> str:
#     """Applies indentation to each line of the generated content."""
#     lines = content.splitlines()
#     indented_lines = [f"{indent}{line}" if line.strip() else "" for line in lines]
#     if len(indented_lines) > 0:
#         indented_lines[0] = indented_lines[0][len(indent):] # Remove the indent that is present due to the location of the comment in the template
#     return "\n".join(indented_lines)


if __name__ == '__main__':
    input_files = sys.argv[1]
    try:
        with open(input_files, 'r') as f:
            data = yaml.safe_load(f)
            print(data)
    except Exception as e:
        log.exception(f"An unexpected error occurred: ", exc_info=e)
        sys.exit(1)
