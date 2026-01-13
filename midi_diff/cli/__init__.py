"""
Author: 
    Inspyre Softworks

Project:
    MIDIDiff

File: 
    midi_diff/cli/__init__.py

Description:
    CLI package entry point - exports the main cli() function for backward compatibility.
"""

from midi_diff.cli.main import cli

__all__ = ['cli']
