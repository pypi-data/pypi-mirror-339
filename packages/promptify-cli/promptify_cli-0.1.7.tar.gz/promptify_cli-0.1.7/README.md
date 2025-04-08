# Promptify CLI

An interactive CLI to select files, generate markdown suitable for LLM prompts, and copy it to the clipboard.

## Installation

```bash
pip install promptify-cli
```

## Demo

![Promptify CLI Demo](https://raw.githubusercontent.com/olliepro/promptify/refs/heads/main/assets/promptify_example.gif)

## Basic Usage

### Default Behavior
- Run `promptify` to interactively select files and generate markdown for your clipboard
- Supports `.promptignore` files (works like `.gitignore`)
- Offers to add a basic `.promptignore` if none is found at project root. (First time only)
- Includes a file tree to depth 4, excluding ignored files
- Selected files (highlighted green) are md-formatted
- Shows LOC and GPT-4o token counts as you use the UI

### Help

```bash
promptify --help
```

> | Option                 | Short | Type      | Description                       | Default |
> | ---------------------- | ----- | --------- | --------------------------------- | ------- |
> | `--depth`              | `-d`  | INTEGER   | Max directory depth (0=root only) | `4`     |
> | `--path`               | `-p`  | DIRECTORY | Starting directory path           | CWD     |
> | `--clear-state`        |       |           | Clear previous selections         |         |
> | `--install-completion` |       |           | Install shell completion          |         |
> | `--show-completion`    |       |           | Show shell completion             |         |
> | `--help`               |       |           | Show help message and exit        |         |


## Example Output (Copied to Clipboard)

````markdown
Project Structure (Depth: 4):

```
example_documentation_project/
├─ foobar/
│  └─ bar.py
├─ foo.py
└─ output.md
```

---

## File: `foo.py`

```python
def foo(bar):
    return bar

```

---

## File: `foobar/bar.py`

```python
def bar(foo):
    return foo

```
````

## Development

This package is self-contained in 1 file at `src/promptify/cli.py`. It's in a state that the UI and features meet my needs, but if you wish to modify the functionality, add more args, etc. drop me a github issue (slow response time) or feel free to submit a merge request!