import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="""
Run linting for a Quantum Machine.

This command checks code formatting and style issues using tools like flake8 or pylint.

Example:
    quantum lint machine HelloWorld
""")

@app.command()
def machine(path: str):
    """
    Run linting for a Quantum Machine.

    This command checks code formatting and style issues using tools like flake8 or pylint.

    Example:
        quantum lint machine HelloWorld
    """
    project_path = Path(path).resolve()

    if not (project_path / "main.py").exists():
        typer.secho("❌ No main.py found to lint.", fg=typer.colors.RED)
        raise typer.Exit()

    try:
        subprocess.run(["flake8", str(project_path)], check=True)
        typer.secho("✅ Lint passed: No major issues found!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("⚠️ Linting failed. Please fix the above issues.", fg=typer.colors.YELLOW)