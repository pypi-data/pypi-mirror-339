# PyFJ

A tool for creating django-ninja projects, based on the template: [django_ninja_template](https://github.com/olivetree123/django_ninja_template)

## Install

Recommended installation using pipx:
```bash
pipx install pyfj
```

You can also install using pip:
```bash
pip install pyfj
```

Or using poetry:

```bash
poetry add pyfj
```

## Usage

After installation, you can use the following commands:

### 1. Create a new project

```bash
# Interactive mode
pyfj create

# Directly specify the name
pyfj create --name=myproject
```

### 2. Rename a project

```bash
# Interactive mode
pyfj rename

# Directly specify the names
pyfj rename --name=old_project_name --new_name=new_project_name
```

### 3. View help

```bash
pyfj --help
pyfj create --help
pyfj rename --help
```

## Features

1. Create new projects - Create a project from the Django Ninja template
2. Rename projects - Rename an existing project, including file contents and directory names

## Requirements

- Python 3.8+
- Git (only required for creating new projects)

## Development

```bash
# Clone the repository
git clone https://github.com/olivetree123/pyfj.git
cd pyfj

# Install dependencies
poetry install

# Install in development mode
poetry install -e .

# Or directly run the test script
python test.py
```
