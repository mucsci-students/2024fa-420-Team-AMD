# 2024fa-420-Team-AMD

# UML Editor

Provided is a terminal based UML editor, which can keep track of class structure and relationships within projects.

Supports:
    - Keeping track of a multitude of classes
    - Noting attributes of a class
    - Storing relationships between classes
    - Saving workspaces to JSON and loading from JSON
    - Friendly UI

## Getting Started

### Setting up the project 

To get started, clone the repo.

```console
    $ git clone https://github.com/mucsci-students/2024fa-420-Team-AMD.git
```

Make sure you have [Python](https://www.python.org/) and [pip](https://pypi.org/project/pip/) installed on your system. Install [virtualenv](https://pypi.org/project/virtualenv/) through pip.

```console
    $ pip install virtualenv
```

In the root folder of the project, initialize the virtual environment.

```console
    $ python -m venv env
```

After creating the environment, activate it. Note that this is different between some platforms.

```console
    $ source env/bin/activate (for MacOS, Linux)
    $ ./env/bin/Activate.ps1 (for Windows Powershell)
```

Finally, install all required libraries within the virtual environment.

```console
    (env) $ pip install -r requirements.txt
```

### Running up the project 

To run, use the python interpreter from the terminal within the root folder.

```console
    (env) $ cd 2024fa-420-Team-AMD
    (env) $ python src/main.py
```

This will launch a graphical view of the editor with a toolbar for defining classes, attributes, and relationships. Some options may be disabled on startup, but they will be enabled as your UML project grows.

To get a command line interface, use the `--cli` flag on startup.

```console
    (env) $ python src/main.py --cli
    (env) $ Welcome to our Unified Modeling Language (UML) program! Please enter a valid command.
    (env) $ Enter UML Command:
```

Use `help` command to get a list of valid commands and enter the help interface. Type `exit` to return to the editor. You can also use `exit` to exit from the editor itself.

## Running Tests

To run the tests for the editor, execute pytest from within the virtual environment.

```console
    (env) $ cd 2024fa-420-Team-AMD
    (env) $ pytest
```

These can also be run from the central `test.py` file in `src/`.

```console
    (env) $ cd 2024fa-420-Team-AMD
    (env) $ python src/test.py
```
