"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/version.py

Description:
    Version information retrieval, update checking, and version display functionality.
"""

import argparse
import json
import os
import platform
import urllib.error
import urllib.request
from importlib import metadata

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


DIST_NAME = 'midi-diff'
PYPI_JSON_URL = f'https://pypi.org/pypi/{DIST_NAME}/json'

# Update check configuration
UPDATE_CHECK_ENV_VAR = 'MIDIFF_CHECK_UPDATES'
UPDATE_CHECK_TRUTHY_VALUES = ('1', 'true', 'yes')


class VersionAction(argparse.Action):
    """Custom argparse action to print version info and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        print_version_info()
        parser.exit()


def get_version() -> str:
    """Get the version of the MIDIDiff package."""
    return get_metadata_version(DIST_NAME, 'unknown')


def get_dependency_version(name: str) -> str:
    """Get the version of a dependency package."""
    return get_metadata_version(name, 'not installed')


def get_metadata_version(name: str, fallback: str) -> str:
    """
    Get the version of a package from metadata.
    
    Parameters:
        name: The package name.
        fallback: The fallback value if the package is not found.
    
    Returns:
        The version string or the fallback value.
    """
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return fallback


def check_for_update(current_version: str) -> str:
    """
    Check PyPI for available updates.
    
    Parameters:
        current_version: The currently installed version.
    
    Returns:
        A message indicating update status or error.
    """
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


def print_version_info() -> None:
    """Print version information in a formatted panel."""
    console = Console()
    current_version = get_version()

    markdown_text = f"""
# Version Information

**MIDIDiff:** {current_version}

----

**Python:** {platform.python_version()}  
**Platform:** {platform.platform()}  

----

**mido:** {get_dependency_version('mido')}  
**rich:** {get_dependency_version('rich')}
""".strip()

    panel = Panel(
        Markdown(markdown_text),
        border_style='blue',
        padding=(1, 2),
    )

    console.print(panel)

    if os.getenv(UPDATE_CHECK_ENV_VAR, '').lower() in UPDATE_CHECK_TRUTHY_VALUES:
        update_msg = check_for_update(current_version)

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
