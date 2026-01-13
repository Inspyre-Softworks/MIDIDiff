import os
from pathlib import Path

# Create the cli package directory
cli_dir = Path(r'C:\Users\tayja\PycharmProjects\MIDIDiff\midi_diff\cli')
cli_dir.mkdir(exist_ok=True)

print(f"Created directory: {cli_dir}")
