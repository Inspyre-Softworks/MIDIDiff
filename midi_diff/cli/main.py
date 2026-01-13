"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/main.py

Description:
    Main CLI entry point with command routing logic.
"""

import sys

from midi_diff.cli.parser import build_parser
from midi_diff.cli.commands import run_diff, run_debug_info


def cli() -> None:
    """Main CLI entry point that routes to appropriate command handlers."""
    parser = build_parser()

    # Backward compatibility: if arguments look like old-style positional args
    # (3+ args without a subcommand), inject 'diff' as the subcommand
    if len(sys.argv) >= 4 and sys.argv[1] not in [
        'diff',
        'debug-info',
        '-V',
        '--version',
        '-h',
        '--help',
    ]:
        sys.argv.insert(1, 'diff')

    args = parser.parse_args()

    if args.command == 'diff':
        run_diff(args.file_a, args.file_b, args.out_file)
    elif args.command == 'debug-info':
        run_debug_info(copy=args.copy)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    cli()
