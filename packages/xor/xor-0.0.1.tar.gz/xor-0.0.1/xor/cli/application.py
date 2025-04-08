"""Command line application."""

import typer

import xor

app = typer.Typer()


@app.command()
def about() -> None:
    """Display the package's tagline."""
    typer.echo(xor.__doc__)


@app.command()
def version() -> None:
    """Display the package's version."""
    typer.echo(xor.__version__)
