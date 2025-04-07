# SynthDef Parser

A Python parser for SuperCollider SynthDef binary files (.scsyndef).

## Installation

```bash
pip install synthdef-parser
```

## Usage

```python
from synthdef_parser import parse_synthdef_file

# Parse from file
result = parse_synthdef_file("path/to/your.scsyndef")

# Or parse from bytes
with open("path/to/your.scsyndef", "rb") as f:
    result = parse_synthdef(f.read())
```

## Features

- Parses SynthDef binary format into Python dictionaries
- Handles all major sections: constants, parameters, UGens, variants
- Preserves the complete structure of the SynthDef

## License

MIT