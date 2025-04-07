import typer
import ast

app = typer.Typer(help="""
Validate a Quantum Machine's project.json file.

This command ensures the structure and required fields of project.json are valid.

Example:
    quantum validate machine HelloWorld
""")

@app.command()
def machine(file: str):
    """
    Validate a Quantum Machine's project.json file.

    This command ensures the structure and required fields of project.json are valid.

    Example:
        quantum validate machine HelloWorld
    """
    try:
        with open(file) as f:
            tree = ast.parse(f.read(), filename=file)

        class_found = any(
            isinstance(node, ast.ClassDef) and any(
                base.id == "CoreEngine" for base in node.bases if isinstance(base, ast.Name)
            )
            for node in tree.body
        )

        if class_found:
            typer.secho("✅ Valid Quantum Machine!", fg=typer.colors.GREEN)
        else:
            typer.secho("❌ No CoreEngine-based class found.", fg=typer.colors.RED)

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)