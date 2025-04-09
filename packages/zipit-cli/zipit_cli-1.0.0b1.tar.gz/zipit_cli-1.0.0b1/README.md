# zipit-cli

`zipit-cli` is a lightweight command-line tool that zips your current directory, while automatically respecting your `.gitignore` file and any custom exclusions you provide. It is perfect for packaging projects, excluding unwanted files like build artifacts, logs, or virtual environments.

---

### Installation

To install the package from PyPI:

```bash
pip install zipit-cli
```

This will install a CLI command called `zipit`.

---

### Usage

Basic usage:

```bash
zipit
```

Zips the current directory, using the folder name as the output zip file.

---

### Common Options

| Flag             | Description |
|------------------|-------------|
| `--name`         | Specify a custom name for the zip file |
| `--verbose`      | Show detailed log of what is being zipped or skipped |
| `--dry-run`      | Simulate without creating the zip file |
| `--exclude`      | Glob-style patterns to exclude (e.g., `*.log`, `temp/`) |
| `--summary`      | Show a summary with file counts, size, and types |
| `--info`         | Display the config info and exit |
| `--zip-type`     | Control folder structure inside zip: `outer` (default) or `inner` |

---

### Examples

```bash
zipit --name release.zip
zipit --exclude "*.log" "__pycache__/" --summary
zipit --dry-run --verbose
zipit --zip-type inner
zipit --zip-type outer
zipit --info
```

---

### What is `--zip-type`?

| `--zip-type` | ZIP Structure                                      |
|--------------|----------------------------------------------------|
| `outer`      | `project_folder.zip > project_folder > files`      |
| `inner`      | `project_folder.zip > files` (no project folder)   |

---

### Features

- Automatically respects `.gitignore`
- Supports additional `--exclude` patterns
- `--dry-run` mode for safe previewing
- Informative `--summary` and `--info` flags
- Customize zip structure via `--zip-type`

---

### License

MIT License

---

### Author

**Zubin Palit**
