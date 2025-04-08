# tree2structure

Convert a textual tree-style folder structure into nested Python dicts and generate real files/folders with inline comments.

## Install

```bash
  pip install tree2structure
```

## Usage

```python
from tree2structure.parser import parse_structure
from tree2structure.generator import create_from_structure

structure = parse_structure(your_string_raw_tree)
create_from_structure(structure, base_path="your_project/")
```
