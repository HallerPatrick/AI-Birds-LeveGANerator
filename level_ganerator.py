# LevelGANerator Main Entry Point

# Script is calling the single modules with a subprocess to ensure relative imports of files and packages

import os
import subprocess

import click

# Please change if necessary, but should be a python 3.7
PYTHON_BIN = "python3"

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


@click.group()
#@click.option("--parameter_file", "-pf", default="./parameters.txt")
def cli():
    pass


@cli.command()
@click.argument("level_count")
def baseline():
    """
    This task generates sample level xmls from the baseline 
    level generator provided by the AI Birds Competition

    """
    with cd("baseline"):
        subprocess.call([PYTHON_BIN, "baseline.py"])

@cli.command()
def raw_level():
    """

    """

    with cd("raw_level_generator"):
        subprocess.call([PYTHON_BIN, "raw_level_generator.py"])


@cli.command()
@click.argument("epochs")
def train(epochs):
    """
    Training the keras model from sample data (default epoch=2000)

    """

    with cd("nn"):
        subprocess.call([PYTHON_BIN, "train.py"])

@cli.command()
def doctor():
    """
    Running the doctor to check for dependencies and if other tools are installed

    """

    with cd("other/doctor"):
        subprocess.call([PYTHON_BIN, "doctor.py"])

@cli.command()
def gen():
    """


    """
    
    with cd("xml_generator"):
        subprocess.call([PYTHON_BIN, "__main__.py"])

if __name__ == "__main__":
    cli()
