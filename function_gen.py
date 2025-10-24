# function_generator.py

from systemrdl.node import FieldNode
from systemrdl.rdltypes import UserEnum, AccessType, OnWriteType
from doxy_gen import DoxygenCommentGenerator  # Import the Doxygen generator
import logging

log = logging.getLogger("rdl_compiler")

class FunctionGenerator:
    """Generates C++ function strings based on FieldNode information."""
    def __init__(self):
        self.enums = []

    # @staticmethod
    def generate_enum_string(self, encode: UserEnum, regwidth: int, encode_name: str) -> str:
        """Generates C++ enum string."""
        members = [f'  {e.name} = {e.value}, /**< {e.rdl_desc} */' for e in encode]
        return f'enum class {encode_name} : uint{regwidth}_t {{\n' + '\n'.join(members) + '\n};\n\n'

    # @staticmethod
    def binary_range_to_mask(self, bit_range: tuple[int, int], total_bit_length: int = 8) -> str:
        """Converts a bit range to a binary mask string."""
        try:
            num_ones = (bit_range[0] - bit_range[1]) + 1
            sequential_ones = (1 << num_ones) - 1
            shifted_ones = sequential_ones << bit_range[1]
            print(f"Bit range {bit_range}")
            return format(shifted_ones, f'#0{total_bit_length + 2}b')
        except Exception as e:
            log.error(f"Invalid bit range: {bit_range}, and bit length: {total_bit_length}")

    # @staticmethod
    def generate_function_string(self, node: FieldNode, width: int, reg_name: str, address: int) -> list[str]:
        """Generates C++ function string for a FieldNode."""
        encode = node.get_property('encode')
        encode_name = ""
        name = node.get_property('name')
        # if name.__contains__(''):
        #     print(f"Name contains spaces: {name}")
        if encode:
            if encode.__name__[0] == '_':
                encode_name = f'{encode.__name__[1:-5]}_Options'
            else:
                encode_name = f'{name}_Options'
        access_type = node.get_property('sw')
        onwrite_type = node.get_property('onwrite')
        reg_var_name = reg_name.lower() + '_'
        function_string = ""
        enum_string = ""

        if encode:
            if encode_name not in self.enums:
                enum_string += DoxygenCommentGenerator.generate_enum_comment(node, encode)
                enum_string += self.generate_enum_string(encode, width, encode_name)
                self.enums.append(encode_name)

        print(f"Name {name}")

        if onwrite_type == OnWriteType.wzc:
            access_type = AccessType.na
            function_string += DoxygenCommentGenerator.generate_wzc_comment(node)
            function_string += f'[[nodiscard("Function returns expected which represents success or failure")]]\n'
            function_string += f'auto {name}() -> std::expected<void, std::error_code> {{\n'
            function_string += f'  this->{reg_var_name} = register_parser::parse::Register{width}Bit(this->{reg_var_name}, {self.binary_range_to_mask((node.high, node.low), width)}_u{width}, 0_u{width});\n'
            # function_string += f'  return this->Write{width}(0x{address >> width//8 - 1:X}, this->{reg_var_name});\n' # This shift removes what is added due to it not being an 8 bit register in the rdl file
            function_string += f'  return this->Write{width}(0x{address:X}, this->{reg_var_name});\n' # This shift removes what is added due to it not being an 8 bit register in the rdl file
            function_string += f'}}\n\n'

        if access_type in (AccessType.rw, AccessType.w):
            function_string += DoxygenCommentGenerator.generate_write_comment(node, encode, encode_name)
            param_type = encode_name if encode else f'uint{width}_t'
            function_string += f'[[nodiscard("Function returns expected which represents success or failure")]]\n'
            function_string += f'auto {name}(const {param_type} value) -> std::expected<void, std::error_code> {{\n'
            function_string += f'  this->{reg_var_name} = register_parser::parse::Register{width}Bit(this->{reg_var_name}, {self.binary_range_to_mask((node.high, node.low), width)}_u{width}, static_cast<uint{width}_t>(value));\n'
            function_string += f'  return this->Write{width}(0x{address:X}, this->{reg_var_name});\n' # This shift removes what is added due to it not being an 8 bit register in the rdl file
            function_string += f'}}\n\n'

        if access_type in (AccessType.rw, AccessType.r):
            function_string += DoxygenCommentGenerator.generate_read_comment(node, encode, width, encode_name)
            return_type = encode_name if encode else f'uint{width}_t'
            function_string += f'[[nodiscard("Function returns expected which represents success or failure")]]\n'
            function_string += f'auto {name}() -> std::expected<{return_type}, std::error_code> {{\n'
            function_string += f'  if (const auto read_result = this->Read{width}(0x{address:X}); !read_result) [[unlikely]] return std::unexpected(read_result.error());\n'
            function_string += f'  else [[likely]] this->{reg_var_name} = read_result.value();\n'
            function_string += f'  return {f"static_cast<" + return_type + f">(register_parser::parse::Register{width}Bit(this->{reg_var_name}, {self.binary_range_to_mask((node.high, node.low), width)}_u{width}))" if encode else f"register_parser::parse::Register{width}Bit(this->{reg_var_name}, {self.binary_range_to_mask((node.high, node.low), width)}_u{width})"};\n'
            function_string += f'}}\n\n'

        return [function_string, enum_string]