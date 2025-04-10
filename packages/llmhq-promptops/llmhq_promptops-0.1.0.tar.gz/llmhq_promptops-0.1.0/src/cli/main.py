# cli/main.py
import typer
from cli.commands import init, create, render

app = typer.Typer()

app.add_typer(init.app, name="init", help="Initialize promptops structure")
app.add_typer(create.app, name="create", help="Create a new prompt template")
app.add_typer(render.app, name="render", help="Render a prompt with variables")

if __name__ == "__main__":
    app()
