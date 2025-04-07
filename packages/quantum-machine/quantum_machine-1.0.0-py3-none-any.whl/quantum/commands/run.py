import typer
import subprocess
from pathlib import Path
import json

app = typer.Typer(help="""
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
)

@app.command()
def machine(machine_name: str):
    """
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
    # ✅ Check for core engine only when running the machine
    try:
        from quantum.CoreEngine import CoreEngine  # Only needed when actually running the machine
    except ImportError:
        typer.secho("❌ Missing dependency: 'quantum-core-engine' is required. Please install it separately.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.echo(f"Running machine: {machine_name}")
    
    project_path = Path(machine_name).resolve()

    if not (project_path / "main.py").exists():
        typer.secho("❌ Entrypoint main.py file not found!", fg=typer.colors.RED)
        raise typer.Exit()
    
    input_data = {
        "machine_name": machine_name,
        "input_data": {"env": "dev"},
        "output": f"{machine_name}.json",
        "depends_machine": []
    }

    command = [
        "python",
        f"./{machine_name}/main.py",
        json.dumps(input_data)
    ]

    typer.echo(f"Running machine '{machine_name}' with env='dev'")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Stream logs line by line
    for line in process.stdout:
        print(line, end='')

    process.wait()

    if process.returncode == 0:
        typer.echo("✅ Machine executed successfully")
        typer.echo(process.stdout)
    else:
        typer.echo("❌ Machine execution failed", err=True)
        typer.echo(process.stderr, err=True)

    #"""Run a Quantum Machine using Docker"""
    # file_path = Path(file).resolve()
    # folder = file_path.parent

    # docker_cmd = [
    #     "docker", "run", "--rm",
    #     "-v", f"{folder}:/app",
    #     "quantumdatalytica/quantum-core:latest",
    #     "python", f"/app/{file_path.name}"
    # ]

    # try:
    #     subprocess.run(docker_cmd, check=True)
    # except subprocess.CalledProcessError as e:
    #     typer.secho(f"❌ Docker execution failed: {e}", fg=typer.colors.RED)