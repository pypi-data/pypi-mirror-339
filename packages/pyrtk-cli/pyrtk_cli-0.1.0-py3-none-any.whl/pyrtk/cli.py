import typer
from pyrtk.scaffold.api import create_api_structure
from pyrtk.scaffold.ms import create_ms_structure
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from pathlib import Path
import subprocess
import platform

app = typer.Typer(help="PyRTK - Python REST Toolkit CLI")

@app.command("create")
def create_project(
    name: str = typer.Argument(..., help="Name of the new project"),
    type: str = typer.Option(..., "--type", "-t", help="Project type: 'api' or 'ms'")
):
    """
    Create a new FastAPI project scaffold.
    """
    type = type.lower()

    if type not in ["api", "ms"]:
        typer.echo("❌ Invalid project type. Use --type api or --type ms")
        raise typer.Exit(code=1)

    typer.echo(f"🔨 Creating {type.upper()} project: {name}...")

    try:
        if type == "api":
            create_api_structure(name)
        elif type == "ms":
            create_ms_structure(name)

        typer.echo(f"✅ Project '{name}' created successfully.")
    
    except FileExistsError:
        typer.echo(f"⚠️  The folder '{name}' already exists.")
        raise typer.Exit(code=1)

@app.command("init")
def init_project():
    """Initialize a PyRTK-compatible project in the current folder."""
    typer.echo("🔧 Project initialized.")

@app.command("install")
def install_plugin(name: str = typer.Argument(..., help="Name of the plugin to install")):
    """Install a plugin or additional dependency."""
    typer.echo(f"📦 Installing plugin: {name}")

@app.command("generate")
def generate_component(component: str = typer.Argument(..., help="Component type (e.g., router, model, schema)"),
                       name: str = typer.Argument(..., help="Name of the component")):
    """Generate a specific module (router, model, etc.)."""
    typer.echo(f"✨ Generating {component} named {name}")

@app.command("run")
def run_dev():
    """Run the current PyRTK project using Uvicorn."""
    console = Console()
    current_dir = Path.cwd()
    project_name = current_dir.name
    venv_path = current_dir / f"{project_name}-venv"

    # Detect python path from venv
    if platform.system() == "Windows":
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"

    if not python_path.exists():
        console.print(f"[bold red]❌ Virtual environment not found at:[/bold red] {venv_path}")
        console.print("💡 Run [bold yellow]pyrtk create[/bold yellow] first or activate the environment manually.")
        raise typer.Exit(code=1)

    if not (current_dir / "main.py").exists():
        console.print("[bold red]❌ 'main.py' not found in project root.[/bold red]")
        raise typer.Exit(code=1)

    # Mostrar spinner de lanzamiento
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("\n[bold cyan]👁️  Tracking Uvicorn server logs... (press CTRL+C to stop)[/bold cyan]\n", total=None)

        try:
            # Lanza el server y reemplaza el proceso actual
            subprocess.run(
                [str(python_path), "-m", "uvicorn", "main:app", "--reload"],
                check=True
            )
        except subprocess.CalledProcessError:
            progress.update(task, description="❌ Failed to start Uvicorn server.")
            raise typer.Exit(code=1)

@app.command("test")
def run_tests():
    """Run all unit and integration tests."""
    typer.echo("🧪 Running tests...")

@app.command("docs")
def open_docs():
    """Open the Swagger API documentation."""
    typer.echo("📖 Opening Swagger docs...")

def main():
    app()

if __name__ == "__main__":
    main()