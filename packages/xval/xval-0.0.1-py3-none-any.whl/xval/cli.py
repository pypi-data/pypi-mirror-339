import click

@click.group()
def cli():
    """Xval's command line interface."""
    pass

@cli.command()
def hello():
    """Print hello world."""
    click.echo("Hello, World!")

if __name__ == '__main__':
    cli()