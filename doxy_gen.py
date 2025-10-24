# doxygen_comment_generator.py

from systemrdl.node import FieldNode
from systemrdl.rdltypes import UserEnum

class DoxygenCommentGenerator:
    """Generates Doxygen comments for enums and functions."""

    @staticmethod
    def generate_enum_comment(node: FieldNode, encode: UserEnum) -> str:
        """Generates Doxygen comment for an enum."""
        return f'/**\n * @brief {encode.type_name.rsplit('_')[0]} | {node.get_path_segment()} | options enum\n */\n'

    @staticmethod
    def generate_wzc_comment(node: FieldNode) -> str:
        """Generates Doxygen comment for a write function."""
        desc = node.get_property('desc')
        return f'/**\n * @brief W | {node.get_path_segment()} | {desc}\n * @returns std::expected<void, std::error_code> Returns void on success, error code on failure.\n */\n'


    @staticmethod
    def generate_write_comment(node: FieldNode, encode: UserEnum, encode_name: str) -> str:
        """Generates Doxygen comment for a write function."""
        desc = node.get_property('desc')
        if encode:
            return f'/**\n * @brief W | {node.get_path_segment()} | {desc}\n * @param value The value to write, from enum {encode_name}.\n * @returns std::expected<void, std::error_code> Returns void on success, error code on failure.\n */\n'
        else:
            return f'/**\n * @brief W | {node.get_path_segment()} | {desc}\n * @param value The value to write.\n * @returns std::expected<void, std::error_code> Returns void on success, error code on failure.\n */\n'

    @staticmethod
    def generate_read_comment(node: FieldNode, encode: UserEnum, regwidth: int, encode_name: str) -> str:
        """Generates Doxygen comment for a read function."""
        desc = node.get_property('desc')
        if encode:
            return f'/**\n * @brief R | {node.get_path_segment()} | {desc} (Read)\n * @returns std::expected<{encode_name}, std::error_code> The read value, from enum {encode_name}, or error code on failure.\n */\n'
        else:
            return f'/**\n * @brief R | {node.get_path_segment()} | {desc} (Read)\n * @returns std::expected<uint{regwidth}_t, std::error_code> The read value, or error code on failure.\n */\n'
