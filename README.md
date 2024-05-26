# ReconcileIaC

This repository contains the code for the AST project.

Below are the instructions to run the project

- Optional: If you don't want to fill out your system with the dependencies, use `python -m venv venv` and activate the virtual environment before installing the dependencies.

```bash
# if on Linux
source venv/bin/activate

# if on Windows
.\venv\Scripts\Activate.ps1
# OR
.\venv\Scripts\Activate.bat
```

1. Install the required dependencies

```bash
pip install -r requirements.txt
```

2. Import your project

Have it somewhere in your system, so it' easier to access later.

3. Run the project

```bash
python distro_tester.py <path_to_your_project>
```

Add flag `--test` if you want immediately run the molecule tests.

Add flag `--clean` if you want to remove the test project folder after the tests.

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

## FAQ

P: My project is throwing this error:

```bash
CRITICAL 'molecule/default/molecule.yml' glob failed.  Exiting.
```

A: Check if your project folder is NOT in `.gitignore`. If it is, remove it from .gitignore and try again.
Here is the [source](https://github.com/ansible/molecule/issues/4117#issuecomment-2036386679) of the solution.
