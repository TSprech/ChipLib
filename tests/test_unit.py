import logging

import pytest
from chiplib import bits_to_mask, parse_args, setup_logging


# Bit Range Function
@pytest.mark.parametrize("bit_range, expected_mask", [
    ([15, 4], "0xFFF0"),  # 12 bits, shifted 4
    ([7, 0], "0xFF"),  # 8 bits, shifted 0
    ([31, 16], "0xFFFF0000"),  # 16 bits, shifted 16
    ([4, 4], "0x10"),  # 1 bit, shifted 4
    ([8, 8], "0x100"),  # 1 bit, shifted 8
    ([24, 24], "0x1000000"),  # 1 bit, shifted 4
    ([31, 31], "0x80000000"),  # 1 bit, shifted 31
])
def test_bits_to_mask_valid(bit_range, expected_mask):
    """Tests that the mask generation is correct for various valid inputs."""
    assert bits_to_mask(bit_range) == expected_mask


def test_bits_to_mask_invalid_input(caplog):
    """Tests that the function handles invalid input and logs an error."""
    assert bits_to_mask(12) == "0x0"
    # Check that our log.error() message was captured
    assert "received invalid range" in caplog.text


@pytest.mark.parametrize("int_level, logging_level", [
    (0, logging.WARNING),
    (1, logging.INFO),
    (2, logging.DEBUG)
])

def test_setup_logging_valid(int_level, logging_level):
    """Tests that the logging level is correct for various valid inputs."""
    assert setup_logging(int_level).level == logging_level

def test_setup_logging_invalid():
    """Tests that the logging level is correct for various invalid inputs."""
    assert setup_logging(3).level == logging.WARNING


# Argument Parser
def test_parse_args_all_flags(mocker):
    """Tests that all custom flags are correctly parsed."""
    cli_input = [
        "chiplib.py",
        "test_device.yaml",
        "-t", "test_template.jinja",
        "-o", "test_output.cppm",
        "-vv"  # verbosity = 2
    ]
    mocker.patch("sys.argv", cli_input)

    args = parse_args()

    assert args.yaml_file == "test_device.yaml"
    assert args.template_file == "test_template.jinja"
    assert args.output_file == "test_output.cppm"
    assert args.verbosity == 2
