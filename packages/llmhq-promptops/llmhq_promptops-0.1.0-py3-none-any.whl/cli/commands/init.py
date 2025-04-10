# cli/commands/init.py
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def repo():
    """
    Initialize the LLMHQ-promptops repository structure.
    """
    dirs = [".promptops/prompts", ".promptops/configs", ".promptops/templates", ".promptops/vars"]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    typer.echo("Initialized LLMHQ-promptops repository structure.")
