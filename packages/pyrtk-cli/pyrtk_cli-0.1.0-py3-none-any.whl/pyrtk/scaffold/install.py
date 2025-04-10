from pathlib import Path
import subprocess
import platform
from rich.progress import Progress, SpinnerColumn, TextColumn

def create_virtualenv(project_path: Path) -> Path:
    """
    Creates a virtual environment inside the project directory with the name `<project>-venv`
    Example: myproject/myproject-venv
    """
    venv_path = project_path / f"{project_path.name}-venv"

    if venv_path.exists():
        print(f"⚠️  Virtual environment '{venv_path.name}' already exists.")
        return venv_path

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task(f"🐍 Creating virtual environment '{venv_path.name}'...", total=None)

        try:
            subprocess.run(["python3", "-m", "venv", str(venv_path)], check=True)
            progress.update(task, description=f"✅ Virtual environment '{venv_path.name}' created.")
        except subprocess.CalledProcessError:
            progress.update(task, description=f"❌ Failed to create virtual environment '{venv_path.name}'.")

    return venv_path


def install_requirements(project_path: Path):
    """
    Installs packages from requirements.txt using the pip of the created virtual environment,
    then shows a message to the user on how to activate the environment manually.
    """
    req_path = project_path / "requirements.txt"
    if not req_path.exists():
        print("⚠️  No requirements.txt file found.")
        return

    venv_path = create_virtualenv(project_path)

    # Detect pip path in the virtual env
    if platform.system() == "Windows":
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        pip_path = venv_path / "bin" / "pip"

    if not pip_path.exists():
        print(f"❌ pip not found in {pip_path}")
        return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("📦 Installing dependencies...", total=None)

        try:
            subprocess.run(
                [str(pip_path), "install", "-r", str(req_path)],
                check=True
            )
            progress.update(task, description="✅ Dependencies installed successfully.")
        except subprocess.CalledProcessError:
            progress.update(task, description="❌ Failed to install dependencies.")

    # Show activation instructions
    print("\n" + "=" * 60)
    print("🎉 Project setup complete!")
    print("💡 To activate your environment:\n")

    if platform.system() == "Windows":
        print(f"   .\\{project_path.name}-venv\\Scripts\\activate")
    else:
        print(f"   source ./{project_path.name}-venv/bin/activate")

    print("\nThen you can run your project with:\n")
    print("   pyrtk run")
    print("=" * 60 + "\n")