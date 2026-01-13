"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/parser.py

Description:
    Argument parser configuration for the CLI.
"""

import argparse

from midi_diff.cli.version import VersionAction, UPDATE_CHECK_ENV_VAR


def build_parser() -> argparse.ArgumentParser:
    """
    Build and configure the argument parser for the CLI.
    
    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog='midi-diff',
        description='MIDIDiff - Compare MIDI files and output their differences.',
    )

    parser.add_argument(
        '-V',
        '--version',
        action=VersionAction,
        nargs=0,
        help=(
            f'Show version and environment info '
            f'(set {UPDATE_CHECK_ENV_VAR} to a truthy value to check for updates).'
        ),
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    diff_parser = subparsers.add_parser(
        'diff',
        help='Compare two MIDI files and output their differences',
    )
    diff_parser.add_argument('file_a', help='Path to the first MIDI file.')
    diff_parser.add_argument('file_b', help='Path to the second MIDI file.')
    diff_parser.add_argument('out_file', help='Path for the diff MIDI output.')

    debug_parser = subparsers.add_parser(
        'debug-info',
        help='Display diagnostic and environment information',
    )
    debug_parser.add_argument(
        '-c',
        '--copy',
        action='store_true',
        help='Copy the debug markdown to the clipboard.',
    )

    return parser
