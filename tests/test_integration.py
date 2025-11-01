import subprocess
import sys
import os
import textwrap


def test_cli_e2e_run(tmp_path):
    """Tests the application end to end via the command line."""

    spec_file = tmp_path / "spec.yaml"  # Placeholder for a chip's yaml file
    spec_file.write_text(textwrap.dedent("""\
        chip: end2end
        register_width: 8
        registers:
          - address: 0x00
    """))

    template_file = tmp_path / "template.jinja"
    # Have it pull 2 basic fields from the yaml file to validate that exchange works
    template_file.write_text("Chip: {{ spec.chip }}\nRegister Width: {{ spec.register_width }}")

    output_file = tmp_path / "output.txt"  # To hold the output and check against

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chiplib.py"))  # We find the script by navigating up one dir from this test file

    result = subprocess.run(
        [
            sys.executable,  # sys.executable to ensure we use the right python
            script_path,
            str(spec_file),
            "--template", str(template_file),
            "--output", str(output_file),
            "-v"  # Test logging
        ],
        capture_output=True,
        text=True,
    )

    # Check that the CLI command succeeded
    assert result.returncode == 0, f"CLI failed with stderr: {result.stderr}"

    # Check that the log output was correct
    assert "Generation complete" in result.stdout

    # Check that the file was generated with the correct content
    assert output_file.exists(), "Output file was not created"
    assert "Chip: end2end" in output_file.read_text()
    assert "Register Width: 8" in output_file.read_text()
