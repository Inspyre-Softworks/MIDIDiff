# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md file to track project changes
- Contribution guidelines (CONTRIBUTING.md) with changelog maintenance requirements
- Pull request template with changelog update requirements
- Issue templates for bug reports and feature requests
- `rich` library as a dependency for enhanced terminal output
- Colorized and formatted version output (`-V`/`--version`) using rich panels and tables
- `debug-info` subcommand for displaying comprehensive diagnostic information in Rich Markdown format

### Changed
- Updated documentation to mandate changelog updates for user-facing changes
- Consolidated changelog guidance to CONTRIBUTING.md with references from AGENTS.md and copilot-instructions.md to reduce duplication
- Simplified PR template to have single changelog checklist item instead of duplicate entries
- Version info display now uses rich formatting with colored table and panel layout
- CLI refactored to use subcommand structure (argparse subparsers) with `diff` and `debug-info` subcommands
- **BREAKING (internal):** Refactored `midi_diff/cli.py` monolithic module (310 lines) into a package structure with separation of concerns:
  - `midi_diff/cli/__init__.py` - Package entry point exporting `cli()` function
  - `midi_diff/cli/main.py` - Main CLI entry point with command routing
  - `midi_diff/cli/parser.py` - Argument parser configuration
  - `midi_diff/cli/version.py` - Version information and update checking
  - `midi_diff/cli/debug.py` - Debug information generation
  - `midi_diff/cli/clipboard.py` - Cross-platform clipboard operations
  - `midi_diff/cli/commands.py` - Command handler functions
  - `midi_diff/cli/__main__.py` - Module execution support (`python -m midi_diff.cli`)
  - All public APIs remain unchanged; this is purely an internal restructuring

## [1.0.0-dev.3] - 2026-01-12

### Changed
- Refactored CLI version lookup to reuse shared metadata retrieval and remove duplication

## [1.0.0-dev.2] - 2026-01-10

### Added
- Command-line tool for comparing MIDI files and generating diff files
- Support for note matching by pitch, start tick, and duration (velocity ignored)
- Automatic output file name incrementing to prevent overwrites
- Version flag (`-V`/`--version`) with environment details and PyPI update check
- Poetry-based build system with Python 3.13+ requirement
- Extract notes from MIDI files using `mido` library
- Set-based note comparison for efficient diffing
- Output only notes present in one file but not the other
- Immutable `NoteEvent` dataclass with MIDI bounds validation

[Unreleased]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.3...HEAD
[1.0.0-dev.3]: https://github.com/tayjaybabee/MIDIDiff/compare/v1.0.0-dev.2...v1.0.0-dev.3
[1.0.0-dev.2]: https://github.com/tayjaybabee/MIDIDiff/releases/tag/v1.0.0-dev.2
