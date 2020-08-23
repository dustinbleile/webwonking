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
from glob import glob
from os.path import abspath, dirname, exists, isdir, join
from shutil import copyfile

try:
    from doit import get_initial_workdir
    from doit.tools import run_once
except ImportError:
    run_once = False

    def get_initial_workdir():
        return "."


DOIT_CONFIG = {
    "verbosity": 2,  # just make it all verbose
    "default_tasks": None,  # [],  # None is all tasks by default
}


def venv_install():
    print("Running venv_install task")
    venv_dir = abspath("./venv")
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
        "uptodate": [exists(venv_path)],
        # "file_dep": ["./venv"],
        "verbosity": 2,
    }


def setup_files(output_folder, dryrun=False):
    """
    Copy common python setup files
    """
    BASE, DEST = range(2)
    SETUP_FILES = [  # (basename, dest_name)
        ("dodo.py", "dodo.py"),
        ("README_template.md", "README.md"),
        ("setup_py_template.py", "setup.py"),
        ("gitignore.base", ".gitignore"),
    ]
    folder = dirname(__file__)
    print(__file__)
    files_base = [abspath(join(folder, fn[BASE])) for fn in SETUP_FILES]
    files_dest = [abspath(join(output_folder, fn[DEST])) for fn in SETUP_FILES]
    pref = "would copy" if dryrun else ""
    for dest, base in zip(files_dest, files_base):
        if not exists(dest):
            logging.warning(f"{pref}{dest}")
            logging.warning(f"\tfrom: {base}")
            if not dryrun:
                copyfile(base, dest)
    return all(exists(fn) for fn in files_dest)


def task_initial_setup_files():
    # Use clean instead of actions for the dryrun parameter to work
    return {
        "actions": [(setup_files, [], {'output_folder': get_initial_workdir()})],

        "uptodate": [exists(join(get_initial_workdir(), "setup.py"))],
        "verbosity": 2,
    }


def task_pip_update():
    return {
        "actions": [
            "python -m pip install -U pip",
            "python -m pip install -U setuptools doit wheel twine",
        ],
        "uptodate": [run_once],
        "verbosity": 2,
    }


def task_pip_install():
    return {
        "actions": ["python -m pip install -e .[dev] -U --use-feature=2020-resolver"],
        "task_dep": ["pip_update"],
        "file_dep": [join(get_initial_workdir(), "setup.py")],
        "uptodate": [run_once],
        "verbosity": 2,
    }


def task_lint(line_len=100):
    python_files = glob("*.py")
    lint_folders = [fn for fn in glob("*") if isdir(fn) and fn not in ["venv"]]
    files_and_folders =  " ".join(python_files + lint_folders)
    isort_opts = f"--multi-line 3 --trailing-comma -l {line_len} --atomic"
    isort_folder_cmds = [f"find {folder} -name '*.py' -exec isort {isort_opts} {{}} + " for folder in lint_folders]
    
    return {
        "actions": isort_folder_cmds + [
            f"isort --multi-line 3 --trailing-comma -l {line_len} --atomic {' '.join(python_files)}",
            f"black --line-length {line_len} {files_and_folders}",
            f"flake8 --max-line-length {line_len} {files_and_folders}",
            f"mypy --ignore-missing-imports {files_and_folders}",
        ],
        "verbosity": 2,
    }
