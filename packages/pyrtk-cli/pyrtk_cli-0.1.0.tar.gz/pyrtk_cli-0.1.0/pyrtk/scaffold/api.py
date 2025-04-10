from pathlib import Path
from rich.progress import Progress
from pyrtk.scaffold.install import install_requirements

def create_api_structure(name: str):
    base = Path(name)

    # Carpetas necesarias
    folders = [
        base / "app/routers",
        base / "app/schemas",
        base / "app/lib",
    ]

    # Archivos con contenido
    files_with_content = {
        base / "main.py": """\
from fastapi import FastAPI
from app.middleware import apply_middlewares
from app.routers import root

app = FastAPI()

apply_middlewares(app)

app.include_router(root.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
""",
        base / "app/middleware.py": """\
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def apply_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
""",
        base / "app/routers/root.py": """\
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to your new PyRTK API"}
""",
        base / "requirements.txt": "fastapi\nuvicorn\n",
    }

    # Archivos vacíos
    empty_files = [
        base / "README.md",
        base / ".env",
        base / ".gitignore",
    ]

    with Progress() as progress:
        task = progress.add_task("[cyan]Creating API project files...", total=len(folders) + len(files_with_content) + len(empty_files))

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            progress.update(task, advance=1)

        for file, content in files_with_content.items():
            file.write_text(content)
            progress.update(task, advance=1)

        for file in empty_files:
            file.touch()
            progress.update(task, advance=1)

    install_requirements(base)