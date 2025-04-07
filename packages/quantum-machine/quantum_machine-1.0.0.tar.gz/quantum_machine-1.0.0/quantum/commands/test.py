import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="""
Run tests for a Quantum Machine.

This command looks for test scripts and runs them to validate functionality.

Example:
    quantum test machine HelloWorld
""")

@app.command()
def machine(path: str):
    """
    Run tests for a Quantum Machine.

    This command looks for test scripts and runs them to validate functionality.

    Example:
        quantum test machine HelloWorld
    """
    project_path = Path(path).resolve()
    tests_path = project_path / "tests"

    if not tests_path.exists():
        typer.secho("❌ No 'tests' directory found.", fg=typer.colors.RED)
        raise typer.Exit()

    try:
        subprocess.run(["python", "-m", "unittest", "discover", "-s", str(tests_path)], check=True)
        typer.secho("✅ All tests passed!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("❌ Tests failed.", fg=typer.colors.RED)