"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/commands.py

Description:
    Command handler functions for the CLI.
"""

from midi_diff.core import main
from midi_diff.cli.debug import print_debug_info


def run_diff(file_a: str, file_b: str, out_file: str) -> None:
    """
    Run the MIDI diff command.
    
    Parameters:
        file_a: Path to the first MIDI file.
        file_b: Path to the second MIDI file.
        out_file: Path for the diff MIDI output.
    """
    main(file_a, file_b, out_file)


def run_debug_info(*, copy: bool = False) -> None:
    """
    Run the debug-info command.
    
    Parameters:
        copy: If True, copy the debug markdown to the clipboard.
    """
    print_debug_info(copy=copy)
