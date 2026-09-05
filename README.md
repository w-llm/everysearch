# everysearch

A fast, no-dependency command-line tool to search for files and
directories by name — from anywhere on your system.

## Installation

Clone the repo and install locally:

```bash
git clone https://github.com/yourusername/everysearch.git
cd everysearch
pip install .
```

For active development (changes reflect immediately without reinstalling):

```bash
pip install -e .
```

Once installed, `everysearch` is available as a global command in
`cmd`, PowerShell, or Terminal.

## Usage

```bash
everysearch <search_term> [directory] [options]
```

- `search_term` — required. Text to match against file/directory names.
- `directory` — optional. Defaults to the current working directory.

### Options

| Flag                | Description                              |
|----------------------|-------------------------------------------|
| `-c`, `--case-sensitive` | Match exact case                      |
| `--dirs-only`         | Show only matching directories            |
| `--files-only`        | Show only matching files                  |
| `-v`, `--version`     | Show installed version                    |
| `-h`, `--help`        | Show help message                         |

## Examples

Search the current directory for anything containing "invoice":

```bash
everysearch invoice
```

Search a specific directory:

```bash
everysearch report ~/Documents
```

Case-sensitive search, files only:

```bash
everysearch README --files-only -c
```

Show only matching folders:

```bash
everysearch node_modules /projects --dirs-only
```

### Sample Output
