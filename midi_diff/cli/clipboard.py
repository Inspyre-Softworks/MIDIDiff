"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/clipboard.py

Description:
    Cross-platform clipboard operations for copying text.
"""

import shutil
import subprocess
import sys
from typing import Optional


def copy_to_clipboard(text: str) -> Optional[str]:
    """
    Copy text to the system clipboard.
    
    Parameters:
        text: The text to copy to the clipboard.
    
    Returns:
        None if successful, or an error message string if it failed.
    """
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
