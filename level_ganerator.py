# LevelGANerator Main Entry Point

import click


@click.group()
@click.option("--parameter_file", "-pf", default="./parameters.txt")
def cli():
    pass


@cli.command()
@click.argument("level_count")
def baseline():
    """
    This task generates sample level xmls from the baseline 
    level generator provided by the AI Birds Competition

    """

    print("Baseline")

@cli.command()
def train():
    """

    """

if __name__ == "__main__":
    cli()
