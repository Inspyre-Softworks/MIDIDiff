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
import json
import os
import platform
import sys
import urllib.error
import urllib.request
import subprocess
import shutil
from typing import Optional
from importlib import metadata

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from midi_diff.core import main


DIST_NAME = 'midi-diff'
PYPI_JSON_URL = f'https://pypi.org/pypi/{DIST_NAME}/json'

# Update check configuration
UPDATE_CHECK_ENV_VAR = 'MIDIFF_CHECK_UPDATES'
UPDATE_CHECK_TRUTHY_VALUES = ('1', 'true', 'yes')


class VersionAction(argparse.Action):
    """Custom argparse action to print version info and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        _print_version_info()
        parser.exit()


def _get_version() -> str:
    return _get_metadata_version(DIST_NAME, 'unknown')


def _get_dependency_version(name: str) -> str:
    return _get_metadata_version(name, 'not installed')


def _get_metadata_version(name: str, fallback: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return fallback


def _check_for_update(current_version: str) -> str:
    try:
        with urllib.request.urlopen(PYPI_JSON_URL, timeout=5) as response:
            payload = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError) as exc:
        return f'Update check failed: {exc}'

    latest = payload.get('info', {}).get('version')
    if not latest:
        return 'Update check failed: missing version metadata.'
    if latest == current_version:
        return 'Up to date.'
    return f'Update available: {latest} (installed {current_version}).'


def _print_version_info() -> None:
    console = Console()
    current_version = _get_version()

    markdown_text = f"""
# Version Information

**MIDIDiff:** {current_version}

----

**Python:** {platform.python_version()}  
**Platform:** {platform.platform()}  

----

**mido:** {_get_dependency_version('mido')}  
**rich:** {_get_dependency_version('rich')}
""".strip()

    panel = Panel(
        Markdown(markdown_text),
        border_style='blue',
        padding=(1, 2),
    )

    console.print(panel)

    if os.getenv(UPDATE_CHECK_ENV_VAR, '').lower() in UPDATE_CHECK_TRUTHY_VALUES:
        update_msg = _check_for_update(current_version)

        if 'Update available' in update_msg:
            console.print(f'[yellow]⚠ {update_msg}[/yellow]')
        elif 'Up to date' in update_msg:
            console.print(f'[green]✓ {update_msg}[/green]')
        else:
            console.print(f'[red]{update_msg}[/red]')
    else:
        console.print(
            f'[dim]Update check disabled '
            f'(set {UPDATE_CHECK_ENV_VAR}=1 to enable).[/dim]'
        )


def _build_debug_markdown() -> str:
    """Build the markdown content for debug-info output."""
    mididiff_version = _get_version()
    python_version = platform.python_version()
    platform_info = platform.platform()
    mido_version = _get_dependency_version('mido')
    rich_version = _get_dependency_version('rich')

    cwd = os.getcwd()

    path_env = os.getenv('PATH', 'not set')
    truncated_path = (
        path_env[:100] + '...'
        if path_env != 'not set' and len(path_env) > 100
        else path_env
    )

    markdown_text = f"""
# MIDIDiff Debug Information

## Version Information

| Component | Version |
|-----------|---------|
| **MIDIDiff** | `{mididiff_version}` |
| **Python** | `{python_version}` |
| **mido** | `{mido_version}` |
| **rich** | `{rich_version}` |

## Platform Information

| Property | Value |
|----------|-------|
| **Platform** | `{platform_info}` |
| **System** | `{platform.system()}` |
| **Release** | `{platform.release()}` |
| **Machine** | `{platform.machine()}` |
| **Processor** | `{platform.processor() or 'unknown'}` |

## Environment

| Variable | Value |
|----------|-------|
| **Working Directory** | `{cwd}` |
| **{UPDATE_CHECK_ENV_VAR}** | `{os.getenv(UPDATE_CHECK_ENV_VAR, 'not set')}` |
| **PYTHONPATH** | `{os.getenv('PYTHONPATH', 'not set')}` |

**PATH** (truncated):
```
{truncated_path}
```

---

*Copy this information when reporting issues or requesting support.*
""".strip()

    return markdown_text


def _copy_to_clipboard(text: str) -> Optional[str]:
    """Copy text to the system clipboard."""
    try:
        import pyperclip  # type: ignore
        pyperclip.copy(text)
        return None
    except Exception:
        pass

    try:
        if sys.platform.startswith('win'):
            subprocess.run(['clip'], input=text, text=True, check=True)
            return None

        if sys.platform == 'darwin':
            subprocess.run(['pbcopy'], input=text, text=True, check=True)
            return None

        if shutil.which('wl-copy'):
            subprocess.run(['wl-copy'], input=text, text=True, check=True)
            return None

        if shutil.which('xclip'):
            subprocess.run(
                ['xclip', '-selection', 'clipboard'],
                input=text,
                text=True,
                check=True,
            )
            return None

        return 'No clipboard utility found.'
    except Exception as exc:
        return f'Clipboard copy failed: {exc}'


def _print_debug_info(*, copy: bool = False) -> None:
    console = Console()
    markdown_text = _build_debug_markdown()

    panel = Panel(
        Markdown(markdown_text),
        border_style='cyan',
        padding=(1, 2),
        title='[bold cyan]Debug Information[/bold cyan]',
    )
    console.print(panel)

    if copy:
        err = _copy_to_clipboard(markdown_text)
        if err is None:
            console.print('[green]✓ Debug markdown copied to clipboard.[/green]')
        else:
            console.print(f'[red]{err}[/red]')


def _build_parser() -> argparse.ArgumentParser:
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


def cli() -> None:
    parser = _build_parser()

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
        main(args.file_a, args.file_b, args.out_file)
    elif args.command == 'debug-info':
        _print_debug_info(copy=args.copy)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    cli()


__all__ = ['cli']
