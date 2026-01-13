"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/debug.py

Description:
    Debug information generation and display functionality.
"""

import os
import platform

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from midi_diff.cli.version import (
    get_version,
    get_dependency_version,
    UPDATE_CHECK_ENV_VAR,
)
from midi_diff.cli.clipboard import copy_to_clipboard


def build_debug_markdown() -> str:
    """
    Build the markdown content for debug-info output.
    
    Returns:
        A markdown-formatted string with debug information.
    """
    mididiff_version = get_version()
    python_version = platform.python_version()
    platform_info = platform.platform()
    mido_version = get_dependency_version('mido')
    rich_version = get_dependency_version('rich')

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


def print_debug_info(*, copy: bool = False) -> None:
    """
    Print debug information in a formatted panel.
    
    Parameters:
        copy: If True, copy the debug markdown to the clipboard.
    """
    console = Console()
    markdown_text = build_debug_markdown()

    panel = Panel(
        Markdown(markdown_text),
        border_style='cyan',
        padding=(1, 2),
        title='[bold cyan]Debug Information[/bold cyan]',
    )
    console.print(panel)

    if copy:
        err = copy_to_clipboard(markdown_text)
        if err is None:
            console.print('[green]✓ Debug markdown copied to clipboard.[/green]')
        else:
            console.print(f'[red]{err}[/red]')
