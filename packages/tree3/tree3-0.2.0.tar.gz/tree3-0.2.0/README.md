# Tree3

![Tree3-](https://repository-images.githubusercontent.com/950726237/436e5063-14f9-42a0-923e-b22c8256ce1f)

[![PyPI](https://img.shields.io/pypi/v/tree3)](https://pypi.org/project/tree3/) ![License](https://img.shields.io/pypi/l/tree3) [![GitHub Repo stars](https://img.shields.io/github/stars/amirmazinani/tree3?style=flat&label=github%20stars&color=%2357d9a3)](https://github.com/amirmazinani/tree3) [![PyPI Downloads](https://static.pepy.tech/badge/tree3)](https://pepy.tech/projects/tree3)

**`Tree3`** is a command-line utility designed to simplify the process of working with directory structures (works on all operating systems: `Linux`, `macOS`, `Windows` and etc.). Its core functionalities are:
1. **Displaying Directory Structures:** Generate a visual, tree-like representation of a specified directory, similar to the classic `tree` command but more useful.
   #### Example output:
```
/
├── src/
│   ├── main.py
│   └── utils.py
├── config.py
├── README.md
└── setup.py
```

2. **Creating Directory Structures:** Parse a text file containing a predefined tree structure and create the corresponding directories and empty files on the filesystem.

The tool aims to assist developers, particularly when interacting with AI code generation tools or when sharing project structures. It provides options for filtering based on .gitignore rules, saving the output to a file, and copying the structure to the clipboard.

## Installation
Install tree3 using pip:

```bash
pip install tree3
```

## Usage

tree3 is invoked from the command line.

### Synopsis

```
tree3 [OPTIONS] [path]
```

### Arguments and Options

• **`path` (Optional)**: The directory path whose structure you want to display. Defaults to the current directory (`.`).<br>This argument is ignored if `-i` is used.

• **`-o FILE`, `--output FILE`**: Save the generated tree structure to the specified `FILE`.

• **`-i FILE`, `--input FILE`**: Read a tree structure definition from the specified `FILE` and create the corresponding directories and files.

• **`-g`, `--ignore`**: Respect rules found in the `.gitignore` file within the target directory when generating the tree. This ignores files and directories specified in `.gitignore`.

• **`-c`, `--copy`**: Copy the generated tree structure to the system clipboard.

• **`-v`, `--version`**: Display the version of `tree3` and exit.

• **`-h`, `--help`**: Display the help message and exit.

## Examples

### 1. Display the structure of the current directory:

```bash
tree3 [path]
```

#### output:

```
/
├── tree3/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   ├── parser.py
│   │   └── tree.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── clipboard.py
│   │   ├── file_utils.py
│   │   └── gitignore.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   └── constants.py
├── LICENSE
├── pyproject.toml
├── README.md
└── setup.py
```

### 2. Display the structure of a specific project directory:

```bash
tree3 /path/to/my/project
```

### 3. Display structure, ignoring files/dirs from .gitignore:

```bash
tree3 -g /path/to/my/project
```

### 4. Save the structure to a file and copy it to the clipboard:

```bash
tree3 my_project -c -o structure.txt
```

### 5. Create directories and files from a structure definition file:

```bash
tree3 -i structure.txt
```

## Contributing

Feel free to open issues and pull requests on the [GitHub repository](https://github.com/amirmazinani/tree3).

## License

This project is licensed under the MIT License.

---

Built with ♥ by [Amir Mazinani](https://amirmazinani.ir)!
