"""Command line application."""

import typer

import bindly

app = typer.Typer()


@app.command()
def about() -> None:
    """Display the package's tagline."""
    typer.echo(bindly.__doc__)


@app.command()
def version() -> None:
    """Display the package's version."""
    typer.echo(bindly.__version__)
