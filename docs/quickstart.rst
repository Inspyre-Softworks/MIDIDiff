Quick Start
===========

Command-Line Interface
----------------------

Basic Usage
~~~~~~~~~~~

The CLI expects two input MIDI files and an output path for the diff:

.. code-block:: bash

   midi-diff fileA.mid fileB.mid diff.mid

You can also run the module directly:

.. code-block:: bash

   python -m midi_diff.cli diff fileA.mid fileB.mid diff.mid

Output Behavior
~~~~~~~~~~~~~~~

* If the output file already exists, MIDIDiff will append an incrementing suffix
  (for example, ``diff_1.mid``) to avoid overwriting.
* The resulting MIDI file contains only notes that are present in one input but
  not the other.

Version Information
~~~~~~~~~~~~~~~~~~~

Use ``-V`` or ``--version`` to print the installed MIDIDiff version, environment
details, and the result of an update check against PyPI:

.. code-block:: bash

   midi-diff --version

Debug Information
~~~~~~~~~~~~~~~~~

Use the ``debug-info`` subcommand to display comprehensive diagnostic information:

.. code-block:: bash

   midi-diff debug-info

Programmatic Usage
------------------

Basic Example
~~~~~~~~~~~~~

You can also use MIDIDiff as a library in your Python code:

.. code-block:: python

   from midi_diff.core import main

   # Compare two MIDI files and save the diff
   main('fileA.mid', 'fileB.mid', 'diff.mid')

Advanced Usage
~~~~~~~~~~~~~~

Work with the lower-level API:

.. code-block:: python

   import mido
   from midi_diff.midi_utils import extract_notes, notes_to_midi

   # Load MIDI files
   mid_a = mido.MidiFile('fileA.mid')
   mid_b = mido.MidiFile('fileB.mid')

   # Extract notes
   notes_a = set(extract_notes(mid_a))
   notes_b = set(extract_notes(mid_b))

   # Compute diff
   diff_notes = notes_a.symmetric_difference(notes_b)

   # Create output MIDI
   diff_mid = notes_to_midi(list(diff_notes), ticks_per_beat=mid_a.ticks_per_beat)
   diff_mid.save('diff.mid')

How Note Matching Works
------------------------

Notes are considered identical when they share the same:

* Pitch
* Start tick
* Duration

Velocity is intentionally ignored so that the diff focuses on musical placement.
