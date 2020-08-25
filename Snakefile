"""
Snakemake file run with snakemake -n
May need to install snakemake with conda or pip
"""

# variables - simple python works
linelength = 100
name = "webwonking"


# First rule of a a Snakefile is default 'target'.  Called 'rule all' by convention
rule all:
	# only declare some inputs to show completion
	input:
		"setup.py"
###########################################################
# Standard coding
###########################################################

rule python_files_top_folder:
	output:
		"python_files_top_folder.snktmp.tmp"
	shell:
		"ls *.py > {output}"

# Use Snakemake for simple standard linting as an example
#rule lint: ## check style.  isort and black disagree - so order matters.
#	find $(name) -name '*.py' -exec isort --multi-line 3 --trailing-comma -l $(linelength) --atomic {} +
#	black --line-length $(linelength) $(name)
#	flake8 --max-line-length $(linelength) $(name) tests
#	mypy --ignore-missing-imports $(name)

