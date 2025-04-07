import typer
from quantum.commands import init, validate, run, build, test, lint

app = typer.Typer(help="Quantum-CLI: A tool to build, run, test, and validate Quantum Machines.")

app.add_typer(init.app, name="init", help="Initialize a new Quantum Machine scaffold.")
app.add_typer(validate.app, name="validate", help="Validate the structure and config of a Quantum Machine.")
app.add_typer(run.app, name="run", help="Run a Quantum Machine with optional input.")
app.add_typer(build.app, name="build", help="Build a Docker image for a Quantum Machine.")
app.add_typer(test.app, name="test", help="Run unit tests for a Quantum Machine.")
app.add_typer(lint.app, name="lint", help="Lint code for a Quantum Machine.")

if __name__ == "__main__":
    app()
