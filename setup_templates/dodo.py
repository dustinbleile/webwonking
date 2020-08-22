#! /usr/bin/env python
"""
doit style setup

Run at command line with 'doit'
functions starting with 'task_' have special meanings

by doit, cwd is the same as this current file.

Use 'get_initial_workdir' for the other
"""

"""
lint: ## check style.  isort and black disagree - so order matters.
	find $(name) -name '*.py' -exec isort --multi-line 3 --trailing-comma -l $(linelength) --atomic {} +
	black --line-length $(linelength) $(name)
	flake8 --max-line-length $(linelength) $(name) tests
	mypy --ignore-missing-imports $(name)
"""

import logging
from os.path import exists, join, abspath
try:
    from doit.tools import run_once
    from doit import get_initial_workdir
except ImportError:
    run_once = False
    def get_initial_workdir():
        return "."

DOIT_CONFIG = {
    'verbosity': 2,  # just make it all verbose
    'default_tasks': None, # [],  # None is all tasks by default
}

def venv_install():
    print("Running venv_install task")
    venv_dir =abspath("./venv")
    if not exists(venv_dir):
        logging.warning(f"INSTALLING VENV: {venv_dir}")
        import venv
        venv.create(venv_dir)
    else:
        print(f"existing venv {venv_dir}")


def task_venv_install():
    venv_path = join(get_initial_workdir(), "venv")
    return {
        "actions": [f"python -m venv {venv_path}", "ls -ld `pwd`/venv"],
        'uptodate': [exists(venv_path)],
        # "file_dep": ["./venv"],
        "verbosity": 2,
        }


def setup_files(output_folder, script_name, copy_files=False):
    BASE, DEST = range(2)
    SETUP_FILES = [  # (basename, dest_name)
        ("dodo.py", "dodo.py"),
        ("setup_py_template.py", "setup.py"),
        ("gitignore.base", ".gitignore"),
    ]
    files_base = [abspath(join('.', fn[BASE])) for fn in SETUP_FILES]
    files_dest = [abspath(join(output_folder, fn[DEST])) for fn in SETUP_FILES]
    for dest, base in zip(files_dest, files_base):
        if not exists(dest):
            logging.warning(f"{dest}")
            logging.warning(f"\tfrom: {base}")


def task_initial_setup_files():
    return {
        'actions': [setup_files],
        'params': [{'name': 'name', 'type': str, 'default': ''},
                    {'name': 'copy_files', 'default': False,
                    help: 'Run all commands - not just show'},
                  ],
        'uptodate': [exists(join(get_initial_workdir(), "setup.py"))],
        "verbosity": 2,
    }


def task_pip_update():
    return {"actions": ["python -m pip install -U pip",
                        "python -m pip install -U setuptools doit wheel twine"],
            'uptodate': [run_once],
            }


def task_pip_install():
    return {
        "actions": ["python -m pip install -e .[dev] -U --use-feature=2020-resolver"],
        "task_dep": ["pip_update"],
        'uptodate': [run_once],
        }

