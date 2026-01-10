"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli.py
 

Description:
    Command-line interface for MIDIDiff to compare two MIDI files and output their differences.

"""
import argparse
import platform
import sys
import urllib.request
import json
from importlib import metadata
from midi_diff.core import main


def _get_version() -> str:
    version = "unknown"
    try:
        version = metadata.version("midi-diff")
    except metadata.PackageNotFoundError:
        pass
    return version


def _get_dependency_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not installed"


def _check_for_update(current_version: str) -> str:
    url = "https://pypi.org/pypi/midi-diff/json"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = json.load(response)
    except Exception as exc:
        return f"Update check failed: {exc}"

    latest = payload.get("info", {}).get("version")
    if not latest:
        return "Update check failed: missing version metadata."
    if latest == current_version:
        return "Up to date."
    return f"Update available: {latest} (installed {current_version})."


def _print_version_info() -> None:
    current_version = _get_version()
    print(f"MIDIDiff {current_version}")
    print(f"Python {platform.python_version()}")
    print(f"Platform {platform.platform()}")
    print(f"mido {_get_dependency_version('mido')}")
    print(_check_for_update(current_version))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two MIDI files and output their differences.",
    )
    parser.add_argument("file_a", nargs="?", help="Path to the first MIDI file.")
    parser.add_argument("file_b", nargs="?", help="Path to the second MIDI file.")
    parser.add_argument("out_file", nargs="?", help="Path for the diff MIDI output.")
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show version, environment info, and update status.",
    )
    return parser


def cli() -> None:
    """
    Command-line interface for MIDIDiff.

    Usage:
        python -m midi_diff.cli fileA.mid fileB.mid diff.mid

    """
    parser = _build_parser()
    args = parser.parse_args()

    if args.version:
        _print_version_info()
        return

    if not args.file_a or not args.file_b or not args.out_file:
        parser.print_usage()
        print("fileA.mid fileB.mid diff.mid")
        return

    main(args.file_a, args.file_b, args.out_file)


if __name__ == "__main__":
    cli()


__all__ = ["cli"]
