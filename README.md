# ReconcileIaC

This repository contains the code for the AST project.

Below are the instructions to run the project

- Optional: If you don't want to fill out your system with the dependencies, use `python -m venv venv` and activate the virtual environment before installing the dependencies.

1. Install the required dependencies

```bash
pip install -r requirements.txt
```

2. Run the project

```bash
molecule test
```

## Additional

To debug, use the following command

```bash
molecule --debug test
```

You can also use

```bash
molecule -vvv test
```

Or even combine two

```bash
molecule --debug -vvv test
```
