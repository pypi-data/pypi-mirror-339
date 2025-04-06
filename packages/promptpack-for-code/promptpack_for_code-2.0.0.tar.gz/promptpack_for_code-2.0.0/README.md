# promptpack-for-code

![PyPI](https://img.shields.io/pypi/v/promptpack-for-code.svg)

A command-line tool that bundles your code files into a single text or XML file, optimized for AI code review and analysis. It helps developers prepare their codebase for productive conversations with AI language models by combining multiple source files into a well-formatted context.

## Installation

```bash
pip install promptpack-for-code
```

## Usage

You can use the tool with its full name `promptpack-for-code` or with the convenient short aliases: `ppc` or `packcode`.

Basic usage with a single directory:
```bash
ppc /path/to/your/code
```

Process multiple directories:
```bash
ppc dir1 dir2 dir3
```

Specify root directory for tree structure and full relative paths:
```bash
ppc /path/to/specific/folder -r /path/to/project/root
```

Specify output file path (default is output.xml):
```bash
ppc /path/to/src -o /path/to/output/result.xml
```

Generate text output instead of XML (XML is now the default):
```bash
ppc /path/to/src --format text
```

Ignore specific patterns:
```bash
ppc /path/to/src --ignore "*.log" "*.tmp"
```

Show progress bar during processing:
```bash
ppc /path/to/src --progress
```

Force overwrite existing output file:
```bash
ppc /path/to/src -f
```

## Features

- Combines multiple source files from one or more directories into a single output file
- Generates a tree-like directory structure based on the specified root
- Preserves file structure with full relative paths from the root directory
- Supports both XML (default) and plain text output formats
- Built-in ignore patterns for common files (e.g., `.git`, `__pycache__`, etc.)
- Customizable output file path
- Optional progress bar for large projects
- Easy to integrate with various AI chat platforms
- Multiple command aliases: `promptpack-for-code`, `ppc`, and `packcode`

## Output Formats

### Text Format

The generated text output file contains:
1. A tree-like representation of your project structure (based on the root directory)
2. The contents of all files in the specified directories, with paths relative to the root

Example text output:
```
Project Directory Structure:
==========================
project-name
├── src
│   ├── main.py
│   └── utils
│       └── helper.py
└── tests
    └── test_main.py

File Contents from Selected Directories:
===================================

====
File: src/main.py
----
[file content here]
```

### XML Format

The generated XML output file provides a structured representation with:
1. A hierarchical view of your project directory structure
2. The contents of all specified files, with paths relative to the root

Example XML output:
```xml
<project>
  <name>project-name</name>
  <structure>
    <directory path="src">
      <file path="main.py" />
      <directory path="utils">
        <file path="helper.py" />
      </directory>
    </directory>
    <directory path="tests">
      <file path="test_main.py" />
    </directory>
  </structure>
  <contents>
    <file path="src/main.py">
      <content>
        [file content here]
      </content>
    </file>
    <!-- Other file contents -->
  </contents>
</project>
```

The XML format offers better structure and is easier to parse programmatically, making it ideal for automated analysis or integration with other tools.

## Command Aliases

For convenience, this tool provides three command aliases:

- `promptpack-for-code`: The full name
- `ppc`: Short alias for quicker typing
- `packcode`: Alternative alias

All commands provide identical functionality:

```bash
# These all do the same thing (generate XML by default):
promptpack-for-code /path/to/src
ppc /path/to/src
packcode /path/to/src

# These all generate text output:
promptpack-for-code /path/to/src --format text
ppc /path/to/src --format text
packcode /path/to/src --format text
```

## Development

To contribute to this project:

1. Clone the repository:
```bash
git clone https://github.com/changyy/py-promptpack-for-code.git
cd py-promptpack-for-code
```

2. Install in development mode:
```bash
pip install -e .
```

## Requirements

- Python 3.6+
- tqdm (for progress bar support)

## License

MIT License - see LICENSE file for details
