import typer
from pathlib import Path
import yaml
from datetime import datetime

app = typer.Typer(help="Vibe Anchor — persistent project context for agentic coding.")

VIBE_FILE = "vibe.yaml"


@app.command()
def init():
    """
    Initialize a vibe anchor in the current project.
    """
    path = Path(VIBE_FILE)

    if path.exists():
        typer.echo("vibe.yaml already exists.")
        raise typer.Exit()

    data = {
        "project": {
            "created": datetime.utcnow().isoformat(),
            "vibe": "Describe the intended feel and constraints of this project."
        },
        "notes": []
    }

    path.write_text(yaml.safe_dump(data, sort_keys=False))
    typer.echo("Initialized vibe.yaml")


@app.command()
def note(message: str):
    """
    Add a project note or decision.
    """
    path = Path(VIBE_FILE)

    if not path.exists():
        typer.echo("No vibe.yaml found. Run `vibe init` first.")
        raise typer.Exit()

    data = yaml.safe_load(path.read_text())

    data["notes"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "message": message
    })

    path.write_text(yaml.safe_dump(data, sort_keys=False))
    typer.echo("Note added.")


@app.command()
def inject():
    """
    Output project context for AI agents.
    """
    path = Path(VIBE_FILE)

    if not path.exists():
        typer.echo("No vibe.yaml found.")
        raise typer.Exit()

    typer.echo(path.read_text())


if __name__ == "__main__":
    app()
