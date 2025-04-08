import typer

app = typer.Typer(help="Hello world commands")

@app.callback()
def callback():
    """Hello world commands."""

@app.command()
def world():
    """Print Hello World!"""
    typer.echo("Hello World!")
    
# Make "world" the default command for "hello"
app.command()(world)